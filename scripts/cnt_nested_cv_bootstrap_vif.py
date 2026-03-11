#!/usr/bin/env python3
# CNT Model - Nested CV + Bootstrap CI + VIF Test - Critic v2.0 Action

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/data")
MODEL_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/models")
REPORTS_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/reports")

print("=" * 80)
print("CNT Model - Nested CV + Bootstrap CI + VIF - Critic v2.0 Action")
print("=" * 80)

# Load Tier 1 data
print("\n[1] Loading Tier 1 data...")
tier1_file = DATA_DIR / "cnt_dataset_clean.csv"
data = pd.read_csv(tier1_file)
print(f"  Loaded: {len(data)} samples")

# Feature engineering (same as before)
print("\n[2] Feature engineering...")
data['aspect_ratio'] = data['length_um'] * 1000 / (data['diameter_nm'] + 1e-6)
data['volume'] = np.pi * (data['diameter_nm']/2)**2 * data['length_um']
data['surface_area'] = np.pi * data['diameter_nm'] * data['length_um']
data['surface_to_volume'] = data['surface_area'] / (data['volume'] + 1e-6)
data['percolation_param'] = data['length_um'] / data['diameter_nm']
data['network_density'] = 1 / (data['diameter_nm']**2)
data['contact_resistance'] = 1 / (data['length_um'] + 1e-6)
data['junction_count'] = data['length_um']**2
data['log_diameter'] = np.log10(data['diameter_nm'] + 1e-6)
data['log_length'] = np.log10(data['length_um'] + 1e-6)
data['log_aspect_ratio'] = np.log10(data['aspect_ratio'] + 1e-6)
data['log_volume'] = np.log10(data['volume'] + 1e-6)
data['log_conductivity'] = np.log10(data['conductivity_Sm'] + 1)

features = [
    'diameter_nm', 'length_um', 'aspect_ratio', 'volume', 'surface_area',
    'surface_to_volume', 'percolation_param', 'network_density',
    'contact_resistance', 'junction_count', 'log_diameter', 'log_length',
    'log_aspect_ratio', 'log_volume'
]

X = data[features].copy()
y = data['log_conductivity']

# Fill missing
for col in X.columns:
    if X[col].isnull().any():
        X[col].fillna(X[col].median(), inplace=True)

print(f"  Features: {len(features)}")
print(f"  Missing values: {X.isnull().sum().sum()}")

# VIF Test (Critic Requirement #1)
print("\n[3] VIF Test (Multicollinearity Check)...")
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data['Feature'] = features
vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(len(features))]
vif_data = vif_data.sort_values('VIF', ascending=False)

print("\n  VIF Results:")
print(vif_data.to_string(index=False))

high_vif = vif_data[vif_data['VIF'] > 5]
if len(high_vif) > 0:
    print(f"\n  [!] WARNING: {len(high_vif)} features with VIF > 5 (multicollinearity!)")
    print(f"      Features: {list(high_vif['Feature'])}")
else:
    print(f"\n  [OK] All VIF < 5 (no multicollinearity)")

# Save VIF results
vif_file = REPORTS_DIR / "cnt_vif_report.csv"
vif_data.to_csv(vif_file, index=False)
print(f"  Saved: {vif_file.name}")

# Nested Cross-Validation (Critic Requirement #2)
print("\n[4] Nested Cross-Validation...")
from sklearn.model_selection import KFold, GridSearchCV, cross_val_score
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

# Outer CV (5-Fold)
outer_cv = KFold(n_splits=5, shuffle=True, random_state=42)
# Inner CV (3-Fold for hyperparameter tuning)
inner_cv = KFold(n_splits=3, shuffle=True, random_state=42)

# Model pipeline
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model', ElasticNet(random_state=42, max_iter=10000))
])

# Hyperparameter grid
param_grid = {
    'model__alpha': [0.001, 0.01, 0.1, 1.0],
    'model__l1_ratio': [0.3, 0.5, 0.7]
}

# Grid search with inner CV
grid_search = GridSearchCV(pipe, param_grid, cv=inner_cv, scoring='r2', n_jobs=-1)

# Nested CV scores
nested_scores = []
nested_mae = []

print("\n  Running Nested 5x3-Fold CV...")
for fold, (train_idx, test_idx) in enumerate(outer_cv.split(X), 1):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    # Fit with inner CV for hyperparameter tuning
    grid_search.fit(X_train, y_train)
    
    # Predict on outer test set
    y_pred = grid_search.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    nested_scores.append(r2)
    nested_mae.append(mae)
    
    print(f"    Fold {fold}: R2 = {r2:.4f}, MAE = {mae:.4f}")

nested_r2_mean = np.mean(nested_scores)
nested_r2_std = np.std(nested_scores)
nested_r2_95ci = np.percentile(nested_scores, [2.5, 97.5])

nested_mae_mean = np.mean(nested_mae)
nested_mae_95ci = np.percentile(nested_mae, [2.5, 97.5])

print(f"\n  Nested CV Results:")
print(f"    R2: {nested_r2_mean:.4f} (+/- {nested_r2_std*2:.4f})")
print(f"    95% CI: [{nested_r2_95ci[0]:.4f}, {nested_r2_95ci[1]:.4f}]")
print(f"    MAE: {nested_mae_mean:.4f} (95% CI: [{nested_mae_95ci[0]:.4f}, {nested_mae_95ci[1]:.4f}])")

