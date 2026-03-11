#!/usr/bin/env python3
# CNT 5-Fold CV & Feature Engineering - Critic Action

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/data")
MODEL_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/models")

print("=" * 60)
print("CNT 5-Fold CV & Feature Engineering - Critic Action")
print("=" * 60)

# Load clean data
print("\n[1] Loading clean data...")
data = pd.read_csv(DATA_DIR / "cnt_dataset_clean.csv")
print(f"  Loaded: {len(data)} samples")

# Feature engineering
print("\n[2] Feature engineering...")

# Original features
data['aspect_ratio'] = data['length_um'] * 1000 / (data['diameter_nm'] + 1e-6)
data['volume_fraction'] = (data['diameter_nm'] ** 2) * data['length_um']
data['surface_area'] = data['diameter_nm'] * data['length_um']
data['log_conductivity'] = np.log10(data['conductivity_Sm'] + 1)

# Fill missing values
if 'cvd_temperature_C' in data.columns:
    median_temp = data['cvd_temperature_C'].median()
    data['cvd_temperature_C'].fillna(median_temp, inplace=True)
    data['has_catalyst'] = (~data['catalyst'].isnull()).astype(int)
    data['has_carbon_source'] = (~data['carbon_source'].isnull()).astype(int)
else:
    data['has_catalyst'] = 0
    data['has_carbon_source'] = 0

# Feature list
feature_cols = [
    'diameter_nm', 'length_um', 'layers', 
    'cvd_temperature_C', 'aspect_ratio', 
    'volume_fraction', 'surface_area',
    'has_catalyst', 'has_carbon_source'
]

# Remove features with too many missing values
available_features = [f for f in feature_cols if f in data.columns]
print(f"  Available features: {len(available_features)}")
print(f"  {available_features}")

# Prepare data
X = data[available_features].copy()
y = data['conductivity_Sm']
y_log = data['log_conductivity']

# Fill remaining missing values
for col in X.columns:
    if X[col].isnull().any():
        median_val = X[col].median()
        X[col].fillna(median_val, inplace=True)

print(f"  Final feature matrix: {X.shape}")

# 5-Fold Cross-Validation
print("\n[3] 5-Fold Cross-Validation...")
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import ElasticNet, Ridge, Lasso
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

# Models to test
models = {
    'ElasticNet': Pipeline([
        ('scaler', StandardScaler()),
        ('model', ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=10000, random_state=42))
    ]),
    'Ridge': Pipeline([
        ('scaler', StandardScaler()),
        ('model', Ridge(alpha=1.0, random_state=42))
    ]),
    'Lasso': Pipeline([
        ('scaler', StandardScaler()),
        ('model', Lasso(alpha=0.01, max_iter=10000, random_state=42))
    ]),
    'GradientBoosting': GradientBoostingRegressor(
        n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42
    ),
    'RandomForest': RandomForestRegressor(
        n_estimators=100, max_depth=5, random_state=42
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
    print(f"    MAE: {-scores_mae.mean():.4e} (+/- {-scores_mae.std()*2:.4e})")
    
    # CV on log target (often better for conductivity)
    scores_r2_log = cross_val_score(model, X, y_log, cv=cv, scoring='r2')
    
    print(f"    R2 (log): {scores_r2_log.mean():.4f} (+/- {scores_r2_log.std()*2:.4f})")
    
    cv_results.append({
        'Model': name,
        'R2_mean': scores_r2.mean(),
        'R2_std': scores_r2.std(),
        'R2_log_mean': scores_r2_log.mean(),
        'R2_log_std': scores_r2_log.std(),
        'MAE_mean': -scores_mae.mean(),
        'MAE_std': -scores_mae.std()
    })

# Results summary
print("\n" + "=" * 60)
print("5-Fold CV Results Summary")
print("=" * 60)

results_df = pd.DataFrame(cv_results)
results_df = results_df.sort_values('R2_mean', ascending=False)
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

model.fit(X, y)

# Save model
model_file = MODEL_DIR / f"CNT_{best_model_name}_5foldCV.pkl"
joblib.dump(model, model_file)
print(f"  Saved: {model_file.name}")

# Feature importance (if available)
if hasattr(model, 'named_steps') and 'model' in model.named_steps:
    final_model = model.named_steps['model']
    if hasattr(final_model, 'feature_importances_'):
        print("\n[5] Feature importance:")
        importance = final_model.feature_importances_
        for feat, imp in sorted(zip(available_features, importance), key=lambda x: x[1], reverse=True):
            print(f"  {feat}: {imp:.4f}")

# Comparison
print("\n" + "=" * 60)
print("Performance Comparison")
print("=" * 60)
print("  Before outlier removal: R2=0.799 (overfitted)")
print(f"  After outlier removal:  R2=0.496 (test set)")
print(f"  5-Fold CV (clean data): R2={best_model['R2_mean']:.4f} (+/- {best_model['R2_std']*2:.4f})")
print(f"  5-Fold CV (log target): R2={best_model['R2_log_mean']:.4f} (+/- {best_model['R2_log_std']*2:.4f})")

if best_model['R2_mean'] < 0.6:
    print("\n[!] CV R2 < 0.6 - Need more/better data")
elif best_model['R2_mean'] < 0.75:
    print("\n[!] CV R2 < 0.75 - Below original target")
    print("    Recommendation: Use log-transformed target")
else:
    print("\n[OK] CV R2 >= 0.75 - Target met!")

# Save results
print("\n" + "=" * 60)
print("Complete!")
print("=" * 60)

results_file = DATA_DIR / "cnt_5fold_cv_results.csv"
results_df.to_csv(results_file, index=False)
print(f"\nSaved results: {results_file.name}")

# Data quality report
print("\n" + "=" * 60)
print("Data Quality Report")
print("=" * 60)
print(f"  Total samples: {len(data)}")
print(f"  Features used: {len(available_features)}")
print(f"  Missing values: {data[available_features].isnull().sum().sum()}")
print(f"  Target range: [{y.min():.2e}, {y.max():.2e}] S/m")
print(f"  Target median: {y.median():.2e} S/m")
