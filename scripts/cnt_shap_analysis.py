#!/usr/bin/env python3
"""
CNT 性能预测 - SHAP 可解释性分析

基于 SHAP (SHapley Additive exPlanations) 分析 GP 模型的特征重要性

依赖:
    pip install shap scikit-learn pandas numpy matplotlib
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 尝试导入 shap
try:
    import shap
    print(f"SHAP version: {shap.__version__}")
except ImportError:
    print("Installing shap...")
    import subprocess
    subprocess.check_call(["pip", "install", "shap"])
    import shap

print("=" * 70)
print("CNT 性能预测 - SHAP 可解释性分析")
print("=" * 70)

# ============================================================================
# 1. 加载数据 (示例数据，实际使用时替换为真实 CNT 数据集)
# ============================================================================
print("\n[1/5] 加载数据...")

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
# 假设：直径越小电导率越高，层数越少电导率越高
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

# ============================================================================
# 2. 数据预处理
# ============================================================================
print("\n[2/5] 数据预处理...")

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
print("\n[3/5] GP 模型训练...")

kernel = ConstantKernel(1.0) * RBF(length_scale=[1.0] * len(features)) + WhiteKernel(0.1)

gp_model = GaussianProcessRegressor(
    kernel=kernel,
    n_restarts_optimizer=20,
    random_state=42,
    normalize_y=True
)

gp_model.fit(X_train_scaled, y_train_scaled)
print(f"  [OK] GP 模型训练完成")
print(f"  优化后核函数：{gp_model.kernel_}")

# 评估
y_pred_scaled = gp_model.predict(X_test_scaled)
from sklearn.metrics import r2_score
r2 = r2_score(y_test_scaled, y_pred_scaled)
print(f"  Test set R2 = {r2:.3f}")

# ============================================================================
# 4. SHAP 分析
# ============================================================================
print("\n[4/5] SHAP 分析...")

# 创建 SHAP explainer (使用 KernelSHAP，适用于 GP 模型)
explainer = shap.KernelExplainer(gp_model.predict, shap.sample(X_train_scaled, 100))

# 计算 SHAP 值 (使用测试集子集以加速)
shap_values = explainer.shap_values(shap.sample(X_test_scaled, 50), nsamples=500)

print(f"  SHAP 值形状：{shap_values.shape}")
print(f"  [OK] SHAP 分析完成")

# ============================================================================
# 5. 可视化
# ============================================================================
print("\n[5/5] 生成可视化图表...")

figures_dir = Path("D:/OpenClaw/workspace/11-research/cnt-research/figures")
figures_dir.mkdir(parents=True, exist_ok=True)

# 图 1: SHAP 摘要图 (特征重要性)
plt.figure(figsize=(10, 6), dpi=300)
shap.summary_plot(shap_values, X_test_scaled, feature_names=features, show=False, plot_type="bar")
plt.title("CNT 电导率预测 - 特征重要性 (SHAP)", fontsize=14)
plt.tight_layout()
plt.savefig(figures_dir / "cnt_shap_feature_importance.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  [OK] Feature importance: {figures_dir / 'cnt_shap_feature_importance.png'}")

# 图 2: SHAP 依赖图 (每个特征)
print("  Generating dependence plots...")
for i, feature in enumerate(features):
    try:
        plt.figure(figsize=(8, 6), dpi=300)
        shap.dependence_plot(i, shap_values, X_test_scaled, feature_names=features, show=False, ax=plt.gca())
        plt.title(f"SHAP dependence - {feature}", fontsize=12)
        plt.tight_layout()
        plt.savefig(figures_dir / f"cnt_shap_dependence_{feature}.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"    - {feature}: OK")
    except Exception as e:
        print(f"    - {feature}: Skipped ({str(e)[:50]})")

# 图 3: SHAP 力图 (单个样本解释)
plt.figure(figsize=(12, 6), dpi=300)
shap.force_plot(
    explainer.expected_value,
    shap_values[0, :],
    X_test_scaled[0, :],
    feature_names=features,
    matplotlib=True,
    show=False
)
plt.title("单个样本 SHAP 解释", fontsize=12)
plt.tight_layout()
plt.savefig(figures_dir / "cnt_shap_force_plot.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  [OK] Force plot: {figures_dir / 'cnt_shap_force_plot.png'}")

# ============================================================================
# 6. 结果解读
# ============================================================================
print("\n" + "=" * 70)
print("[OK] SHAP 分析完成！")
print("=" * 70)

# 特征重要性排序
mean_abs_shap = np.mean(np.abs(shap_values), axis=0)
sorted_idx = np.argsort(mean_abs_shap)[::-1]

print("\nFeature importance ranking (based on mean |SHAP value|):")
for rank, idx in enumerate(sorted_idx, 1):
    feature = features[idx]
    importance = mean_abs_shap[idx]
    print(f"  {rank}. {feature}: {importance:.4f}")

print(f"\n图表已保存至：{figures_dir}")
print("\n下一步:")
print("  1. 解读 SHAP 分析结果")
print("  2. 提取物理洞见")
print("  3. 撰写论文讨论部分")
