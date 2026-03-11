#!/usr/bin/env python3
# CNT Model - Fix Multicollinearity + Nested CV - Critic v2.0 Action

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/data")
MODEL_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/models")
REPORTS_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/reports")

print("=" * 80)
print("CNT Model - Fix Multicollinearity + Nested CV - Critic v2.0 Action")
print("=" * 80)

# Load Tier 1 data
print("\n[1] Loading Tier 1 data...")
tier1_file = DATA_DIR / "cnt_dataset_clean.csv"
data = pd.read_csv(tier1_file)
print(f"  Loaded: {len(data)} samples")

# Feature engineering - ONLY non-collinear features!
print("\n[2] Feature engineering (avoiding multicollinearity)...")

# Create features
data['aspect_ratio'] = data['length_um'] * 1000 / (data['diameter_nm'] + 1e-6)
data['log_diameter'] = np.log10(data['diameter_nm'] + 1e-6)

# Keep only these (physically meaningful, low collinearity):
features = [
    'diameter_nm',      # 直径 (原始)
    'length_um',        # 长度 (原始)
    'aspect_ratio',     # 长径比 (物理意义)
    'log_diameter',     # 对数直径 (处理宽范围)
]

# Add ONE composite feature (not derived from above)
if 'layers' in data.columns:
    data['layers'].fillna(data['layers'].median(), inplace=True)
    features.append('layers')
    print(f"  Added: layers")

print(f"  Selected features: {len(features)}")
print(f"  {features}")

# Create target
data['log_conductivity'] = np.log10(data['conductivity_Sm'] + 1)

X = data[features].copy()
y = data['log_conductivity']

# Fill missing
for col in X.columns:
    if X[col].isnull().any():
        X[col].fillna(X[col].median(), inplace=True)

print(f"  Missing values: {X.isnull().sum().sum()}")

# VIF Test
print("\n[3] VIF Test...")
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data['Feature'] = features
vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(len(features))]
vif_data = vif_data.sort_values('VIF', ascending=False)

print("\n  VIF Results:")
print(vif_data.to_string(index=False))

high_vif = vif_data[vif_data['VIF'] > 5]
if len(high_vif) > 0:
    print(f"\n  [!] WARNING: {len(high_vif)} features with VIF > 5")
else:
    print(f"\n  [OK] All VIF < 5 (no multicollinearity!)")

# Save VIF results
vif_file = REPORTS_DIR / "cnt_vif_fixed_report.csv"
vif_data.to_csv(vif_file, index=False)
print(f"  Saved: {vif_file.name}")

# Nested Cross-Validation
print("\n[4] Nested Cross-Validation (5x3-Fold)...")
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

outer_cv = KFold(n_splits=5, shuffle=True, random_state=42)
inner_cv = KFold(n_splits=3, shuffle=True, random_state=42)

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model', ElasticNet(random_state=42, max_iter=10000))
])

param_grid = {
    'model__alpha': [0.001, 0.01, 0.1, 1.0],
    'model__l1_ratio': [0.3, 0.5, 0.7]
}

grid_search = GridSearchCV(pipe, param_grid, cv=inner_cv, scoring='r2', n_jobs=1)

nested_scores = []
nested_mae = []

print("\n  Running Nested CV...")
for fold, (train_idx, test_idx) in enumerate(outer_cv.split(X), 1):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    grid_search.fit(X_train, y_train)
    y_pred = grid_search.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    nested_scores.append(r2)
    nested_mae.append(mae)
    
    print(f"    Fold {fold}: R2 = {r2:.4f}, MAE = {mae:.4f}")

nested_r2_mean = np.mean(nested_scores)
nested_r2_std = np.std(nested_scores)
nested_r2_95ci = np.percentile(nested_scores, [2.5, 97.5])

print(f"\n  Nested CV Results:")
print(f"    R2: {nested_r2_mean:.4f} (+/- {nested_r2_std*2:.4f})")
print(f"    95% CI: [{nested_r2_95ci[0]:.4f}, {nested_r2_95ci[1]:.4f}]")

