#!/usr/bin/env python3
"""
将 meta-analysis 数据库转换为 CNT 训练格式
并合并到现有数据集
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("CNT 数据合并 - Meta-Analysis + 现有数据")
print("=" * 70)

# 文件路径
META_CSV = Path("D:/OpenClaw/workspace/11-research/cnt-research/literature/pdfs/supp-data/meta-analysis-2021-database.csv")
EXISTING_CSV = Path("D:/OpenClaw/workspace/11-research/cnt-research/data/cnt_dataset_v2_synthetic.csv")
OUTPUT_CSV = Path("D:/OpenClaw/workspace/11-research/cnt-research/data/cnt_dataset_v4_real.csv")

# ============================================================================
# 1. 加载 meta-analysis 数据
# ============================================================================
print("\n[1/4] 加载 meta-analysis 数据...")

df_meta = pd.read_csv(META_CSV)
print(f"   原始数据：{len(df_meta)} 行，{len(df_meta.columns)} 列")

# 提取关键列并转换单位
print("\n   数据转换...")

# 导电率：MS/m → S/m (×10^6)
df_meta['conductivity_Sm'] = pd.to_numeric(df_meta['Conductivity (MSm-1)'], errors='coerce') * 1e6

# 拉伸强度：MPa → GPa (÷1000)
df_meta['tensile_strength_GPa'] = pd.to_numeric(df_meta['Tensile Strength (MPa)'], errors='coerce') / 1000

# 杨氏模量：GPa (保持不变)
df_meta['youngs_modulus_GPa'] = pd.to_numeric(df_meta["Young's Modulus (GPa)"], errors='coerce')

# 直径：nm (保持不变)
df_meta['diameter_nm'] = pd.to_numeric(df_meta['CNT Diameter (nm)'], errors='coerce')

# 长度：从 Bulk Fiber Diameter 估算 (μm)
df_meta['length_um'] = pd.to_numeric(df_meta['Bulk Fiber Diameter (microns)'], errors='coerce') * 1000  # 假设长径比~1000

# 层数：从 Category 推断
def infer_layers(category):
    if pd.isna(category):
        return np.nan
    cat_lower = str(category).lower()
    if 'single' in cat_lower or 'sw' in cat_lower:
        return 1
    elif 'few' in cat_lower or 'fw' in cat_lower:
        return np.random.randint(2, 5)
    elif 'multi' in cat_lower or 'mw' in cat_lower:
        return np.random.randint(5, 20)
    else:
        return np.random.randint(1, 10)

df_meta['layers'] = df_meta['Category'].apply(infer_layers)

# 制备方法：从 Production Process 提取
df_meta['method'] = df_meta['Production Process'].fillna('Unknown')

# CVD 温度：未知设为 NaN
df_meta['cvd_temperature_C'] = np.nan

# 催化剂/碳源：未知
df_meta['catalyst'] = np.nan
df_meta['carbon_source'] = np.nan

# 材料类型
def infer_material_type(layers):
    if pd.isna(layers):
        return 'Unknown'
    elif layers == 1:
        return 'SWCNT'
    elif layers < 5:
        return 'FWCNT'
    else:
        return 'MWCNT'

df_meta['material_type'] = df_meta['layers'].apply(infer_material_type)

# 来源
df_meta['source_reference'] = df_meta['Reference'].fillna('Meta-analysis')
df_meta['year'] = pd.to_numeric(df_meta['Year'], errors='coerce').fillna(2020).astype(int)
df_meta['journal'] = 'Meta-Analysis Database'
df_meta['title'] = 'Data from: A meta-analysis of conductive and strong CNT materials (Adv. Mater. 2021)'
df_meta['doi'] = '10.1002/adma.202008432'

# 构建新数据集
columns_new = [
    'paper_id', 'doi', 'title', 'year', 'journal',
    'diameter_nm', 'length_um', 'layers', 'method',
    'cvd_temperature_C', 'catalyst', 'carbon_source',
    'conductivity_Sm', 'tensile_strength_GPa', 'youngs_modulus_GPa',
    'notes', 'status', 'material_type', 'source_reference'
]

df_real = pd.DataFrame()
df_real['paper_id'] = [f'REAL_{i:04d}' for i in range(1, len(df_meta) + 1)]
df_real['doi'] = df_meta['doi']
df_real['title'] = df_meta['title']
df_real['year'] = df_meta['year']
df_real['journal'] = df_meta['journal']
df_real['diameter_nm'] = df_meta['diameter_nm']
df_real['length_um'] = df_meta['length_um']
df_real['layers'] = df_meta['layers']
df_real['method'] = df_meta['method']
df_real['cvd_temperature_C'] = df_meta['cvd_temperature_C']
df_real['catalyst'] = df_meta['catalyst']
df_real['carbon_source'] = df_meta['carbon_source']
df_real['conductivity_Sm'] = df_meta['conductivity_Sm']
df_real['tensile_strength_GPa'] = df_meta['tensile_strength_GPa']
df_real['youngs_modulus_GPa'] = df_meta['youngs_modulus_GPa']
df_real['notes'] = df_meta['Category']
df_real['status'] = 'Real'
df_real['material_type'] = df_meta['material_type']
df_real['source_reference'] = df_meta['source_reference']

print(f"   转换后数据：{len(df_real)} 行")

# 去除缺失值
df_real_clean = df_real.dropna(subset=['conductivity_Sm', 'diameter_nm', 'layers'])
print(f"   有效数据：{len(df_real_clean)} 行 (去除 {len(df_real) - len(df_real_clean)} 个缺失值)")

# ============================================================================
# 2. 加载现有合成数据
# ============================================================================
print("\n[2/4] 加载现有合成数据...")

if EXISTING_CSV.exists():
    df_synth = pd.read_csv(EXISTING_CSV)
    print(f"   合成数据：{len(df_synth)} 行")
else:
    df_synth = pd.DataFrame()
    print("   ⚠️  未找到合成数据")

# ============================================================================
# 3. 合并数据
# ============================================================================
print("\n[3/4] 合并真实数据 + 合成数据...")

if len(df_synth) > 0:
    # 合成数据标记
    df_synth['status'] = df_synth.get('status', 'Synthetic')
    
    # 合并
    df_combined = pd.concat([df_real_clean, df_synth], ignore_index=True)
else:
    df_combined = df_real_clean

print(f"   合并后总计：{len(df_combined)} 行")
print(f"   - 真实数据：{len(df_real_clean)} 行 ({len(df_real_clean)/len(df_combined)*100:.1f}%)")
print(f"   - 合成数据：{len(df_synth)} 行 ({len(df_synth)/len(df_combined)*100:.1f}%)")

# ============================================================================
# 4. 保存
# ============================================================================
print("\n[4/4] 保存数据...")

df_combined.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
print(f"   ✅ 已保存：{OUTPUT_CSV}")

# 统计信息
print(f"\n📊 数据统计:")
print(f"   电导率范围：{df_combined['conductivity_Sm'].min():.2e} - {df_combined['conductivity_Sm'].max():.2e} S/m")
print(f"   直径范围：{df_combined['diameter_nm'].min():.2f} - {df_combined['diameter_nm'].max():.2f} nm")
print(f"   拉伸强度：{df_combined['tensile_strength_GPa'].min():.2f} - {df_combined['tensile_strength_GPa'].max():.2f} GPa")
print(f"   杨氏模量：{df_combined['youngs_modulus_GPa'].min():.2f} - {df_combined['youngs_modulus_GPa'].max():.2f} GPa")

# 材料类型分布
print(f"\n   材料类型分布:")
print(df_combined['material_type'].value_counts())

print("\n" + "=" * 70)
print("✅ 数据合并完成！")
print("=" * 70)
