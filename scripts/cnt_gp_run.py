#!/usr/bin/env python3
"""
CNT 性能预测 - GP 模型训练和评估

高斯过程回归 (Gaussian Process Regression) 用于 CNT 电导率预测

依赖:
    pip install scikit-learn pandas numpy matplotlib
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel, Matern
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import json
import pickle

print("=" * 70)
print("CNT 性能预测 - GP 模型训练")
print("=" * 70)

# ============================================================================
# 配置
# ============================================================================
import argparse

parser = argparse.ArgumentParser(description="CNT GP 模型训练")
parser.add_argument('--data', type=str, default=None, help='数据文件路径')
args = parser.parse_args()

DATA_PATH = Path("D:/OpenClaw/workspace/11-research/cnt-research/data/cnt_dataset_v1.csv")
if args.data:
    DATA_PATH = Path(args.data)
    
MODELS_DIR = Path("D:/OpenClaw/workspace/11-research/cnt-research/models")
FIGURES_DIR = Path("D:/OpenClaw/workspace/11-research/cnt-research/figures")

MODELS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# 特征和目标
# 注意：cvd_temperature_C 只有 CVD 法样本有，其他方法为 NaN
# 使用更保守的特征集，确保数据完整性
FEATURES_CORE = ['diameter_nm', 'length_um', 'layers']
FEATURES_FULL = ['diameter_nm', 'length_um', 'layers', 'cvd_temperature_C']
TARGET = 'conductivity_Sm'

# 自动选择特征：如果 cvd_temperature_C 缺失率>50%，只用核心特征
USE_FULL_FEATURES = None  # 将在数据加载后决定

# ============================================================================
# 1. 加载数据
# ============================================================================
print("\n[1/6] 加载数据...")

if not DATA_PATH.exists():
    print(f"  ❌ 数据文件不存在：{DATA_PATH}")
    print("  提示：请先收集 CNT 数据集")
    exit(1)

df = pd.read_csv(DATA_PATH)
print(f"  数据文件：{DATA_PATH}")
print(f"  原始样本数：{len(df)}")

# 检查必要列
missing_cols = [col for col in FEATURES_CORE + [TARGET] if col not in df.columns]
if missing_cols:
    print(f"  ❌ 缺少列：{missing_cols}")
    exit(1)

# 自动选择特征：检查 cvd_temperature_C 完整性
if 'cvd_temperature_C' in df.columns:
    temp_missing_rate = df['cvd_temperature_C'].isna().mean()
    print(f"  cvd_temperature_C 缺失率：{temp_missing_rate:.1%}")
    
    if temp_missing_rate > 0.5:
        print(f"  [INFO] 缺失率>50%，使用核心特征 (3 个)")
        FEATURES = FEATURES_CORE.copy()
    else:
        print(f"  [INFO] 缺失率≤50%，使用完整特征 (4 个)")
        FEATURES = FEATURES_FULL.copy()
else:
    print(f"  [INFO] cvd_temperature_C 列不存在，使用核心特征 (3 个)")
    FEATURES = FEATURES_CORE.copy()

# 处理缺失值
df = df.dropna(subset=FEATURES + [TARGET])
print(f"  有效样本数：{len(df)} (删除 {len(df) - len(df)} 个缺失值)")

if len(df) < 5:
    print(f"  [WARN] 样本数过少 ({len(df)} < 5)，模型可能不可靠")
    print("  建议：继续收集数据，目标 300+ 样本")

# 数据概览
print(f"\n  数据范围:")
for col in FEATURES + [TARGET]:
    print(f"    {col}: {df[col].min():.2f} - {df[col].max():.2f}")

# ============================================================================
# 2. 数据预处理 + 特征工程
# ============================================================================
print("\n[2/6] 数据预处理 + 特征工程...")

# 衍生特征
print("  添加衍生特征...")

# 1. 长径比 (aspect ratio) - 如果 length_um 缺失，用典型值填充
df['length_um_filled'] = df['length_um'].fillna(df['length_um'].median())
df['aspect_ratio'] = df['length_um_filled'] * 1000 / df['diameter_nm']

# 2. 直径对数 (捕捉非线性效应)
df['log_diameter'] = np.log10(df['diameter_nm'] + 1e-6)

# 3. 层数分类 (SWCNT vs MWCNT)
df['is_swcnn'] = (df['layers'] == 1).astype(int)

# 4. 工艺复杂度 (CVD=1, 其他=0)
df['is_cvd'] = df['method'].apply(lambda x: 1 if x == 'CVD' else 0)

# 5. 温度归一化 (仅 CVD 样本，其他填 0)
df['temp_normalized'] = (df['cvd_temperature_C'] / 1000.0).fillna(0)

# 6. 催化剂存在性
df['has_catalyst'] = df['catalyst'].notna().astype(int)

# 7. 碳源存在性
df['has_carbon_source'] = df['carbon_source'].notna().astype(int)

# 8. 体积分数估算 (简化模型)
df['volume_fraction_est'] = 1.0 / (df['diameter_nm'] ** 2) * df['layers']

# 更新特征列表
FEATURES_ENHANCED = FEATURES + [
    'aspect_ratio',
    'log_diameter',
    'is_swcnn',
    'is_cvd',
    'temp_normalized',
    'has_catalyst',
    'has_carbon_source',
    'volume_fraction_est'
]

print(f"  原始特征：{len(FEATURES)} 个")
print(f"  增强特征：{len(FEATURES_ENHANCED)} 个 (+{len(FEATURES_ENHANCED) - len(FEATURES)})")

# 再次清理 NaN（应该没有了，因为做了填充）
df = df.dropna(subset=FEATURES_ENHANCED + [TARGET])
print(f"  最终有效样本：{len(df)}")

X = df[FEATURES_ENHANCED].values
y = df[TARGET].values

# 对数转换 (电导率跨越多个数量级)
y_log = np.log10(y)

# 数据集划分
test_size = 0.25 if len(df) >= 20 else 0.3
X_train, X_test, y_train, y_test = train_test_split(
    X, y_log, test_size=test_size, random_state=42
)

print(f"  训练集：{len(X_train)} 样本")
print(f"  测试集：{len(X_test)} 样本")

# 标准化
scaler_X = StandardScaler()
scaler_y = StandardScaler()

X_train_scaled = scaler_X.fit_transform(X_train)
X_test_scaled = scaler_X.transform(X_test)
y_train_scaled = scaler_y.fit_transform(y_train.reshape(-1, 1)).flatten()
y_test_scaled = scaler_y.transform(y_test.reshape(-1, 1)).flatten()

print(f"  [OK] 标准化完成")

# ============================================================================
# 3. GP 模型训练
# ============================================================================
print("\n[3/6] GP 模型训练...")

# 核函数：RBF + WhiteKernel (适用于小数据集)
kernel = ConstantKernel(1.0) * RBF(length_scale=[1.0] * len(FEATURES_ENHANCED)) + WhiteKernel(0.1)

gp_model = GaussianProcessRegressor(
    kernel=kernel,
    n_restarts_optimizer=10,
    random_state=42,
    normalize_y=True
)

gp_model.fit(X_train_scaled, y_train_scaled)
print(f"  [OK] GP 模型训练完成")
print(f"  优化后核函数：{gp_model.kernel_}")

# ============================================================================
# 4. 模型评估
# ============================================================================
print("\n[4/6] 模型评估...")

# 预测
y_pred_scaled = gp_model.predict(X_test_scaled)
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()
y_test_orig = scaler_y.inverse_transform(y_test_scaled.reshape(-1, 1)).flatten()

# 指标
r2 = r2_score(y_test_scaled, y_pred_scaled)
mae = mean_absolute_error(y_test_orig, y_pred)
rmse = np.sqrt(mean_squared_error(y_test_orig, y_pred))

print(f"  R2 = {r2:.4f}")
print(f"  MAE = {mae:.2e} S/m")
print(f"  RMSE = {rmse:.2e} S/m")

# 交叉验证 (小数据集时更重要)
if len(X_train) >= 5:
    cv_scores = cross_val_score(gp_model, X_train_scaled, y_train_scaled, cv=3)
    print(f"  Cross-val R2: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")
else:
    print(f"  [WARN] 样本过少，跳过交叉验证")

# 不确定性估计
y_pred_mean, y_pred_std = gp_model.predict(X_test_scaled, return_std=True)
y_pred_std_orig = scaler_y.inverse_transform(y_pred_std.reshape(-1, 1)).flatten()
print(f"  平均预测不确定度：{y_pred_std_orig.mean():.2e} S/m")

# ============================================================================
# 5. 保存模型
# ============================================================================
print("\n[5/6] 保存模型...")

# 保存模型
model_path = MODELS_DIR / "CNT_GP_v1.pkl"
with open(model_path, 'wb') as f:
    pickle.dump({
        'gp_model': gp_model,
        'scaler_X': scaler_X,
        'scaler_y': scaler_y,
        'features': FEATURES,
        'target': TARGET
    }, f)
print(f"  [OK] 模型已保存：{model_path}")

# 保存配置
config = {
    'model_version': 'v1',
    'date': pd.Timestamp.now().isoformat(),
    'n_samples': len(df),
    'n_train': len(X_train),
    'n_test': len(X_test),
    'features': FEATURES,
    'target': TARGET,
    'metrics': {
        'r2': float(r2),
        'mae': float(mae),
        'rmse': float(rmse),
        'cv_r2_mean': float(cv_scores.mean()) if len(X_train) >= 5 else None,
        'cv_r2_std': float(cv_scores.std()) if len(X_train) >= 5 else None
    },
    'kernel': str(gp_model.kernel_)
}

config_path = MODELS_DIR / "CNT_GP_v1_config.json"
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
print(f"  [OK] 配置已保存：{config_path}")

# ============================================================================
# 6. 可视化
# ============================================================================
print("\n[6/6] 生成可视化图表...")

# 图 1: 预测 vs 实际
plt.figure(figsize=(8, 6), dpi=300)
plt.scatter(y_test_orig, y_pred, alpha=0.7, edgecolors='k', linewidth=0.5)
min_val = min(y_test_orig.min(), y_pred.min())
max_val = max(y_test_orig.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='理想预测')
plt.xlabel('实际电导率 (S/m)', fontsize=12)
plt.ylabel('预测电导率 (S/m)', fontsize=12)
plt.title(f'CNT Conductivity Prediction (GP, R2={r2:.3f})', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "cnt_gp_prediction.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  [OK] 预测图：{FIGURES_DIR / 'cnt_gp_prediction.png'}")

# 图 2: 残差分析
residuals = y_test_orig - y_pred
plt.figure(figsize=(8, 6), dpi=300)
plt.scatter(y_pred, residuals, alpha=0.7, edgecolors='k', linewidth=0.5)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('预测电导率 (S/m)', fontsize=12)
plt.ylabel('残差 (S/m)', fontsize=12)
plt.title('残差分析', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "cnt_gp_residuals.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  [OK] 残差图：{FIGURES_DIR / 'cnt_gp_residuals.png'}")

# 图 3: 特征重要性 (基于 GP 长度尺度)
length_scales = gp_model.kernel_.k1.k2.length_scale
importance = 1 / length_scales  # 长度尺度越小，特征越重要
importance_norm = importance / importance.max()

plt.figure(figsize=(12, 6), dpi=300)
bars = plt.bar(FEATURES_ENHANCED, importance_norm, color='steelblue', edgecolor='navy')
plt.xlabel('Feature', fontsize=12)
plt.ylabel('Relative Importance', fontsize=12)
plt.title('CNT Conductivity Prediction - Feature Importance', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3, axis='y')

# 添加数值标签
for bar, val in zip(bars, importance_norm):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
             f'{val:.3f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "cnt_gp_feature_importance.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  [OK] 特征重要性：{FIGURES_DIR / 'cnt_gp_feature_importance.png'}")

# ============================================================================
# 完成
# ============================================================================
print("\n" + "=" * 70)
print("[OK] GP 模型训练完成！")
print("=" * 70)

print(f"\n模型性能:")
print(f"  R2 = {r2:.4f}")
print(f"  MAE = {mae:.2e} S/m")
print(f"  RMSE = {rmse:.2e} S/m")

print(f"\n输出文件:")
print(f"  模型：{model_path}")
print(f"  配置：{config_path}")
print(f"  图表：{FIGURES_DIR / 'cnt_gp_*.png'}")

if len(df) < 50:
    print(f"\n[WARN] 当前样本数 ({len(df)}) 较少，模型可能过拟合")
    print(f"  建议：继续收集数据，目标 300+ 样本")

print(f"\n下一步:")
print(f"  1. 运行 SHAP 分析：py scripts/cnt_shap_analysis.py")
print(f"  2. 继续收集数据")
print(f"  3. 重新训练模型")