# Bootstrap Confidence Intervals (Critic Requirement #3)
print("\n[5] Bootstrap Confidence Intervals (1000 iterations)...")
from sklearn.utils import resample

n_bootstrap = 1000
bootstrap_r2 = []
bootstrap_mae = []

print(f"  Running {n_bootstrap} bootstrap iterations...")
for i in range(n_bootstrap):
    # Resample with replacement
    X_boot, y_boot = resample(X, y, n_samples=len(X), random_state=i)
    
    # Train model
    pipe.fit(X_boot, y_boot)
    
    # Predict on OOB samples
    oob_mask = ~X_boot.index.isin(X_boot.index)
    if oob_mask.sum() > 0:
        y_pred = pipe.predict(X_boot[oob_mask])
        r2 = r2_score(y_boot[oob_mask], y_pred)
        mae = mean_absolute_error(y_boot[oob_mask], y_pred)
        bootstrap_r2.append(r2)
        bootstrap_mae.append(mae)

bootstrap_r2_mean = np.mean(bootstrap_r2)
bootstrap_r2_95ci = np.percentile(bootstrap_r2, [2.5, 97.5])
bootstrap_mae_mean = np.mean(bootstrap_mae)
bootstrap_mae_95ci = np.percentile(bootstrap_mae, [2.5, 97.5])

print(f"\n  Bootstrap Results ({n_bootstrap} iterations):")
print(f"    R2: {bootstrap_r2_mean:.4f} (95% CI: [{bootstrap_r2_95ci[0]:.4f}, {bootstrap_r2_95ci[1]:.4f}])")
print(f"    MAE: {bootstrap_mae_mean:.4f} (95% CI: [{bootstrap_mae_95ci[0]:.4f}, {bootstrap_mae_95ci[1]:.4f}])")

# Power Analysis (Critic Requirement #4)
print("\n[6] Power Analysis...")
from statsmodels.stats.power import FTestPower

# Effect size (Cohen's f²)
r2 = nested_r2_mean
f2 = r2 / (1 - r2)  # Cohen's f²

# Power calculation
alpha = 0.05
n_samples = len(X)
n_features = len(features)
df_num = n_features
df_denom = n_samples - n_features - 1

power_analyzer = FTestPower()
statistical_power = power_analyzer.power(effect_size=f2, nobs=n_samples, alpha=alpha, df_num=df_num, df_denom=df_denom)

print(f"  Effect size (Cohen's f²): {f2:.4f}")
print(f"  Sample size: {n_samples}")
print(f"  Number of features: {n_features}")
print(f"  Statistical power: {statistical_power:.4f}")

if statistical_power >= 0.8:
    print(f"  [OK] Power >= 0.8 (adequate)")
else:
    print(f"  [!] WARNING: Power < 0.8 (need more samples)")

# Required sample size for power = 0.8
required_n = power_analyzer.solve_power(effect_size=f2, power=0.8, alpha=alpha, df_num=df_num)
print(f"  Required samples for power=0.8: {int(required_n)}")

# Train final model on all data
print("\n[7] Training final model on all data...")
pipe.fit(X, y)

# Save model
model_file = MODEL_DIR / "CNT_ElasticNet_nested_cv.pkl"
joblib.dump(pipe, model_file)
print(f"  Saved: {model_file.name}")

# Save all results
print("\n[8] Saving results...")
results = {
    'Metric': ['Nested_CV_R2', 'Nested_CV_R2_95CI_lower', 'Nested_CV_R2_95CI_upper',
               'Bootstrap_R2', 'Bootstrap_R2_95CI_lower', 'Bootstrap_R2_95CI_upper',
               'Statistical_Power', 'Cohen_f2', 'Required_Samples'],
    'Value': [nested_r2_mean, nested_r2_95ci[0], nested_r2_95ci[1],
              bootstrap_r2_mean, bootstrap_r2_95ci[0], bootstrap_r2_95ci[1],
              statistical_power, f2, required_n]
}
results_df = pd.DataFrame(results)
results_file = REPORTS_DIR / "cnt_nested_cv_bootstrap_results.csv"
results_df.to_csv(results_file, index=False)
print(f"  Saved: {results_file.name}")

# Final summary
print("\n" + "=" * 80)
print("CRITIC v2.0 COMPLIANCE REPORT")
print("=" * 80)
print(f"  ✓ Nested CV:          R2 = {nested_r2_mean:.4f} (95% CI: [{nested_r2_95ci[0]:.4f}, {nested_r2_95ci[1]:.4f}])")
print(f"  ✓ Bootstrap CI:       R2 = {bootstrap_r2_mean:.4f} (95% CI: [{bootstrap_r2_95ci[0]:.4f}, {bootstrap_r2_95ci[1]:.4f}])")
print(f"  ✓ VIF Test:           {'All VIF < 5 ✓' if len(high_vif) == 0 else f'{len(high_vif)} features VIF > 5 ✗'}")
print(f"  ✓ Power Analysis:     Power = {statistical_power:.4f} {'✓' if statistical_power >= 0.8 else '✗ (need more samples)'}")
print(f"\n  Critic v2.0 Score:    {'PASS ✓' if (statistical_power >= 0.8 and len(high_vif) == 0) else 'NEEDS IMPROVEMENT ✗'}")

print("\n" + "=" * 80)
print("Complete!")
print("=" * 80)
