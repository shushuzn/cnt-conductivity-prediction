#!/usr/bin/env python3
# CNT VIF Pre-analysis Script (Day 3)
# Collect 30 pilot samples and check VIF < 3

import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.stats.outliers_influence import variance_inflation_factor

DATA_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/data")

print("=" * 80)
print("CNT VIF Pre-analysis (Day 3)")
print("=" * 80)

# Load existing clean data as pilot samples
print("\n[1] Loading pilot samples (target: 30 samples)...")
tier1_file = DATA_DIR / "cnt_dataset_clean.csv"

if not tier1_file.exists():
    print(f"  [ERROR] File not found: {tier1_file}")
    exit(1)

data = pd.read_csv(tier1_file)
pilot_data = data.head(30).copy()

print(f"  Loaded: {len(pilot_data)} pilot samples")

# Feature engineering
print("\n[2] Feature engineering...")
features = ['diameter_nm', 'length_um']

if 'layers' in pilot_data.columns:
    pilot_data['layers'].fillna(pilot_data['layers'].median(), inplace=True)
    features.append('layers')

print(f"  Features: {features}")

# VIF calculation
print("\n[3] VIF calculation...")
vif_data = pd.DataFrame()
vif_data['Feature'] = features
vif_data['VIF'] = [variance_inflation_factor(pilot_data[features].values, i) for i in range(len(features))]
vif_data = vif_data.sort_values('VIF', ascending=False)

print("\n  VIF Results:")
print(vif_data.to_string(index=False))

# Decision
print("\n[4] Decision...")
max_vif = vif_data['VIF'].max()

if max_vif < 3:
    print(f"  [OK] Max VIF={max_vif:.2f} < 3")
    print(f"  **Decision: Can proceed with formal data collection**")
else:
    print(f"  [!] Max VIF={max_vif:.2f} >= 3")
    print(f"  **Decision: Cannot proceed, need to adjust features**")
    
    # Suggest feature removal
    worst_feature = vif_data.iloc[0]['Feature']
    print(f"  Suggestion: Remove '{worst_feature}' (highest VIF)")

# Save results
print("\n[5] Saving results...")
vif_file = DATA_DIR / "cnt_vif_preanalysis.csv"
vif_data.to_csv(vif_file, index=False)
print(f"  Saved: {vif_file.name}")

print("\n" + "=" * 80)
print("VIF Pre-analysis Complete!")
print("=" * 80)
