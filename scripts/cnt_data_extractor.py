#!/usr/bin/env python3
"""
CNT 数据提取工具

从文献 PDF 中提取数据并整理为 CSV 格式
支持手动输入和批量导入

依赖:
    pip install pandas numpy openpyxl
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

print("=" * 70)
print("CNT 数据提取工具")
print("=" * 70)

# ============================================================================
# 配置
# ============================================================================
DATA_DIR = Path("D:/OpenClaw/workspace/11-research/cnt-research/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATA_DIR / "cnt_dataset_v1.csv"
BACKUP_FILE = DATA_DIR / f"cnt_dataset_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# ============================================================================
# 数据模板
# ============================================================================
COLUMNS = [
    'paper_id',      # 论文 ID: CNT_001, CNT_002...
    'doi',           # DOI
    'title',         # 论文标题
    'year',          # 发表年份
    'journal',       # 期刊名
    'diameter_nm',   # 直径 (nm)
    'length_um',     # 长度 (μm)
    'layers',        # 层数 (SWCNT=1, MWCNT=n)
    'method',        # 制备方法 (CVD/电弧/激光等)
    'cvd_temperature_C',  # CVD 温度 (°C)
    'catalyst',      # 催化剂
    'carbon_source', # 碳源
    'conductivity_Sm',    # 电导率 (S/m)
    'tensile_strength_GPa', # 拉伸强度 (GPa)
    'youngs_modulus_GPa',   # 杨氏模量 (GPa)
    'notes',         # 备注
    'status'         # 状态 (To Read/Extracted/Verified)
]

# ============================================================================
# 工具函数
# ============================================================================

def load_existing_data():
    """加载现有数据集"""
    if OUTPUT_FILE.exists():
        df = pd.read_csv(OUTPUT_FILE)
        print(f"  已加载现有数据：{len(df)} 条记录")
        return df
    else:
        print("  创建新数据集")
        return pd.DataFrame(columns=COLUMNS)

def save_data(df):
    """保存数据集"""
    if OUTPUT_FILE.exists():
        # 备份现有文件
        import shutil
        shutil.copy(OUTPUT_FILE, BACKUP_FILE)
        print(f"  已备份：{BACKUP_FILE.name}")
    
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"  已保存：{OUTPUT_FILE}")

def generate_paper_id(df):
    """生成新的论文 ID"""
    if len(df) == 0:
        return "CNT_001"
    else:
        last_id = df['paper_id'].iloc[-1]
        last_num = int(last_id.split('_')[1])
        return f"CNT_{last_num + 1:03d}"

def convert_conductivity(value, unit):
    """转换电导率单位为 S/m"""
    if pd.isna(value):
        return np.nan
    
    value = float(value)
    unit = unit.lower().strip()
    
    if 's/cm' in unit:
        return value * 100  # S/cm → S/m
    elif 's/m' in unit:
        return value
    elif 'ms/cm' in unit:
        return value * 10  # mS/cm → S/m
    else:
        return value  # 假设已经是 S/m

def convert_length(value, unit):
    """转换长度单位为 μm"""
    if pd.isna(value):
        return np.nan
    
    value = float(value)
    unit = unit.lower().strip()
    
    if 'nm' in unit:
        return value / 1000  # nm → μm
    elif 'um' in unit or 'μm' in unit:
        return value
    elif 'mm' in unit:
        return value * 1000  # mm → μm
    else:
        return value  # 假设已经是 μm

def convert_strength(value, unit):
    """转换强度单位为 GPa"""
    if pd.isna(value):
        return np.nan
    
    value = float(value)
    unit = unit.lower().strip()
    
    if 'mpa' in unit:
        return value / 1000  # MPa → GPa
    elif 'gpa' in unit:
        return value
    else:
        return value  # 假设已经是 GPa

# ============================================================================
# 交互式数据录入
# ============================================================================

def manual_entry_mode():
    """手动录入模式"""
    print("\n" + "=" * 70)
    print("手动录入模式")
    print("=" * 70)
    
    df = load_existing_data()
    
    while True:
        print(f"\n当前记录数：{len(df)}")
        print("\n选项:")
        print("  [1] 添加新记录")
        print("  [2] 查看最近记录")
        print("  [3] 保存并退出")
        print("  [4] 放弃并退出")
        
        choice = input("\n请选择 (1-4): ").strip()
        
        if choice == '1':
            # 添加新记录
            paper_id = generate_paper_id(df)
            print(f"\n录入新记录：{paper_id}")
            
            record = {
                'paper_id': paper_id,
                'doi': input("DOI (可选): ").strip() or None,
                'title': input("论文标题: ").strip() or None,
                'year': input("年份: ").strip() or None,
                'journal': input("期刊: ").strip() or None,
                'diameter_nm': input("直径 (nm): ").strip() or None,
                'length_um': input("长度 (μm): ").strip() or None,
                'layers': input("层数: ").strip() or None,
                'method': input("制备方法: ").strip() or None,
                'cvd_temperature_C': input("CVD 温度 (°C): ").strip() or None,
                'catalyst': input("催化剂: ").strip() or None,
                'carbon_source': input("碳源: ").strip() or None,
                'conductivity_Sm': input("电导率 (S/m): ").strip() or None,
                'tensile_strength_GPa': input("拉伸强度 (GPa): ").strip() or None,
                'youngs_modulus_GPa': input("杨氏模量 (GPa): ").strip() or None,
                'notes': input("备注 (可选): ").strip() or None,
                'status': 'Extracted'
            }
            
            df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
            print(f"  ✓ 已添加 {paper_id}")
            
        elif choice == '2':
            # 查看最近记录
            if len(df) > 0:
                print("\n最近 5 条记录:")
                print(df.tail()[['paper_id', 'title', 'diameter_nm', 'conductivity_Sm']].to_string())
            else:
                print("  暂无记录")
                
        elif choice == '3':
            # 保存并退出
            save_data(df)
            print("\n✓ 数据已保存，再见！")
            break
            
        elif choice == '4':
            # 放弃并退出
            print("\n已放弃更改，再见！")
            break
        else:
            print("  无效选择，请重试")

# ============================================================================
# 批量导入模式
# ============================================================================

def batch_import_mode():
    """批量导入模式"""
    print("\n" + "=" * 70)
    print("批量导入模式")
    print("=" * 70)
    
    print("\n支持的格式:")
    print("  1. Excel (.xlsx) - 推荐")
    print("  2. CSV (.csv)")
    print("  3. JSON (.json)")
    
    file_path = input("\n请输入文件路径: ").strip()
    
    if not Path(file_path).exists():
        print(f"  ✗ 文件不存在：{file_path}")
        return
    
    try:
        if file_path.endswith('.xlsx'):
            df_new = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df_new = pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            df_new = pd.read_json(file_path)
        else:
            print("  ✗ 不支持的文件格式")
            return
        
        print(f"  ✓ 成功导入 {len(df_new)} 条记录")
        
        # 合并到现有数据
        df_existing = load_existing_data()
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        
        # 保存
        save_data(df_combined)
        
        print(f"\n✓ 批量导入完成！总计 {len(df_combined)} 条记录")
        
    except Exception as e:
        print(f"  ✗ 导入失败：{str(e)}")

# ============================================================================
# 数据统计
# ============================================================================

def show_statistics():
    """显示数据统计"""
    print("\n" + "=" * 70)
    print("数据统计")
    print("=" * 70)
    
    df = load_existing_data()
    
    if len(df) == 0:
        print("  暂无数据")
        return
    
    print(f"\n总记录数：{len(df)}")
    print(f"已提取：{len(df[df['status'] == 'Extracted'])}")
    print(f"已验证：{len(df[df['status'] == 'Verified'])}")
    
    # 数值统计
    print("\n数值统计:")
    numeric_cols = ['diameter_nm', 'length_um', 'layers', 'conductivity_Sm']
    
    for col in numeric_cols:
        if col in df.columns and df[col].notna().any():
            print(f"\n  {col}:")
            print(f"    最小值：{df[col].min():.2f}")
            print(f"    最大值：{df[col].max():.2f}")
            print(f"    平均值：{df[col].mean():.2f}")
            print(f"    中位数：{df[col].median():.2f}")

# ============================================================================
# 主程序
# ============================================================================

def main():
    print("\n欢迎使用 CNT 数据提取工具！")
    print("\n本工具用于:")
    print("  - 手动录入文献数据")
    print("  - 批量导入 Excel/CSV 数据")
    print("  - 查看数据统计")
    
    while True:
        print("\n" + "=" * 70)
        print("主菜单")
        print("=" * 70)
        print("\n选项:")
        print("  [1] 手动录入模式")
        print("  [2] 批量导入模式")
        print("  [3] 查看数据统计")
        print("  [4] 退出")
        
        choice = input("\n请选择 (1-4): ").strip()
        
        if choice == '1':
            manual_entry_mode()
        elif choice == '2':
            batch_import_mode()
        elif choice == '3':
            show_statistics()
        elif choice == '4':
            print("\n再见！")
            break
        else:
            print("  无效选择，请重试")

if __name__ == "__main__":
    main()
