#!/usr/bin/env python3
# CNT Outlier Removal & Model Retraining - Critic Action

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/data")
MODEL_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/models")

print("=" * 60)
print("CNT Outlier Removal & Retraining - Critic Action")
print("=" * 60)

# Load quality filtered data
print("\n[1] Loading quality filtered data...")
data = pd.read_csv(DATA_DIR / "cnt_dataset_quality_filtered.csv")
print(f"  Loaded: {len(data)} samples")

# IQR-based outlier removal
print("\n[2] Removing outliers (IQR method)...")
cols_to_check = ['conductivity_Sm', 'diameter_nm', 'length_um']

outlier_mask = pd.Series([False] * len(data))

for col in cols_to_check:
    if col in data.columns:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        col_outliers = ((data[col] < Q1 - 1.5*IQR) | 
                       (data[col] > Q3 + 1.5*IQR))
        outlier_mask |= col_outliers
        print(f"  {col}: {col_outliers.sum()} outliers removed")

clean_data = data[~outlier_mask].copy()
print(f"\n  Original: {len(data)} samples")
print(f"  Outliers removed: {outlier_mask.sum()} samples")
print(f"  Clean data: {len(clean_data)} samples ({len(clean_data)/len(data)*100:.1f}% retained)")

# Save clean data
clean_file = DATA_DIR / "cnt_dataset_clean.csv"
clean_data.to_csv(clean_file, index=False, encoding='utf-8-sig')
print(f"\n  Saved: {clean_file.name}")

# Train/test split on clean data
print("\n[3] Creating train/test sets from clean data...")
from sklearn.model_selection import train_test_split

if len(clean_data) >= 30:
    train_data, test_data = train_test_split(
        clean_data, 
        test_size=int(min(30, len(clean_data)*0.1)),
        random_state=42
    )
    
    train_file = DATA_DIR / "cnt_train_clean.csv"
    test_file = DATA_DIR / "cnt_test_clean.csv"
    
    train_data.to_csv(train_file, index=False, encoding='utf-8-sig')
    test_data.to_csv(test_file, index=False, encoding='utf-8-sig')
    
    print(f"  Train set: {len(train_data)} samples")
    print(f"  Test set: {len(test_data)} samples")
else:
    print(f"  [ERROR] Not enough samples: {len(clean_data)} < 30")
    exit(1)

# Feature preparation
print("\n[4] Preparing features...")
feature_cols = ['diameter_nm', 'length_um', 'layers', 'cvd_temperature_C']
target_col = 'conductivity_Sm'

# Add derived features
train_data['aspect_ratio'] = train_data['length_um'] * 1000 / (train_data['diameter_nm'] + 1e-6)
test_data['aspect_ratio'] = test_data['length_um'] * 1000 / (test_data['diameter_nm'] + 1e-6)

feature_cols.append('aspect_ratio')

# Handle missing values
for col in feature_cols:
    if train_data[col].isnull().any():
        median_val = train_data[col].median()
        train_data[col].fillna(median_val, inplace=True)
        test_data[col].fillna(median_val, inplace=True)
        print(f"  Filled missing {col} with median: {median_val:.2f}")

X_train = train_data[feature_cols]
y_train = train_data[target_col]
X_test = test_data[feature_cols]
y_test = test_data[target_col]

print(f"\n  Features: {feature_cols}")
print(f"  X_train: {X_train.shape}, X_test: {X_test.shape}")

# Model training
print("\n[5] Training models...")
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import joblib

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler
scaler_file = MODEL_DIR / "CNT_scaler_clean.pkl"
joblib.dump(scaler, scaler_file)
print(f"  Saved scaler: {scaler_file.name}")

# Train multiple models
models = {
    'ElasticNet': ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42, max_iter=10000),
    'GradientBoosting': GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42),
    'RandomForest': RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42),
    'GP_RBF': GaussianProcessRegressor(kernel=RBF(length_scale=1.0), random_state=42),
    'GP_Matern': GaussianProcessRegressor(kernel=Matern(nu=2.5), random_state=42)
}

results = []

for name, model in models.items():
    print(f"\n  Training {name}...")
    model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    
    # Metrics
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    
    print(f"    Train R2: {train_r2:.4f}, Test R2: {test_r2:.4f}")
    print(f"    Train MAE: {train_mae:.4e}, Test MAE: {test_mae:.4e}")
    
    # Save best model
    if test_r2 > 0.5:  # Only save if test R² is reasonable
        model_file = MODEL_DIR / f"CNT_{name}_clean.pkl"
        joblib.dump(model, model_file)
        print(f"    Saved: {model_file.name}")
    
    results.append({
        'Model': name,
        'Train_R2': train_r2,
        'Test_R2': test_r2,
        'Train_MAE': train_mae,
        'Test_MAE': test_mae
    })

# Results summary
print("\n" + "=" * 60)
print("Results Summary")
print("=" * 60)

results_df = pd.DataFrame(results)
results_df = results_df.sort_values('Test_R2', ascending=False)
print(results_df.to_string(index=False))

# Best model
best_model = results_df.iloc[0]
print(f"\n[OK] Best model: {best_model['Model']}")
print(f"     Test R2: {best_model['Test_R2']:.4f}")
print(f"     Test MAE: {best_model['Test_MAE']:.4e}")

# Compare with previous
print("\n" + "=" * 60)
print("Comparison with Previous (274 samples, no outlier removal)")
print("=" * 60)
print("  Previous R2: 0.799 (training set)")
print(f"  New Test R2: {best_model['Test_R2']:.4f} (test set)")
print(f"  Gap: {0.799 - best_model['Test_R2']:.4f}")

if best_model['Test_R2'] < 0.6:
    print("\n[!] WARNING: Test R2 dropped significantly!")
    print("    Previous R2=0.799 may have been overfitting outliers.")
elif best_model['Test_R2'] < 0.75:
    print("\n[!] Test R2 below target (0.75)")
    print("    Need more/better data.")
else:
    print("\n[OK] Test R2 meets target (>0.75)")

print("\n" + "=" * 60)
print("Complete!")
print("=" * 60)

# Save results
results_file = DATA_DIR / "cnt_model_comparison_clean.csv"
results_df.to_csv(results_file, index=False)
print(f"\nSaved results: {results_file.name}")
