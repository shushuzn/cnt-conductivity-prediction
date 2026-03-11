#!/usr/bin/env python3
# Extract CNT Data from Meta-Analysis Database

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

LITERATURE_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/literature/pdfs/supp-data")
DATA_DIR = Path("D:/OpenClaw/workspace/06-research-研究/领域研究/cnt-research/data")

print("=" * 60)
print("Extract CNT Data from Meta-Analysis Database")
print("=" * 60)

# Load meta-analysis database
print("\n[1] Loading meta-analysis database...")
meta_db_file = LITERATURE_DIR / "meta-analysis-2021-database.csv"

meta_db = pd.read_csv(meta_db_file)
print(f"  Loaded: {len(meta_db)} rows")
print(f"  Columns: {len(meta_db.columns)}")

# Show relevant columns
print("\n  Relevant columns:")
for col in meta_db.columns:
    col_lower = str(col).lower()
    if any(k in col_lower for k in ['conductivity', 'diameter', 'length', 'layer', 'method', 'temp']):
        print(f"    - {col}")

# Extract key parameters
print("\n[2] Extracting parameters...")

# Map to standard names
extracted = pd.DataFrame()

# Conductivity (MSm-1 -> S/m)
if 'Conductivity (MSm-1)' in meta_db.columns:
    extracted['conductivity_Sm'] = pd.to_numeric(meta_db['Conductivity (MSm-1)'], errors='coerce') * 1e6
    print(f"  Conductivity: {extracted['conductivity_Sm'].notna().sum()} samples")

# CNT Diameter
if 'CNT Diameter (nm)' in meta_db.columns:
    extracted['diameter_nm'] = pd.to_numeric(meta_db['CNT Diameter (nm)'], errors='coerce')
    print(f"  Diameter: {extracted['diameter_nm'].notna().sum()} samples")

# Length (check for length column)
length_cols = [col for col in meta_db.columns if 'length' in str(col).lower()]
if length_cols:
    print(f"  Length columns found: {length_cols}")
    extracted['length_um'] = pd.to_numeric(meta_db[length_cols[0]], errors='coerce')
    print(f"  Length: {extracted['length_um'].notna().sum()} samples")

# Density (can be used as proxy for some properties)
if 'Density (g cm-3)' in meta_db.columns:
    extracted['density_gcm3'] = pd.to_numeric(meta_db['Density (g cm-3)'], errors='coerce')
    print(f"  Density: {extracted['density_gcm3'].notna().sum()} samples")

# Tensile Strength
if "Tensile Strength (MPa)" in meta_db.columns:
    extracted['tensile_strength_MPa'] = pd.to_numeric(meta_db["Tensile Strength (MPa)"], errors='coerce')
    print(f"  Tensile Strength: {extracted['tensile_strength_MPa'].notna().sum()} samples")

# Young's Modulus
if "Young's Modulus (GPa)" in meta_db.columns:
    extracted['youngs_modulus_GPa'] = pd.to_numeric(meta_db["Young's Modulus (GPa)"], errors='coerce')
    print(f"  Young's Modulus: {extracted['youngs_modulus_GPa'].notna().sum()} samples")

# Quality filter: must have conductivity and diameter
print("\n[3] Quality filtering...")
mask = extracted['conductivity_Sm'].notna() & extracted['diameter_nm'].notna()
filtered = extracted[mask].copy()
print(f"  Before filter: {len(extracted)} samples")
print(f"  After filter: {len(filtered)} samples")
print(f"  Retained: {len(filtered)/len(extracted)*100:.1f}%")

# Add source
filtered['source'] = 'meta-analysis-2021'

# Save extracted data
output_file = DATA_DIR / "cnt_meta_analysis_extracted.csv"
filtered.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n  Saved: {output_file.name}")
print(f"  Shape: {filtered.shape}")

# Statistics
print(f"\n  Sample statistics:")
print(f"    Conductivity: [{filtered['conductivity_Sm'].min():.2e}, {filtered['conductivity_Sm'].max():.2e}] S/m")
print(f"    Conductivity median: {filtered['conductivity_Sm'].median():.2e} S/m")
print(f"    Diameter: [{filtered['diameter_nm'].min():.2f}, {filtered['diameter_nm'].max():.2f}] nm")
print(f"    Diameter median: {filtered['diameter_nm'].median():.2f} nm")

# Merge with existing clean data
print("\n[4] Merging with existing clean data...")
clean_file = DATA_DIR / "cnt_dataset_clean.csv"

if clean_file.exists():
    clean_data = pd.read_csv(clean_file)
    print(f"  Existing clean data: {len(clean_data)} samples")
    
    # Select common columns
    common_cols = [col for col in clean_data.columns if col in filtered.columns]
    print(f"  Common columns: {common_cols}")
    
    if len(common_cols) >= 2:
        # Combine
        combined_data = pd.concat([
            clean_data[common_cols],
            filtered[common_cols]
        ], ignore_index=True)
        
        print(f"  Combined data: {len(combined_data)} samples")
        
        # Remove duplicates
        if 'conductivity_Sm' in combined_data.columns and 'diameter_nm' in combined_data.columns:
            before_dedup = len(combined_data)
            combined_data = combined_data.drop_duplicates(
                subset=['conductivity_Sm', 'diameter_nm'],
                keep='first'
            )
            print(f"  Duplicates removed: {before_dedup - len(combined_data)}")
        
        print(f"  After deduplication: {len(combined_data)} samples")
        
        # Save combined data
        combined_file = DATA_DIR / "cnt_dataset_combined.csv"
        combined_data.to_csv(combined_file, index=False, encoding='utf-8-sig')
        print(f"\n  Saved: {combined_file.name}")
    else:
        print("  [SKIP] Not enough common columns")
else:
    print("  [INFO] No clean data file - using extracted data only")

print("\n" + "=" * 60)
print("Extraction Complete!")
print("=" * 60)

# Summary
print("\nSummary:")
print(f"  Meta-analysis database: {len(meta_db)} rows")
print(f"  Extracted samples: {len(filtered)}")
if clean_file.exists() and len(common_cols) >= 2:
    print(f"  Combined samples: {len(combined_data)}")
    print(f"\n  Target: 300+ samples")
    if len(combined_data) >= 300:
        print(f"  [OK] Target reached! ✓")
    else:
        print(f"  [!] Still need {300 - len(combined_data)} more samples")
