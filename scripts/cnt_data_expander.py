#!/usr/bin/env python3
"""
CNT 数据扩充脚本 - 基于文献值生成合成数据

从已知 5 个真实样本出发，基于文献报道的范围生成合理的合成数据
用于快速扩充训练集，支持 ML 模型初步训练

文献依据:
- SWCNT 电导率：10^5 - 10^7 S/m
- MWCNT 电导率：10^4 - 10^6 S/m
- 拉伸强度：10-150 GPa
- 杨氏模量：200-1500 GPa
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import sys
import io

# 修复 Windows 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("CNT 数据扩充脚本 - 文献值合成")
print("=" * 70)

# ============================================================================
# 配置
# ============================================================================
DATA_DIR = Path("D:/OpenClaw/workspace/11-research/cnt-research/data")
OUTPUT_FILE = DATA_DIR / "cnt_dataset_v2_synthetic.csv"

# 随机种子（可复现）
np.random.seed(42)

# ============================================================================
# 文献参数范围 (基于已收集的 5 个真实样本 + 文献综述)
# ============================================================================
LITERATURE_RANGES = {
    'SWCNT': {
        'diameter_nm': (0.8, 3.0),      # 直径范围
        'length_um': (10, 500),          # 长度范围
        'layers': 1,                      # 单壁
        'conductivity_Sm': (5e5, 2e6),   # 电导率范围
        'tensile_strength_GPa': (30, 150), # 拉伸强度
        'youngs_modulus_GPa': (800, 1500), # 杨氏模量
    },
    'MWCNT': {
        'diameter_nm': (3, 50),          # 直径范围
        'length_um': (10, 1000),         # 长度范围
        'layers': (2, 20),               # 层数范围
        'conductivity_Sm': (1e5, 1e6),   # 电导率范围
        'tensile_strength_GPa': (10, 80),  # 拉伸强度
        'youngs_modulus_GPa': (200, 1000), # 杨氏模量
    }
}

# 制备方法分布
METHODS = {
    'CVD': 0.50,           # 50% CVD
    'Arc discharge': 0.25, # 25% 电弧
    'Laser ablation': 0.20, # 20% 激光
    'HiPco': 0.05,         # 5% HiPco
}

# 催化剂分布
CATALYSTS = ['Fe', 'Co', 'Ni', 'Fe/Co', 'Co/Mo', None]
CATALYST_WEIGHTS = [0.30, 0.25, 0.15, 0.15, 0.10, 0.05]

# 碳源分布
CARBON_SOURCES = ['CH4', 'C2H2', 'C2H4', 'CO', 'Ethanol', None]
CARBON_SOURCE_WEIGHTS = [0.30, 0.25, 0.15, 0.10, 0.10, 0.10]

# ============================================================================
# 数据生成函数
# ============================================================================

def generate_sample(material_type, sample_id):
    """生成单个样本"""
    params = LITERATURE_RANGES[material_type]
    
    # 结构参数
    diameter = np.random.uniform(*params['diameter_nm'])
    length = np.random.uniform(*params['length_um'])
    
    if isinstance(params['layers'], int):
        layers = params['layers']
    else:
        layers = np.random.randint(*params['layers'])
    
    # 制备方法
    method = np.random.choice(list(METHODS.keys()), p=list(METHODS.values()))
    
    # 工艺参数（仅 CVD 有温度和催化剂）
    if method == 'CVD':
        cvd_temp = np.random.uniform(700, 1000)  # °C
        catalyst = np.random.choice(CATALYSTS, p=CATALYST_WEIGHTS)
        carbon_source = np.random.choice(CARBON_SOURCES, p=CARBON_SOURCE_WEIGHTS)
    else:
        cvd_temp = np.nan
        catalyst = None
        carbon_source = None
    
    # 性能参数（对数均匀分布）
    conductivity = np.random.uniform(*params['conductivity_Sm'])
    tensile_strength = np.random.uniform(*params['tensile_strength_GPa'])
    youngs_modulus = np.random.uniform(*params['youngs_modulus_GPa'])
    
    # 添加一些相关性（更真实）
    # 直径越小，电导率倾向于越高（量子限制效应）
    if material_type == 'SWCNT':
        conductivity *= (3.0 / diameter) ** 0.3  # 轻微反比
    
    # 层数越多，模量倾向于越高
    if material_type == 'MWCNT':
        youngs_modulus *= (layers / 5) ** 0.2
    
    return {
        'paper_id': f'CNT_{sample_id:03d}',
        'doi': f'SYNTHETIC_{sample_id:03d}',
        'title': f'Synthetic data based on literature ranges ({material_type})',
        'year': np.random.randint(2010, 2024),
        'journal': 'Literature-based synthesis',
        'diameter_nm': round(diameter, 2),
        'length_um': round(length, 1),
        'layers': layers,
        'method': method,
        'cvd_temperature_C': round(cvd_temp, 0) if not np.isnan(cvd_temp) else np.nan,
        'catalyst': catalyst,
        'carbon_source': carbon_source,
        'conductivity_Sm': round(conductivity, 0),
        'tensile_strength_GPa': round(tensile_strength, 1),
        'youngs_modulus_GPa': round(youngs_modulus, 0),
        'notes': f'{material_type} synthetic data',
        'status': 'Synthetic',
        'material_type': material_type
    }

# ============================================================================
# 主流程
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CNT 数据扩充")
    parser.add_argument('--n-swcnt', type=int, default=100, help='SWCNT 样本数')
    parser.add_argument('--n-mwcnt', type=int, default=100, help='MWCNT 样本数')
    parser.add_argument('--output', type=str, default=None, help='输出文件')
    args = parser.parse_args()
    
    print(f"\n📊 生成参数:")
    print(f"   SWCNT 样本数：{args.n_swcnt}")
    print(f"   MWCNT 样本数：{args.n_mwcnt}")
    print(f"   总样本数：{args.n_swcnt + args.n_mwcnt}")
    
    # 加载真实数据
    real_data_file = DATA_DIR / "cnt_dataset_v1.csv"
    if real_data_file.exists():
        df_real = pd.read_csv(real_data_file)
        print(f"\n✅ 加载真实数据：{len(df_real)} 条记录")
    else:
        df_real = pd.DataFrame()
        print("\n⚠️  未找到真实数据，仅生成合成数据")
    
    # 生成合成数据
    print(f"\n🔧 生成合成数据...")
    synthetic_samples = []
    
    total_id = len(df_real) + 1
    
    for i in range(args.n_swcnt):
        sample = generate_sample('SWCNT', total_id)
        synthetic_samples.append(sample)
        total_id += 1
    
    for i in range(args.n_mwcnt):
        sample = generate_sample('MWCNT', total_id)
        synthetic_samples.append(sample)
        total_id += 1
    
    df_synthetic = pd.DataFrame(synthetic_samples)
    print(f"   ✅ 生成 {len(df_synthetic)} 条合成记录")
    
    # 合并数据
    if len(df_real) > 0:
        # 添加 material_type 列到真实数据
        if 'material_type' not in df_real.columns:
            df_real['material_type'] = df_real['layers'].apply(lambda x: 'SWCNT' if x == 1 else 'MWCNT')
        
        df_combined = pd.concat([df_real, df_synthetic], ignore_index=True)
        print(f"\n📦 合并后总记录数：{len(df_combined)}")
    else:
        df_combined = df_synthetic
    
    # 保存
    output_file = args.output if args.output else OUTPUT_FILE
    df_combined.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✅ 数据已保存：{output_file}")
    
    # 统计分析
    print(f"\n📊 数据统计:")
    print(f"\n   材料类型分布:")
    print(df_combined['material_type'].value_counts())
    
    print(f"\n   电导率范围 (S/m):")
    print(f"      Min: {df_combined['conductivity_Sm'].min():.2e}")
    print(f"      Max: {df_combined['conductivity_Sm'].max():.2e}")
    print(f"      Mean: {df_combined['conductivity_Sm'].mean():.2e}")
    
    print(f"\n   直径范围 (nm):")
    print(f"      Min: {df_combined['diameter_nm'].min():.2f}")
    print(f"      Max: {df_combined['diameter_nm'].max():.2f}")
    print(f"      Mean: {df_combined['diameter_nm'].mean():.2f}")
    
    print(f"\n   拉伸强度范围 (GPa):")
    print(f"      Min: {df_combined['tensile_strength_GPa'].min():.2f}")
    print(f"      Max: {df_combined['tensile_strength_GPa'].max():.2f}")
    print(f"      Mean: {df_combined['tensile_strength_GPa'].mean():.2f}")
    
    print(f"\n   杨氏模量范围 (GPa):")
    print(f"      Min: {df_combined['youngs_modulus_GPa'].min():.2f}")
    print(f"      Max: {df_combined['youngs_modulus_GPa'].max():.2f}")
    print(f"      Mean: {df_combined['youngs_modulus_GPa'].mean():.2f}")
    
    # 可视化提示
    print(f"\n💡 下一步建议:")
    print(f"   1. 运行 cnt_gp_run.py 训练 GP 模型")
    print(f"   2. 使用 SHAP 分析特征重要性")
    print(f"   3. 继续从文献提取真实数据替换合成数据")
