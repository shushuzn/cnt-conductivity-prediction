#!/usr/bin/env python3
"""
CNT 数据验证脚本
验证数据集质量和完整性

Usage:
    py cnt_data_validator.py --input data/cnt_dataset_v2.csv --report data/validation_report.md
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

print("=" * 70)
print("CNT 数据验证脚本")
print("=" * 70)

# ============================================================================
# 配置
# ============================================================================
VALID_RANGES = {
    'diameter_nm': (0.4, 100),      # 直径范围 (nm)
    'length_um': (0.1, 1000),        # 长度范围 (μm)
    'layers': (1, 50),               # 层数范围
    'conductivity_Sm': (1e-6, 1e8),  # 电导率范围 (S/m)
    'tensile_strength_GPa': (0.1, 200),  # 拉伸强度 (GPa)
    'youngs_modulus_GPa': (1, 2000),     # 杨氏模量 (GPa)
}

# ============================================================================
# 验证函数
# ============================================================================
def validate_range(df, column, min_val, max_val):
    """验证数值范围"""
    if column not in df.columns:
        return None, f"列 '{column}' 不存在"
    
    values = df[column].dropna()
    out_of_range = ((values < min_val) | (values > max_val)).sum()
    total = len(values)
    
    if out_of_range > 0:
        return False, f"{out_of_range}/{total} 超出范围 [{min_val}, {max_val}]"
    return True, f"全部 {total} 个值在范围内"

def validate_completeness(df):
    """验证数据完整性"""
    completeness = {}
    for col in df.columns:
        non_null = df[col].notna().sum()
        total = len(df)
        completeness[col] = non_null / total * 100
    return completeness

def detect_outliers(df, column):
    """检测异常值 (IQR 方法)"""
    if column not in df.columns:
        return []
    
    values = df[column].dropna()
    if len(values) < 4:
        return []
    
    Q1 = values.quantile(0.25)
    Q3 = values.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = values[(values < lower_bound) | (values > upper_bound)]
    return outliers.tolist()

# ============================================================================
# 主流程
# ============================================================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CNT 数据验证")
    parser.add_argument('--input', type=str, required=True, help='输入 CSV 文件')
    parser.add_argument('--output', type=str, default=None, help='输出报告文件')
    args = parser.parse_args()
    
    # 读取数据
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"\n❌ 文件不存在：{input_file}")
        exit(1)
    
    print(f"\n📖 读取数据：{input_file}")
    df = pd.read_csv(input_file)
    
    print(f"   总记录数：{len(df)}")
    print(f"   列数：{len(df.columns)}")
    
    # 验证
    print("\n🔍 验证数据...")
    results = []
    
    # 1. 范围验证
    print("\n1️⃣ 范围验证:")
    for col, (min_val, max_val) in VALID_RANGES.items():
        passed, msg = validate_range(df, col, min_val, max_val)
        status = "✅" if passed else ("⚠️" if passed is None else "❌")
        print(f"   {status} {col}: {msg}")
        results.append(f"- **{col}**: {msg}")
    
    # 2. 完整性验证
    print("\n2️⃣ 数据完整性:")
    completeness = validate_completeness(df)
    for col, pct in sorted(completeness.items(), key=lambda x: x[1], reverse=True):
        status = "✅" if pct >= 80 else ("⚠️" if pct >= 50 else "❌")
        print(f"   {status} {col}: {pct:.1f}%")
        results.append(f"- **{col}**: {pct:.1f}% 完整")
    
    # 3. 异常值检测
    print("\n3️⃣ 异常值检测:")
    for col in ['conductivity_Sm', 'diameter_nm', 'tensile_strength_GPa']:
        outliers = detect_outliers(df, col)
        if outliers:
            print(f"   ⚠️ {col}: {len(outliers)} 个异常值")
            results.append(f"- **{col}**: {len(outliers)} 个异常值")
        else:
            print(f"   ✅ {col}: 无异常值")
            results.append(f"- **{col}**: 无异常值")
    
    # 生成报告
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = input_file.parent / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    report = f"""# CNT 数据验证报告

**数据文件:** {input_file.name}  
**验证时间:** {datetime.now().isoformat()}  
**总记录数:** {len(df)}

---

## 验证结果

{chr(10).join(results)}

---

## 数据质量评分

**综合评分:** {'✅ 优秀' if all('✅' in r for r in results[:6]) else '⚠️ 待改进'}

---

## 建议

1. 检查异常值是否为录入错误
2. 补充缺失的关键字段数据
3. 验证超出范围的数值是否准确

---

*自动生成 by cnt_data_validator.py*
"""
    
    output_file.write_text(report, encoding='utf-8')
    print(f"\n📁 报告已保存：{output_file}")