# Bootstrap CI
print("\n[5] Bootstrap CI (500 iterations)...")
from sklearn.utils import resample

n_bootstrap = 500
bootstrap_r2 = []

print(f"  Running {n_bootstrap} bootstrap iterations...")
for i in range(n_bootstrap):
    X_boot, y_boot = resample(X, y, n_samples=len(X), random_state=i)
    pipe.fit(X_boot, y_boot)
    y_pred = pipe.predict(X_boot)
    r2 = r2_score(y_boot, y_pred)
    bootstrap_r2.append(r2)

bootstrap_r2_mean = np.mean(bootstrap_r2)
bootstrap_r2_95ci = np.percentile(bootstrap_r2, [2.5, 97.5])

print(f"\n  Bootstrap Results:")
print(f"    R2: {bootstrap_r2_mean:.4f} (95% CI: [{bootstrap_r2_95ci[0]:.4f}, {bootstrap_r2_95ci[1]:.4f}])")

# Power Analysis
print("\n[6] Power Analysis...")
from statsmodels.stats.power import FTestPower

r2 = nested_r2_mean
f2 = r2 / (1 - r2)
n_samples = len(X)
n_features = len(features)

power_analyzer = FTestPower()
statistical_power = power_analyzer.power(
    effect_size=f2, nobs=n_samples, alpha=0.05,
    df_num=n_features, df_denom=n_samples - n_features - 1
)

print(f"  Effect size (Cohen's f²): {f2:.4f}")
print(f"  Sample size: {n_samples}")
print(f"  Statistical power: {statistical_power:.4f}")
print(f"  {'[OK] Power >= 0.8' if statistical_power >= 0.8 else '[!] Power < 0.8'}")

# Train final model
print("\n[7] Training final model...")
pipe.fit(X, y)

model_file = MODEL_DIR / "CNT_ElasticNet_fixed_vif.pkl"
joblib.dump(pipe, model_file)
print(f"  Saved: {model_file.name}")

# Save results
print("\n[8] Saving results...")
results = {
    'Metric': ['Nested_CV_R2', 'Nested_CV_R2_95CI_lower', 'Nested_CV_R2_95CI_upper',
               'Bootstrap_R2', 'Bootstrap_R2_95CI_lower', 'Bootstrap_R2_95CI_upper',
               'VIF_All_Pass', 'Statistical_Power', 'Cohen_f2'],
    'Value': [nested_r2_mean, nested_r2_95ci[0], nested_r2_95ci[1],
              bootstrap_r2_mean, bootstrap_r2_95ci[0], bootstrap_r2_95ci[1],
              1 if len(high_vif) == 0 else 0, statistical_power, f2]
}
results_df = pd.DataFrame(results)
results_file = REPORTS_DIR / "cnt_fixed_nested_cv_results.csv"
results_df.to_csv(results_file, index=False)
print(f"  Saved: {results_file.name}")

# Final report
print("\n" + "=" * 80)
print("CRITIC v2.0 COMPLIANCE REPORT - FIXED")
print("=" * 80)
print(f"  Features: {len(features)} (reduced from 14)")
print(f"  VIF Test: {'✓ PASS (all VIF < 5)' if len(high_vif) == 0 else '✗ FAIL'}")
print(f"  Nested CV: R2 = {nested_r2_mean:.4f} (95% CI: [{nested_r2_95ci[0]:.4f}, {nested_r2_95ci[1]:.4f}])")
print(f"  Bootstrap: R2 = {bootstrap_r2_mean:.4f} (95% CI: [{bootstrap_r2_95ci[0]:.4f}, {bootstrap_r2_95ci[1]:.4f}])")
print(f"  Power: {statistical_power:.4f} {'✓' if statistical_power >= 0.8 else '✗'}")
print(f"\n  OVERALL: {'✓ PASS' if (len(high_vif) == 0 and statistical_power >= 0.8) else '✗ NEEDS WORK'}")
print("=" * 80)
