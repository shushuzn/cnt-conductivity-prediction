#!/usr/bin/env python3
"""
CNT 性能预测 - GP 基线模型

基于 LIG 研究框架复用的 GP 模型
用于 CNT 数据集的基线预测

依赖:
    pip install scikit-learn pandas numpy matplotlib
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import json
import matplotlib.pyplot as plt

print("=" * 70)
print("CNT 性能预测 - GP 基线模型")
print("=" * 70)

# ============================================================================
# 1. 加载数据 (示例数据，实际使用时替换为真实 CNT 数据集)
# ============================================================================
print("\n[1/6] 加载数据...")

# 创建示例数据 (实际使用时替换为真实数据)
np.random.seed(42)
n_samples = 300

# 模拟 CNT 特征
data = {
    'diameter_nm': np.random.uniform(1, 50, n_samples),  # 直径 1-50 nm
    'length_um': np.random.uniform(1, 500, n_samples),   # 长度 1-500 μm
    'layers': np.random.randint(1, 20, n_samples),       # 层数 1-20
    'cvd_temperature_C': np.random.uniform(600, 1000, n_samples),  # CVD 温度
    'growth_time_min': np.random.uniform(10, 60, n_samples),  # 生长时间
}

df = pd.DataFrame(data)

# 模拟电导率 (基于物理关系 + 噪声)
df['conductivity_Sm'] = (
    1e6 * np.exp(-0.05 * df['diameter_nm']) *  # 直径负相关
    np.exp(-0.02 * df['layers']) *              # 层数负相关
    (1 + 0.001 * df['length_um']) *             # 长度正相关
    np.exp(-((df['cvd_temperature_C'] - 800) ** 2) / 50000) *  # 温度最优值
    np.random.uniform(0.5, 1.5, n_samples)      # 噪声
)

features = ['diameter_nm', 'length_um', 'layers', 'cvd_temperature_C', 'growth_time_min']
target = 'conductivity_Sm'

print(f"  样本数：{len(df)}")
print(f"  特征：{features}")
print(f"  目标：{target}")
print(f"  电导率范围：{df[target].min():.2e} - {df[target].max():.2e} S/m")

# 数据探索统计
print(f"\n  数据统计:")
print(df[features + [target]].describe())

# ============================================================================
# 2. 数据预处理
# ============================================================================
print("\n[2/6] 数据预处理...")

X = df[features].values
y = np.log10(df[target].values)  # 对数转换，使分布更均匀

# 数据集划分
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 标准化
scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_train_scaled = scaler_X.fit_transform(X_train)
X_test_scaled = scaler_X.transform(X_test)
y_train_scaled = scaler_y.fit_transform(y_train.reshape(-1, 1)).flatten()
y_test_scaled = scaler_y.transform(y_test.reshape(-1, 1)).flatten()

print(f"  训练集：{len(X_train)} 样本")
print(f"  测试集：{len(X_test)} 样本")
print(f"  [OK] 标准化完成")

# ============================================================================
# 3. GP 模型训练
# ============================================================================
print("\n[3/6] GP 模型训练...")

# 核函数 (与 LIG 研究相同配置)
kernel = ConstantKernel(100) * RBF(length_scale=[1.0] * len(features)) + WhiteKernel(0.05)

gp_model = GaussianProcessRegressor(
    kernel=kernel,
    n_restarts_optimizer=20,
    random_state=42,
    normalize_y=True
)

print(f"  核函数：{kernel}")
print(f"  开始训练...")

gp_model.fit(X_train_scaled, y_train_scaled)
print(f"  [OK] GP 模型训练完成")
print(f"  优化后核函数：{gp_model.kernel_}")

# ============================================================================
# 4. 预测与评估
# ============================================================================
print("\n[4/6] 预测与评估...")

# 预测 (带不确定性)
y_pred_scaled, y_std_scaled = gp_model.predict(X_test_scaled, return_std=True)

# 反标准化
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()
y_std = y_std_scaled * scaler_y.scale_[0]
y_true = scaler_y.inverse_transform(y_test_scaled.reshape(-1, 1)).flatten()

# 评估
r2 = r2_score(y_true, y_pred)
mae = mean_absolute_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
nrmse = rmse / np.mean(y_true) * 100

print(f"\n  测试集性能:")
print(f"    R2 = {r2:.3f} (目标：> 0.75)")
print(f"    MAE = {mae:.2e} S/m")
print(f"    RMSE = {rmse:.2e} S/m")
print(f"    NRMSE = {nrmse:.1f}%")

# 交叉验证
cv_scores = cross_val_score(gp_model, X_train_scaled, y_train_scaled, cv=5, scoring='r2')
print(f"\n  5 折交叉验证:")
print(f"    平均 R2 = {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")

# 不确定性
mean_uncertainty = np.mean(y_std)
rel_uncertainty = mean_uncertainty / np.mean(y_true) * 100

print(f"\n  不确定性:")
print(f"    平均：±{mean_uncertainty:.2e} S/m ({rel_uncertainty:.1f}%)")

# 95% 置信区间
ci_95_lower = y_pred - 2 * y_std
ci_95_upper = y_pred + 2 * y_std

# 覆盖率
in_ci = (y_true >= ci_95_lower) & (y_true <= ci_95_upper)
coverage = np.mean(in_ci) * 100
print(f"    95% CI 覆盖率：{coverage:.1f}% (目标：~95%)")

# ============================================================================
# 5. 保存模型
# ============================================================================
print("\n[5/6] 保存模型...")

output_dir = Path("D:/OpenClaw/workspace/11-research/cnt-research/models")
output_dir.mkdir(parents=True, exist_ok=True)

# 保存模型和标准化器
joblib.dump(gp_model, output_dir / "CNT_GP_baseline.pkl")
joblib.dump(scaler_X, output_dir / "CNT_GP_scaler_X.pkl")
joblib.dump(scaler_y, output_dir / "CNT_GP_scaler_y.pkl")

print(f"  [OK] 模型已保存:")
print(f"    CNT_GP_baseline.pkl")
print(f"    CNT_GP_scaler_X.pkl")
print(f"    CNT_GP_scaler_y.pkl")

# 保存配置
config = {
    'model': 'GaussianProcessRegressor',
    'features': features,
    'target': 'conductivity_Sm',
    'kernel': str(gp_model.kernel_),
    'dataset': {
        'n_samples': len(df),
        'n_train': len(X_train),
        'n_test': len(X_test),
        'test_size': 0.2,
        'random_state': 42
    },
    'performance': {
        'r2': float(r2),
        'mae': float(mae),
        'rmse': float(rmse),
        'nrmse_pct': float(nrmse),
        'cv_r2_mean': float(cv_scores.mean()),
        'cv_r2_std': float(cv_scores.std()),
        'mean_uncertainty': float(mean_uncertainty),
        'relative_uncertainty_pct': float(rel_uncertainty),
        'ci_95_coverage': float(coverage)
    }
}

config_path = output_dir / "CNT_GP_baseline_config.json"
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"  [OK] 配置已保存：{config_path}")

# ============================================================================
# 6. 可视化
# ============================================================================
print("\n[6/6] 生成图表...")

figures_dir = Path("D:/OpenClaw/workspace/11-research/cnt-research/figures")
figures_dir.mkdir(parents=True, exist_ok=True)

# 图 1: 预测 vs 真实值
fig1, ax1 = plt.subplots(figsize=(8, 6), dpi=300)
ax1.errorbar(y_true, y_pred, yerr=y_std, fmt='o', capsize=3, markersize=6, alpha=0.7, 
             color='blue', ecolor='gray', elinewidth=1.5)
ax1.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', linewidth=2, label='Ideal prediction')
ax1.set_xlabel("True conductivity (S/m)", fontsize=12)
ax1.set_ylabel("Predicted conductivity (S/m)", fontsize=12)
ax1.set_title(f"CNT GP Baseline\nR2 = {r2:.3f}, MAE = {mae:.2e} S/m", fontsize=14)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(figures_dir / "cnt_gp_baseline_prediction.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  [OK] Prediction plot: {figures_dir / 'cnt_gp_baseline_prediction.png'}")

# 图 2: 残差分析
fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(14, 5), dpi=300)

# 残差 vs 预测值
residuals = y_true - y_pred
ax2a.scatter(y_pred, residuals, alpha=0.7, s=60, color='blue')
ax2a.axhline(y=0, color='red', linestyle='--', linewidth=2)
ax2a.set_xlabel("Predicted conductivity (S/m)", fontsize=12)
ax2a.set_ylabel("Residual (S/m)", fontsize=12)
ax2a.set_title("Residual Analysis", fontsize=13)
ax2a.grid(True, alpha=0.3, linestyle='--')

# 残差分布
ax2b.hist(residuals, bins=15, edgecolor='black', alpha=0.7, color='skyblue')
ax2b.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Zero residual')
ax2b.set_xlabel("Residual (S/m)", fontsize=12)
ax2b.set_ylabel("Count", fontsize=12)
ax2b.set_title(f"Residual Distribution\nMean={np.mean(residuals):.2e}, Std={np.std(residuals):.2e}", fontsize=13)
ax2b.legend(fontsize=10)
ax2b.grid(True, alpha=0.3, linestyle='--', axis='y')

plt.tight_layout()
plt.savefig(figures_dir / "cnt_gp_baseline_residuals.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  [OK] Residual plot: {figures_dir / 'cnt_gp_baseline_residuals.png'}")

# ============================================================================
# 7. 总结
# ============================================================================
print("\n" + "=" * 70)
print("[OK] CNT GP Baseline Model Complete!")
print("=" * 70)

print(f"\nPerformance Summary:")
print(f"  R2 = {r2:.3f} {'✅' if r2 >= 0.75 else '⏳'} (目标：> 0.75)")
print(f"  MAE = {mae:.2e} S/m")
print(f"  95% CI Coverage = {coverage:.1f}%")

print(f"\nFiles:")
print(f"  Model: {output_dir / 'CNT_GP_baseline.pkl'}")
print(f"  Config: {output_dir / 'CNT_GP_baseline_config.json'}")
print(f"  Figures: {figures_dir / 'cnt_gp_baseline_*.png'}")

print(f"\nNext Steps:")
print(f"  1. Replace with real CNT dataset")
print(f"  2. Feature selection and optimization")
print(f"  3. SHAP analysis for interpretability")
print(f"  4. Paper writing")
