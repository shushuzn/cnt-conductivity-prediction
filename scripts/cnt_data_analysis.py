#!/usr/bin/env python3
# CNT Data Analysis - Critic Action Execution

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/data")

print("=" * 60)
print("CNT Data Analysis - Critic Action")
print("=" * 60)

# Load datasets
print("\n[1] Loading datasets...")
v4_real = pd.read_csv(DATA_DIR / "cnt_dataset_v4_real.csv")
v5_300plus = pd.read_csv(DATA_DIR / "cnt_dataset_v5_300plus.csv")

print(f"  cnt_dataset_v4_real: {len(v4_real)} samples")
print(f"  cnt_dataset_v5_300plus: {len(v5_300plus)} samples")

# Missing value analysis
print("\n[2] Missing value analysis...")
missing = v4_real.isnull().sum().sort_values(ascending=False)
missing_pct = (missing / len(v4_real) * 100).round(2)
missing_df = pd.DataFrame({'Missing': missing, 'Percent%': missing_pct})
print(missing_df[missing_df['Missing'] > 0].head(10))

# Quality filtering
print("\n[3] Quality filtering...")
critical_cols = ['conductivity_Sm', 'diameter_nm', 'length_um']
quality_mask = v4_real[critical_cols].notnull().all(axis=1)
quality_data = v4_real[quality_mask].copy()

print(f"  Original: {len(v4_real)} samples")
print(f"  Quality filtered: {len(quality_data)} samples")
print(f"  Retained: {len(quality_data)/len(v4_real)*100:.1f}%")

# Save filtered data
output_file = DATA_DIR / "cnt_dataset_quality_filtered.csv"
quality_data.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n  Saved: {output_file.name} ({len(quality_data)} samples)")

# Outlier detection
print("\n[4] Outlier detection (IQR method)...")
outlier_count = 0

for col in ['conductivity_Sm', 'diameter_nm', 'length_um']:
    if col in quality_data.columns:
        Q1 = quality_data[col].quantile(0.25)
        Q3 = quality_data[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((quality_data[col] < Q1 - 1.5*IQR) | 
                   (quality_data[col] > Q3 + 1.5*IQR))
        outlier_count += outliers.sum()
        print(f"  {col}: {outliers.sum()} outliers")

print(f"\n  Total outliers: {outlier_count}")

# Train/test split
print("\n[5] Creating train/test sets...")
from sklearn.model_selection import train_test_split

if len(quality_data) >= 30:
    train_data, test_data = train_test_split(
        quality_data, 
        test_size=int(min(30, len(quality_data)*0.1)),
        random_state=42
    )
    
    train_file = DATA_DIR / "cnt_train_set.csv"
    test_file = DATA_DIR / "cnt_test_set.csv"
    
    train_data.to_csv(train_file, index=False, encoding='utf-8-sig')
    test_data.to_csv(test_file, index=False, encoding='utf-8-sig')
    
    print(f"  Train set: {len(train_data)} samples -> {train_file.name}")
    print(f"  Test set: {len(test_data)} samples -> {test_file.name}")
else:
    print(f"  Not enough samples ({len(quality_data)} < 30)")

# Feature list for SHAP
print("\n[6] SHAP analysis preparation...")
print("  Feature columns:")
feature_cols = [col for col in quality_data.columns 
                if quality_data[col].dtype in ['int64', 'float64'] 
                and col not in ['sample_id', 'uncertainty']]
print(f"  {feature_cols[:10]}...")

print("\n" + "=" * 60)
print("Analysis Complete!")
print("=" * 60)

# Summary
print("\nSummary:")
print(f"  Original data: {len(v4_real)} samples")
print(f"  Quality data: {len(quality_data)} samples")
print(f"  Outliers: {outlier_count}")
if len(quality_data) >= 30:
    print(f"  Train set: {len(train_data)} samples")
    print(f"  Test set: {len(test_data)} samples")

print("\nRecommendations:")
if len(quality_data) < 300:
    print(f"  [!] Need more samples: {len(quality_data)} < 300")
else:
    print(f"  [OK] Sample target reached: {len(quality_data)} >= 300")

if outlier_count > len(quality_data) * 0.05:
    print(f"  [!] High outlier ratio: {outlier_count/len(quality_data)*100:.1f}% > 5%")
else:
    print(f"  [OK] Outlier ratio acceptable: {outlier_count/len(quality_data)*100:.1f}%")
