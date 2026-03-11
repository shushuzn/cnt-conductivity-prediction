#!/usr/bin/env python3
"""
CNT 数据扩充到 300+ 样本
策略：使用所有 533 个样本，对缺失的 length_um 用中位数填充
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 70)
print("CNT 数据扩充到 300+ 样本")
print("=" * 70)

DATA_PATH = Path("data/cnt_dataset_v4_real.csv")
OUTPUT_PATH = Path("data/cnt_dataset_v5_300plus.csv")

# 加载数据
df = pd.read_csv(DATA_PATH)
print(f"\n原始数据：{len(df)} 行")

# 核心特征
print(f"\n数据完整性检查:")
print(f"  diameter_nm: {df['diameter_nm'].notna().sum()} ({df['diameter_nm'].notna().mean():.1%})")
print(f"  length_um: {df['length_um'].notna().sum()} ({df['length_um'].notna().mean():.1%})")
print(f"  layers: {df['layers'].notna().sum()} ({df['layers'].notna().mean():.1%})")
print(f"  conductivity_Sm: {df['conductivity_Sm'].notna().sum()} ({df['conductivity_Sm'].notna().mean():.1%})")

# 填充 length_um 缺失值
length_median = df['length_um'].median()
print(f"\nlength_um 中位数：{length_median:.2f} μm")
df['length_um'] = df['length_um'].fillna(length_median)

# 衍生特征（与 cnt_gp_run.py 一致）
print("\n添加衍生特征...")

# 1. 长径比
df['aspect_ratio'] = df['length_um'] * 1000 / df['diameter_nm']

# 2. 直径对数
df['log_diameter'] = np.log10(df['diameter_nm'] + 1e-6)

# 3. SWCNT 标识
df['is_swcnn'] = (df['layers'] == 1).astype(int)

# 4. CVD 工艺标识
df['is_cvd'] = df['method'].apply(lambda x: 1 if x == 'CVD' else 0)

# 5. 温度归一化
df['temp_normalized'] = (df['cvd_temperature_C'] / 1000.0).fillna(0)

# 6. 催化剂存在性
df['has_catalyst'] = df['catalyst'].notna().astype(int)

# 7. 碳源存在性
df['has_carbon_source'] = df['carbon_source'].notna().astype(int)

# 8. 体积分数估算
df['volume_fraction_est'] = 1.0 / (df['diameter_nm'] ** 2) * df['layers']

# 检查 NaN
FEATURES_ENHANCED = [
    'diameter_nm', 'length_um', 'layers',
    'aspect_ratio', 'log_diameter', 'is_swcnn', 'is_cvd',
    'temp_normalized', 'has_catalyst', 'has_carbon_source', 'volume_fraction_est'
]

nan_count = df[FEATURES_ENHANCED + ['conductivity_Sm']].isna().sum().sum()
print(f"\n衍生特征后 NaN 总数：{nan_count}")

# 删除仍有 NaN 的行（应该很少）
df_clean = df.dropna(subset=FEATURES_ENHANCED + ['conductivity_Sm'])
print(f"最终有效样本：{len(df_clean)}")

# 保存
df_clean.to_csv(OUTPUT_PATH, index=False, encoding='utf-8-sig')
print(f"\n已保存：{OUTPUT_PATH}")

# 统计
print(f"\n数据集统计:")
print(f"  样本数：{len(df_clean)}")
print(f"  特征数：{len(FEATURES_ENHANCED)}")
print(f"  电导率范围：{df_clean['conductivity_Sm'].min():.2e} - {df_clean['conductivity_Sm'].max():.2e} S/m")
print(f"  直径范围：{df_clean['diameter_nm'].min():.2f} - {df_clean['diameter_nm'].max():.2f} nm")
print(f"  长度范围：{df_clean['length_um'].min():.2f} - {df_clean['length_um'].max():.2f} μm")

if len(df_clean) >= 300:
    print(f"\n[OK] Target reached: {len(df_clean)} >= 300")
else:
    print(f"\n[INFO] Close to target: {len(df_clean)} / 300 ({len(df_clean)/300:.1%})")
