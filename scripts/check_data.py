import pandas as pd

df = pd.read_csv('data/cnt_dataset_v4_real.csv')
print(f"Total rows: {len(df)}")
print(f"Diameter non-null: {df['diameter_nm'].notna().sum()}")
print(f"Conductivity non-null: {df['conductivity_Sm'].notna().sum()}")
print(f"Both complete: {df[['diameter_nm', 'conductivity_Sm']].notna().all(axis=1).sum()}")
print(f"With length_um: {df[['diameter_nm', 'length_um', 'conductivity_Sm']].notna().all(axis=1).sum()}")
print(f"With layers: {df[['diameter_nm', 'layers', 'conductivity_Sm']].notna().all(axis=1).sum()}")
print(f"Core 3 + conductivity: {df[['diameter_nm', 'length_um', 'layers', 'conductivity_Sm']].notna().all(axis=1).sum()}")
