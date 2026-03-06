#!/usr/bin/env python3
"""
测试批量导入功能
"""

import pandas as pd
from pathlib import Path

print("=" * 70)
print("CNT 数据提取工具 - 批量导入测试")
print("=" * 70)

# 测试文件
sample_file = Path("D:/OpenClaw/workspace/11-research/cnt-research/data/sample_dataset.csv")
output_file = Path("D:/OpenClaw/workspace/11-research/cnt-research/data/cnt_dataset_v1.csv")

# 检查文件
print(f"\n[1/3] 检查示例数据...")
if sample_file.exists():
    df_sample = pd.read_csv(sample_file)
    print(f"  [OK] 示例文件存在：{sample_file.name}")
    print(f"  记录数：{len(df_sample)}")
    print(f"  列数：{len(df_sample.columns)}")
    print(f"\n  列名:")
    for col in df_sample.columns:
        print(f"    - {col}")
else:
    print(f"  ✗ 示例文件不存在：{sample_file}")
    exit(1)

# 显示数据预览
print(f"\n[2/3] 数据预览...")
print(f"\n  前 3 条记录:")
print(df_sample[['paper_id', 'title', 'diameter_nm', 'conductivity_Sm']].head(3).to_string())

print(f"\n  数据统计:")
print(f"    直径范围：{df_sample['diameter_nm'].min():.1f} - {df_sample['diameter_nm'].max():.1f} nm")
print(f"    电导率范围：{df_sample['conductivity_Sm'].min():.2e} - {df_sample['conductivity_Sm'].max():.2e} S/m")
print(f"    层数分布：SWCNT={len(df_sample[df_sample['layers']==1])}, MWCNT={len(df_sample[df_sample['layers']>1])}")

# 保存为初始数据集
print(f"\n[3/3] 创建初始数据集...")
df_sample.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"  [OK] 已保存：{output_file}")
print(f"  记录数：{len(df_sample)}")

print("\n" + "=" * 70)
print("[OK] 批量导入测试完成！")
print("=" * 70)

print(f"\n下一步:")
print(f"  1. 运行数据提取工具查看数据")
print(f"  2. 继续添加更多数据")
print(f"  3. 开始 GP 模型训练")
