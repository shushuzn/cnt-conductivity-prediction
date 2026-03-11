#!/usr/bin/env python3
# CNT Model Retraining with 511 Samples - Critic Action

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/data")
MODEL_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/models")

print("=" * 60)
print("CNT Model Retraining with 511 Samples - Critic Action")
print("=" * 60)

# Load combined data
print("\n[1] Loading combined data...")
combined_file = DATA_DIR / "cnt_dataset_combined.csv"

if not combined_file.exists():
    print(f"  [ERROR] File not found: {combined_file}")
    exit(1)

data = pd.read_csv(combined_file)
print(f"  Loaded: {len(data)} samples")
print(f"  Columns: {list(data.columns)}")

# Feature engineering
print("\n[2] Feature engineering...")

# Original features
features = ['diameter_nm', 'length_um']

# Add derived features
data['aspect_ratio'] = data['length_um'] * 1000 / (data['diameter_nm'] + 1e-6)
features.append('aspect_ratio')

data['log_diameter'] = np.log10(data['diameter_nm'] + 1e-6)
features.append('log_diameter')

data['log_length'] = np.log10(data['length_um'] + 1e-6)
features.append('log_length')

data['volume'] = (data['diameter_nm'] ** 2) * data['length_um']
features.append('volume')

data['surface_area'] = data['diameter_nm'] * data['length_um']
features.append('surface_area')

# Add more features if available
if 'density_gcm3' in data.columns:
    data['density_gcm3'].fillna(data['density_gcm3'].median(), inplace=True)
    features.append('density_gcm3')

if 'tensile_strength_MPa' in data.columns:
    data['tensile_strength_MPa'].fillna(data['tensile_strength_MPa'].median(), inplace=True)
    features.append('tensile_strength_MPa')

if 'youngs_modulus_GPa' in data.columns:
    data['youngs_modulus_GPa'].fillna(data['youngs_modulus_GPa'].median(), inplace=True)
    features.append('youngs_modulus_GPa')

# Target variable (log-transformed)
data['log_conductivity'] = np.log10(data['conductivity_Sm'] + 1)

print(f"  Features: {len(features)}")
print(f"  {features}")

# Prepare data
X = data[features].copy()
y = data['conductivity_Sm']
y_log = data['log_conductivity']

# Fill missing values
for col in X.columns:
    if X[col].isnull().any():
        median_val = X[col].median()
        X[col].fillna(median_val, inplace=True)

print(f"  Final feature matrix: {X.shape}")
print(f"  Missing values: {X.isnull().sum().sum()}")

# 5-Fold Cross-Validation
print("\n[3] 5-Fold Cross-Validation...")
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import ElasticNet, Ridge, Lasso
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

# Models to test
models = {
    'ElasticNet': Pipeline([
        ('scaler', StandardScaler()),
        ('model', ElasticNet(alpha=0.01, l1_ratio=0.5, max_iter=10000, random_state=42))
    ]),
    'Ridge': Pipeline([
        ('scaler', StandardScaler()),
        ('model', Ridge(alpha=1.0, random_state=42))
    ]),
    'Lasso': Pipeline([
        ('scaler', StandardScaler()),
        ('model', Lasso(alpha=0.001, max_iter=10000, random_state=42))
    ]),
    'GradientBoosting': GradientBoostingRegressor(
        n_estimators=200, max_depth=4, learning_rate=0.05, random_state=42
    ),
    'RandomForest': RandomForestRegressor(
        n_estimators=200, max_depth=6, random_state=42
    )
}

cv = KFold(n_splits=5, shuffle=True, random_state=42)

cv_results = []

for name, model in models.items():
    print(f"\n  {name}:")
    
    # CV on original target
    scores_r2 = cross_val_score(model, X, y, cv=cv, scoring='r2')
    scores_mae = cross_val_score(model, X, y, cv=cv, scoring='neg_mean_absolute_error')
    
    print(f"    R2: {scores_r2.mean():.4f} (+/- {scores_r2.std()*2:.4f})")
    print(f"    MAE: {-scores_mae.mean():.4e}")
    
    # CV on log target
    scores_r2_log = cross_val_score(model, X, y_log, cv=cv, scoring='r2')
    
    print(f"    R2 (log): {scores_r2_log.mean():.4f} (+/- {scores_r2_log.std()*2:.4f})")
    
    cv_results.append({
        'Model': name,
        'R2_mean': scores_r2.mean(),
        'R2_std': scores_r2.std(),
        'R2_log_mean': scores_r2_log.mean(),
        'R2_log_std': scores_r2_log.std(),
        'MAE_mean': -scores_mae.mean()
    })

# Results summary
print("\n" + "=" * 60)
print("5-Fold CV Results Summary (511 samples)")
print("=" * 60)

results_df = pd.DataFrame(cv_results)
results_df = results_df.sort_values('R2_log_mean', ascending=False)
print(results_df[['Model', 'R2_mean', 'R2_std', 'R2_log_mean']].to_string(index=False))

# Best model
best_model = results_df.iloc[0]
print(f"\n[OK] Best model: {best_model['Model']}")
print(f"     CV R2: {best_model['R2_mean']:.4f} (+/- {best_model['R2_std']*2:.4f})")
print(f"     CV R2 (log): {best_model['R2_log_mean']:.4f} (+/- {best_model['R2_log_std']*2:.4f})")

# Train final model on all data
print("\n[4] Training final model on all data...")
best_model_name = best_model['Model']
model = models[best_model_name]

model.fit(X, y_log)

# Save model
model_file = MODEL_DIR / f"CNT_{best_model_name}_511samples.pkl"
joblib.dump(model, model_file)
print(f"  Saved: {model_file.name}")

# Feature importance
if hasattr(model, 'named_steps') and 'model' in model.named_steps:
    final_model = model.named_steps['model']
    if hasattr(final_model, 'coef_'):
        print("\n[5] Feature coefficients (linear model):")
        for feat, coef in sorted(zip(features, final_model.coef_), key=lambda x: abs(x[1]), reverse=True):
            print(f"  {feat}: {coef:.4f}")

# Comparison
print("\n" + "=" * 60)
print("Performance Comparison")
print("=" * 60)
print("  Before (194 samples):  CV R2 = 0.47-0.63")
print(f"  After (511 samples):   CV R2 = {best_model['R2_log_mean']:.4f} (+/- {best_model['R2_log_std']*2:.4f})")

if best_model['R2_log_mean'] >= 0.75:
    print("\n[OK] CV R2 >= 0.75 - Original target reached! ✓")
elif best_model['R2_log_mean'] >= 0.60:
    print("\n[OK] CV R2 >= 0.60 - Revised target reached! ✓")
else:
    print(f"\n[!] CV R2 < 0.60 - Need more improvements")

# Save results
print("\n" + "=" * 60)
print("Complete!")
print("=" * 60)

results_file = DATA_DIR / "cnt_511_samples_cv_results.csv"
results_df.to_csv(results_file, index=False)
print(f"\nSaved results: {results_file.name}")

# Data quality report
print("\n" + "=" * 60)
print("Data Quality Report")
print("=" * 60)
print(f"  Total samples: {len(data)}")
print(f"  Features used: {len(features)}")
print(f"  Target range: [{y.min():.2e}, {y.max():.2e}] S/m")
print(f"  Target median: {y.median():.2e} S/m")
print(f"  Log target range: [{y_log.min():.2f}, {y_log.max():.2f}]")
