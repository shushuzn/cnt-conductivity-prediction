#!/usr/bin/env python3
"""
CNT 性能预测 - 多模型对比 (使用 v4_real 数据集，274 样本)

对比模型：
- Gaussian Process (GP)
- Random Forest (RF)
- Gradient Boosting (GB)
- Ridge Regression
- XGBoost (如果可用)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import json

print("=" * 70)
print("CNT 性能预测 - 多模型对比 (v4_real, 274 样本)")
print("=" * 70)

# ============================================================================
# 配置
# ============================================================================
DATA_PATH = Path("data/cnt_dataset_v4_real.csv")
MODELS_DIR = Path("models")
FIGURES_DIR = Path("figures")

MODELS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# 1. 加载数据
# ============================================================================
print("\n[1/5] 加载数据...")

df = pd.read_csv(DATA_PATH)
print(f"  数据文件：{DATA_PATH}")
print(f"  原始样本数：{len(df)}")

# 填充 length_um
df['length_um'] = df['length_um'].fillna(df['length_um'].median())

# 衍生特征
df['aspect_ratio'] = df['length_um'] * 1000 / df['diameter_nm']
df['log_diameter'] = np.log10(df['diameter_nm'] + 1e-6)
df['is_swcnn'] = (df['layers'] == 1).astype(int)
df['is_cvd'] = df['method'].apply(lambda x: 1 if x == 'CVD' else 0)
df['temp_normalized'] = (df['cvd_temperature_C'] / 1000.0).fillna(0)
df['has_catalyst'] = df['catalyst'].notna().astype(int)
df['has_carbon_source'] = df['carbon_source'].notna().astype(int)
df['volume_fraction_est'] = 1.0 / (df['diameter_nm'] ** 2) * df['layers']

FEATURES = [
    'diameter_nm', 'length_um', 'layers',
    'aspect_ratio', 'log_diameter', 'is_swcnn', 'is_cvd',
    'temp_normalized', 'has_catalyst', 'has_carbon_source', 'volume_fraction_est'
]
TARGET = 'conductivity_Sm'

df = df.dropna(subset=FEATURES + [TARGET])
print(f"  有效样本数：{len(df)}")

X = df[FEATURES].values
y = np.log10(df[TARGET].values)  # 对数转换

# 数据集划分
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
print(f"  训练集：{len(X_train)} 样本")
print(f"  测试集：{len(X_test)} 样本")

# 标准化
scaler_X = StandardScaler()
X_train_scaled = scaler_X.fit_transform(X_train)
X_test_scaled = scaler_X.transform(X_test)

# ============================================================================
# 2. 模型训练
# ============================================================================
print("\n[2/5] 模型训练...")

models = {
    'GP': GaussianProcessRegressor(
        kernel=ConstantKernel(1.0) * RBF(length_scale=1.0) + WhiteKernel(noise_level=0.1),
        n_restarts_optimizer=5,
        random_state=42
    ),
    'Random_Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
    'Gradient_Boosting': GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42),
    'Ridge': Ridge(alpha=1.0)
}

results = []

for name, model in models.items():
    print(f"\n  训练 {name}...")
    
    # 训练
    model.fit(X_train_scaled, y_train)
    
    # 预测
    y_pred = model.predict(X_test_scaled)
    
    # 评估
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # 交叉验证
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')
    cv_r2_mean = cv_scores.mean()
    cv_r2_std = cv_scores.std()
    
    print(f"    R2 = {r2:.4f}")
    print(f"    MAE = {mae:.4f}")
    print(f"    RMSE = {rmse:.4f}")
    print(f"    CV R2 = {cv_r2_mean:.4f} (+/- {cv_r2_std:.4f})")
    
    results.append({
        'model': name,
        'r2': r2,
        'mae': mae,
        'rmse': rmse,
        'cv_r2_mean': cv_r2_mean,
        'cv_r2_std': cv_r2_std
    })

# 排序
results.sort(key=lambda x: x['r2'], reverse=True)

# ============================================================================
# 3. 结果对比
# ============================================================================
print("\n" + "=" * 70)
print("模型性能对比")
print("=" * 70)
print(f"{'模型':<20} {'R2':<10} {'MAE':<12} {'RMSE':<12} {'CV R2':<15}")
print("=" * 70)

for r in results:
    print(f"{r['model']:<20} {r['r2']:<10.4f} {r['mae']:<12.4f} {r['rmse']:<12.4f} {r['cv_r2_mean']:<10.4f} (+/- {r['cv_r2_std']:.4f})")

print("=" * 70)
print(f"🏆 最佳模型：{results[0]['model']} (R2 = {results[0]['r2']:.4f})")

# 保存结果
results_df = pd.DataFrame(results)
results_df.to_csv(MODELS_DIR / "model_comparison_results_v4.csv", index=False)
print(f"\n结果已保存：{MODELS_DIR / 'model_comparison_results_v4.csv'}")

# ============================================================================
# 4. 可视化
# ============================================================================
print("\n[4/5] 生成可视化...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 图 1: R2 对比
ax1 = axes[0]
models_names = [r['model'].replace('_', '\n') for r in results]
r2_values = [r['r2'] for r in results]
colors = ['#2ecc71' if r['r2'] > 0.7 else '#3498db' if r['r2'] > 0.5 else '#e74c3c' for r in results]

bars = ax1.barh(models_names, r2_values, color=colors, edgecolor='black', linewidth=1.5)
ax1.set_xlabel('R2 Score', fontsize=12)
ax1.set_title('Model Comparison - R2 Score', fontsize=14)
ax1.axvline(x=0.75, color='green', linestyle='--', linewidth=2, label='Target (0.75)')
ax1.legend()

# 添加数值标签
for bar, val in zip(bars, r2_values):
    ax1.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
             f'{val:.3f}', ha='left', va='center', fontsize=11, fontweight='bold')

# 图 2: CV R2 对比
ax2 = axes[1]
cv_r2_means = [r['cv_r2_mean'] for r in results]
cv_r2_stds = [r['cv_r2_std'] for r in results]

bars2 = ax2.barh(models_names, cv_r2_means, xerr=cv_r2_stds, color='#9b59b6', 
                 edgecolor='black', linewidth=1.5, capsize=5)
ax2.set_xlabel('Cross-Validation R2', fontsize=12)
ax2.set_title('Model Comparison - CV R2 (5-fold)', fontsize=14)
ax2.axvline(x=0.6, color='green', linestyle='--', linewidth=2, label='Target (0.60)')
ax2.legend()

# 添加数值标签
for bar, val, std in zip(bars2, cv_r2_means, cv_r2_stds):
    ax2.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
             f'{val:.3f}\n(+/- {std:.3f})', ha='left', va='center', fontsize=9)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "cnt_model_comparison_v4.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  [OK] 对比图：{FIGURES_DIR / 'cnt_model_comparison_v4.png'}")

# ============================================================================
# 5. 完成
# ============================================================================
print("\n" + "=" * 70)
print("[OK] 多模型对比完成！")
print("=" * 70)

print(f"\n关键发现:")
print(f"  最佳模型：{results[0]['model']}")
print(f"  最佳 R2: {results[0]['r2']:.4f}")
print(f"  最佳 CV R2: {results[0]['cv_r2_mean']:.4f} (+/- {results[0]['cv_r2_std']:.4f})")

if results[0]['r2'] >= 0.75:
    print(f"\n✅ R2 目标达成 (>= 0.75)")
else:
    print(f"\n⏸️ R2 未达目标 (>= 0.75)，需要进一步优化")

print(f"\n输出文件:")
print(f"  结果：{MODELS_DIR / 'model_comparison_results_v4.csv'}")
print(f"  图表：{FIGURES_DIR / 'cnt_model_comparison_v4.png'}")
