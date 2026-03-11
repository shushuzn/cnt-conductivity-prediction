#!/usr/bin/env python3
"""
从 Supporting Information Excel 数据库提取 CNT 数据
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("CNT Meta-Analysis 数据库提取")
print("=" * 70)

# Excel 文件路径
EXCEL_PATH = Path("D:/OpenClaw/workspace/11-research/cnt-research/literature/pdfs/supp-data/20210409_Metaanalysis_database.xlsx")

if not EXCEL_PATH.exists():
    print(f"❌ Excel 文件不存在：{EXCEL_PATH}")
    exit(1)

print(f"\n📊 打开 Excel: {EXCEL_PATH.name}")
print(f"   大小：{EXCEL_PATH.stat().st_size / 1024:.1f} KB")

# 读取所有 sheet
xlsx = pd.ExcelFile(EXCEL_PATH)
print(f"\n📑 Sheet 列表:")
for sheet in xlsx.sheet_names:
    print(f"   - {sheet}")

# 读取主数据表
print(f"\n🔍 读取数据...")

# 尝试读取第一个 sheet（通常是主数据）
df = pd.read_excel(EXCEL_PATH, sheet_name=xlsx.sheet_names[0])

print(f"\n✅ 数据加载完成!")
print(f"   行数：{len(df)}")
print(f"   列数：{len(df.columns)}")

print(f"\n📋 列名:")
for i, col in enumerate(df.columns):
    print(f"   {i+1}. {col}")

# 显示前几行
print(f"\n📊 数据预览 (前 5 行):")
print(df.head())

# 统计信息
print(f"\n📈 数据统计:")
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols[:10]:  # 前 10 个数值列
    print(f"   {col}: {df[col].mean():.2f} (mean), {df[col].std():.2f} (std), {df[col].min():.2f} - {df[col].max():.2f}")

# 保存为 CSV
OUTPUT_CSV = EXCEL_PATH.parent / "meta-analysis-2021-database.csv"
df.to_csv(OUTPUT_CSV, index=False)
print(f"\n✅ 已保存：{OUTPUT_CSV}")

# 提取关键列（电导率、强度、模量等）
print("\n" + "=" * 70)
print("提取 CNT 相关数据...")

# 查找关键列
key_columns = []
for col in df.columns:
    col_lower = str(col).lower()
    if any(x in col_lower for x in ['conductivity', 'strength', 'modulus', 'diameter', 'length', 'density']):
        key_columns.append(col)

print(f"\n🔑 关键列 ({len(key_columns)}):")
for col in key_columns:
    print(f"   - {col}")

# 提取子集
if key_columns:
    df_key = df[key_columns]
    print(f"\n📊 关键数据预览:")
    print(df_key.head())
    
    # 保存关键数据
    KEY_CSV = EXCEL_PATH.parent / "meta-analysis-2021-key-data.csv"
    df_key.to_csv(KEY_CSV, index=False)
    print(f"\n✅ 关键数据已保存：{KEY_CSV}")

print("\n" + "=" * 70)
print("✅ 提取完成！")
print("=" * 70)
