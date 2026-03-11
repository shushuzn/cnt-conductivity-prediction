#!/usr/bin/env python3
"""
CNT 性能预测 - 多模型对比

对比 GP / Random Forest / XGBoost 在 CNT 电导率预测上的表现

依赖:
    pip install scikit-learn xgboost pandas numpy matplotlib
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import io

# 修复 Windows 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
import matplotlib.pyplot as plt
import json

print("=" * 70)
print("CNT 性能预测 - 多模型对比")
print("=" * 70)

# ============================================================================
# 配置
# ============================================================================
import argparse

parser = argparse.ArgumentParser(description="CNT 多模型对比")
parser.add_argument('--data', type=str, default=None, help='数据文件路径')
args = parser.parse_args()

DATA_PATH = Path("D:/OpenClaw/workspace/11-research/cnt-research/data/cnt_dataset_v2_synthetic.csv")
if args.data:
    DATA_PATH = Path(args.data)

MODELS_DIR = Path("D:/OpenClaw/workspace/11-research/cnt-research/models")
FIGURES_DIR = Path("D:/OpenClaw/workspace/11-research/cnt-research/figures")

MODELS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# 特征和目标
FEATURES = ['diameter_nm', 'length_um', 'layers', 'cvd_temperature_C']
TARGET = 'conductivity_Sm'

# ============================================================================
# 1. 加载数据 + 特征工程
# ============================================================================
print("\n[1/5] 加载数据...")

if not DATA_PATH.exists():
    print(f"  ❌ 数据文件不存在：{DATA_PATH}")
    exit(1)

df = pd.read_csv(DATA_PATH)
print(f"  数据文件：{DATA_PATH}")
print(f"  原始样本数：{len(df)}")

# 衍生特征
print("\n[2/5] 特征工程...")

# 1. 长径比
df['aspect_ratio'] = df['length_um'] * 1000 / df['diameter_nm']

# 2. 直径对数
df['log_diameter'] = np.log10(df['diameter_nm'] + 1e-6)

# 3. SWCNT 标识
df['is_swcnn'] = (df['layers'] == 1).astype(int)

# 4. CVD 标识
df['is_cvd'] = df['method'].apply(lambda x: 1 if x == 'CVD' else 0)

# 5. 温度归一化
df['temp_normalized'] = df['cvd_temperature_C'] / 1000.0

# 6. 催化剂存在性
df['has_catalyst'] = df['catalyst'].notna().astype(int)

# 7. 碳源存在性
df['has_carbon_source'] = df['carbon_source'].notna().astype(int)

# 8. 体积分数估算
df['volume_fraction_est'] = 1.0 / (df['diameter_nm'] ** 2) * df['layers']

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

# 处理缺失值
df = df.dropna(subset=FEATURES_ENHANCED + [TARGET])
print(f"  有效样本数：{len(df)}")

# 对数转换
y = np.log10(df[TARGET].values)
X = df[FEATURES_ENHANCED].values

# 数据集划分
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

print(f"  训练集：{len(X_train)} 样本")
print(f"  测试集：{len(X_test)} 样本")

# ============================================================================
# 3. 多模型训练对比
# ============================================================================
print("\n[3/5] 模型训练...")

models = {
    'GP': GaussianProcessRegressor(
        kernel=ConstantKernel(1.0) * RBF(length_scale=[1.0] * len(FEATURES_ENHANCED)) + WhiteKernel(0.1),
        n_restarts_optimizer=10,
        random_state=42,
        normalize_y=True
    ),
    'Random Forest': RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    ),
    'Gradient Boosting': GradientBoostingRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    ),
    'Ridge': Ridge(alpha=1.0)
}

# 尝试导入 XGBoost
try:
    import xgboost as xgb
    models['XGBoost'] = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1
    )
    print("  ✅ XGBoost 可用")
except ImportError:
    print("  ⚠️  XGBoost 未安装，跳过 (pip install xgboost)")

results = []

for name, model in models.items():
    print(f"\n  训练 {name}...")
    
    try:
        # 训练
        model.fit(X_train, y_train)
        
        # 预测
        y_pred = model.predict(X_test)
        
        # 评估
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # 交叉验证
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()
        
        results.append({
            'name': name,
            'r2': r2,
            'mae': mae,
            'rmse': rmse,
            'cv_r2_mean': cv_mean,
            'cv_r2_std': cv_std
        })
        
        print(f"    R² = {r2:.4f}")
        print(f"    MAE = {mae:.4f}")
        print(f"    RMSE = {rmse:.4f}")
        print(f"    CV R² = {cv_mean:.4f} (+/- {cv_std:.4f})")
        
    except Exception as e:
        print(f"    ❌ 错误：{e}")
        results.append({
            'name': name,
            'r2': np.nan,
            'mae': np.nan,
            'rmse': np.nan,
            'cv_r2_mean': np.nan,
            'cv_r2_std': np.nan
        })

# ============================================================================
# 4. 结果对比
# ============================================================================
print("\n[4/5] 结果对比...")

print("\n" + "=" * 70)
print(f"{'模型':<20} {'R²':<10} {'MAE':<12} {'RMSE':<12} {'CV R²':<15}")
print("=" * 70)

for r in sorted(results, key=lambda x: x['r2'], reverse=True):
    if not np.isnan(r['r2']):
        print(f"{r['name']:<20} {r['r2']:<10.4f} {r['mae']:<12.4f} {r['rmse']:<12.4f} {r['cv_r2_mean']:<10.4f} (+/- {r['cv_r2_std']:.4f})")

print("=" * 70)

# 最佳模型
best = max([r for r in results if not np.isnan(r['r2'])], key=lambda x: x['r2'])
print(f"\n🏆 最佳模型：{best['name']} (R² = {best['r2']:.4f})")

# ============================================================================
# 5. 可视化
# ============================================================================
print("\n[5/5] 生成可视化...")

# 1. R² 对比柱状图
fig, ax = plt.subplots(figsize=(10, 6))

model_names = [r['name'] for r in results if not np.isnan(r['r2'])]
r2_scores = [r['r2'] for r in results if not np.isnan(r['r2'])]
cv_scores = [r['cv_r2_mean'] for r in results if not np.isnan(r['r2'])]
cv_stds = [r['cv_r2_std'] for r in results if not np.isnan(r['r2'])]

x = np.arange(len(model_names))
width = 0.35

bars1 = ax.bar(x - width/2, r2_scores, width, label='Test R²', color='steelblue')
bars2 = ax.bar(x + width/2, cv_scores, width, yerr=cv_stds, label='CV R² (5-fold)', color='coral', capsize=5)

ax.set_ylabel('R² Score')
ax.set_title('CNT 电导率预测 - 多模型对比')
ax.set_xticks(x)
ax.set_xticklabels(model_names, rotation=15)
ax.legend()
ax.set_ylim(0, max(r2_scores) * 1.2)

# 添加数值标签
for bar in bars1:
    height = bar.get_height()
    ax.annotate(f'{height:.3f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

for bar in bars2:
    height = bar.get_height()
    ax.annotate(f'{height:.3f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "cnt_model_comparison.png", dpi=300, bbox_inches='tight')
print(f"  ✅ 对比图已保存：{FIGURES_DIR / 'cnt_model_comparison.png'}")

# 保存结果
results_df = pd.DataFrame(results)
results_df.to_csv(MODELS_DIR / "model_comparison_results.csv", index=False)
print(f"  ✅ 结果已保存：{MODELS_DIR / 'model_comparison_results.csv'}")

print("\n" + "=" * 70)
print("✅ 多模型对比完成！")
print("=" * 70)
