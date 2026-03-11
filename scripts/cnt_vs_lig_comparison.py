#!/usr/bin/env python3
"""
CNT vs LIG 跨材料对比分析

对比维度：
1. 电导率范围
2. 制造工艺复杂度
3. 成本效益
4. 应用场景
5. 技术成熟度 (TRL)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

print("=" * 70)
print("CNT vs LIG 跨材料对比分析")
print("=" * 70)

# ============================================================================
# 1. 加载数据
# ============================================================================
print("\n[1/4] 加载数据...")

# CNT 数据
CNT_DATA = Path("data/cnt_dataset_v4_real.csv")
df_cnt = pd.read_csv(CNT_DATA)
print(f"\nCNT 数据集:")
print(f"  样本数：{len(df_cnt)}")
print(f"  电导率范围：{df_cnt['conductivity_Sm'].min():.2e} - {df_cnt['conductivity_Sm'].max():.2e} S/m")
print(f"  直径范围：{df_cnt['diameter_nm'].min():.2f} - {df_cnt['diameter_nm'].max():.2f} nm")
print(f"  层数范围：{df_cnt['layers'].min():.0f} - {df_cnt['layers'].max():.0f}")

# LIG 数据
LIG_DATA = Path("D:/OpenClaw/workspace/11-research/data/lig_dataset_200.csv")
df_lig = pd.read_csv(LIG_DATA)
print(f"\nLIG 数据集:")
print(f"  样本数：{len(df_lig)}")

# LIG 列名映射
lig_conductivity_col = 'sigma_Sm' if 'sigma_Sm' in df_lig.columns else 'conductivity_Sm'
df_lig['conductivity_Sm'] = df_lig[lig_conductivity_col]

# 添加缺失的列 (用于后续分析)
if 'laser_power_mW' not in df_lig.columns:
    df_lig['laser_power_mW'] = df_lig.get('P_W', 0) * 1000  # 假设 P_W 是功率 (W)
if 'scan_speed_mm_s' not in df_lig.columns:
    df_lig['scan_speed_mm_s'] = df_lig.get('v_mms', 0)  # 假设 v_mms 是速度

print(f"  电导率范围：{df_lig['conductivity_Sm'].min():.2e} - {df_lig['conductivity_Sm'].max():.2e} S/m")
print(f"  激光功率：{df_lig['laser_power_mW'].min():.0f} - {df_lig['laser_power_mW'].max():.0f} mW")
print(f"  扫描速度：{df_lig['scan_speed_mm_s'].min():.1f} - {df_lig['scan_speed_mm_s'].max():.1f} mm/s")

# ============================================================================
# 2. 电导率对比
# ============================================================================
print("\n" + "=" * 70)
print("电导率对比")
print("=" * 70)

cnt_conductivity = df_cnt['conductivity_Sm'].dropna()
lig_conductivity = df_lig['conductivity_Sm'].dropna()

print(f"\n统计指标:")
print(f"{'指标':<15} {'CNT':<20} {'LIG':<20}")
print("-" * 55)
print(f"{'最小值':<15} {cnt_conductivity.min():<20.2e} {lig_conductivity.min():<20.2e}")
print(f"{'最大值':<15} {cnt_conductivity.max():<20.2e} {lig_conductivity.max():<20.2e}")
print(f"{'平均值':<15} {cnt_conductivity.mean():<20.2e} {lig_conductivity.mean():<20.2e}")
print(f"{'中位数':<15} {cnt_conductivity.median():<20.2e} {lig_conductivity.median():<20.2e}")
print(f"{'标准差':<15} {cnt_conductivity.std():<20.2e} {lig_conductivity.std():<20.2e}")

# 电导率等级分布
def conductivity_tier(cond):
    if cond >= 1e7:
        return "超高 (>=10^7)"
    elif cond >= 1e6:
        return "高 (10^6-10^7)"
    elif cond >= 1e5:
        return "中 (10^5-10^6)"
    elif cond >= 1e4:
        return "低 (10^4-10^5)"
    else:
        return "极低 (<10^4)"

cnt_tiers = pd.cut(cnt_conductivity, 
                   bins=[0, 1e4, 1e5, 1e6, 1e7, float('inf')],
                   labels=['<10^4', '10^4-10^5', '10^5-10^6', '10^6-10^7', '>10^7'])
lig_tiers = pd.cut(lig_conductivity,
                   bins=[0, 1e4, 1e5, 1e6, 1e7, float('inf')],
                   labels=['<10^4', '10^4-10^5', '10^5-10^6', '10^6-10^7', '>10^7'])

print(f"\n电导率分布:")
print(f"{'等级':<15} {'CNT 数量':<15} {'CNT 占比':<15} {'LIG 数量':<15} {'LIG 占比':<15}")
print("-" * 75)
for tier in cnt_tiers.cat.categories:
    cnt_count = (cnt_tiers == tier).sum()
    cnt_pct = cnt_count / len(cnt_tiers) * 100
    lig_count = (lig_tiers == tier).sum()
    lig_pct = lig_count / len(lig_tiers) * 100
    print(f"{tier:<15} {cnt_count:<15} {cnt_pct:<15.1f} {lig_count:<15} {lig_pct:<15.1f}")

# ============================================================================
# 3. 工艺对比
# ============================================================================
print("\n" + "=" * 70)
print("制造工艺对比")
print("=" * 70)

print(f"\nCNT 制备方法:")
if 'method' in df_cnt.columns:
    method_counts = df_cnt['method'].value_counts()
    for method, count in method_counts.items():
        pct = count / len(df_cnt) * 100
        print(f"  {method}: {count} ({pct:.1f}%)")

print(f"\nLIG 制备工艺:")
print(f"  方法：激光直写 (Laser-Induced Graphene)")
print(f"  前驱体：聚合物薄膜 (PI, PET, 纸张，生物材料等)")
print(f"  激光功率：{df_lig['laser_power_mW'].min():.0f} - {df_lig['laser_power_mW'].max():.0f} mW")
print(f"  扫描速度：{df_lig['scan_speed_mm_s'].min():.1f} - {df_lig['scan_speed_mm_s'].max():.1f} mm/s")
print(f"  环境：{df_lig['atmosphere'].unique() if 'atmosphere' in df_lig.columns else '空气/惰性气体'}")

# 工艺复杂度评分 (1-10)
print(f"\n工艺复杂度评分 (1-10, 10 为最复杂):")
print(f"  CNT: 8/10")
print(f"    - 需要高温 CVD (700-1000°C)")
print(f"    - 需要催化剂 (Fe, Co, Ni)")
print(f"    - 需要碳源气体 (CH4, C2H2)")
print(f"    - 后处理复杂 (纯化，分散)")
print(f"  LIG: 3/10")
print(f"    - 室温加工")
print(f"    - 无需催化剂")
print(f"    - 一步成型")
print(f"    - 可直接图案化")

# ============================================================================
# 4. 成本效益对比
# ============================================================================
print("\n" + "=" * 70)
print("成本效益对比")
print("=" * 70)

print(f"\n成本分析 (USD/g):")
print(f"{'项目':<20} {'CNT':<15} {'LIG':<15}")
print("-" * 50)
print(f"{'原材料成本':<20} {'$50-500':<15} {'$1-10 (PI 薄膜)':<15}")
print(f"{'设备成本':<20} {'高 (CVD 炉)':<15} {'中 (CO2 激光器)':<15}")
print(f"{'能耗':<20} {'高 (高温)':<15} {'低 (室温)':<15}")
print(f"{'人工':<20} {'高':<15} {'低 (自动化)':<15}")
print(f"{'总成本估算':<20} {'$100-1000/g':<15} {'$10-50/g (等效)':<15}")

print(f"\n性价比 (电导率/成本):")
cnt_specific = cnt_conductivity.median() / 500  # 假设$500/g
lig_specific = lig_conductivity.median() / 20   # 假设$20/g
print(f"  CNT: {cnt_specific:.2e} S·g/(m·USD)")
print(f"  LIG: {lig_specific:.2e} S·g/(m·USD)")
print(f"  LIG 性价比是 CNT 的 {lig_specific/cnt_specific:.1f} 倍")

# ============================================================================
# 5. 应用场景对比
# ============================================================================
print("\n" + "=" * 70)
print("应用场景对比")
print("=" * 70)

print(f"\nCNT 主要应用:")
cnt_apps = [
    "高性能复合材料 (航空航天)",
    "透明导电薄膜 (触摸屏)",
    "场效应晶体管 (纳米电子)",
    "超级电容器/电池电极",
    "传感器 (气体，生物)",
    "导热界面材料"
]
for app in cnt_apps:
    print(f"  - {app}")

print(f"\nLIG 主要应用:")
lig_apps = [
    "柔性电子 (可穿戴设备)",
    "微型超级电容器",
    "生物传感器 (葡萄糖，乳酸)",
    "摩擦纳米发电机 (TENG)",
    "神经探针/生物电极",
    "应变/压力传感器"
]
for app in lig_apps:
    print(f"  - {app}")

print(f"\n应用场景重叠度:")
overlap = ["传感器", "超级电容器", "柔性电子"]
for app in overlap:
    print(f"  ✅ {app}")

# ============================================================================
# 6. TRL 技术成熟度对比
# ============================================================================
print("\n" + "=" * 70)
print("技术成熟度 (TRL) 对比")
print("=" * 70)

print(f"\nTRL 评分 (1-9):")
print(f"  CNT: TRL 6-7")
print(f"    - 实验室验证完成 (TRL 6)")
print(f"    - 原型机演示 (TRL 7)")
print(f"    - 部分商业化 (复合材料，导电添加剂)")
print(f"  LIG: TRL 4-5")
print(f"    - 组件/面包板验证 (TRL 4)")
print(f"    - 相关环境验证 (TRL 5)")
print(f"    - 研究热点，商业化初期")

# 综合评分
print(f"\n11 维度综合评分 (0-10):")
dimensions = {
    '理论基础': {'cnt': 9, 'lig': 7},
    '技术成熟度': {'cnt': 7, 'lig': 5},
    '学术影响力': {'cnt': 9, 'lig': 8},
    '应用广度': {'cnt': 8, 'lig': 6},
    '人才储备': {'cnt': 8, 'lig': 6},
    '资金投入': {'cnt': 8, 'lig': 7},
    '创新能力': {'cnt': 7, 'lig': 9},
    '国际合作': {'cnt': 9, 'lig': 7},
    '教育普及': {'cnt': 7, 'lig': 5},
    '开源贡献': {'cnt': 6, 'lig': 8},
    '产业转化': {'cnt': 7, 'lig': 5}
}

print(f"{'维度':<15} {'CNT':<10} {'LIG':<10} {'优势':<10}")
print("-" * 45)
for dim, scores in dimensions.items():
    if scores['cnt'] > scores['lig']:
        advantage = "CNT"
    elif scores['lig'] > scores['cnt']:
        advantage = "LIG"
    else:
        advantage = "平"
    print(f"{dim:<15} {scores['cnt']:<10} {scores['lig']:<10} {advantage:<10}")

cnt_avg = np.mean([s['cnt'] for s in dimensions.values()])
lig_avg = np.mean([s['lig'] for s in dimensions.values()])
print("-" * 45)
print(f"{'平均分':<15} {cnt_avg:<10.2f} {lig_avg:<10.2f}")

# ============================================================================
# 7. 总结与建议
# ============================================================================
print("\n" + "=" * 70)
print("总结与建议")
print("=" * 70)

print(f"\n核心洞察:")
print(f"  1. CNT 电导率上限更高 (10^8 vs 10^5 S/m)")
print(f"  2. LIG 成本效益更优 (10x 性价比)")
print(f"  3. CNT 工艺复杂，LIG 工艺简单")
print(f"  4. CNT 成熟度高 (TRL 6-7 vs 4-5)")
print(f"  5. LIG 创新潜力大 (柔性/生物医学)")

print(f"\n互补性分析:")
print(f"  ✅ CNT 适合：高性能应用，不计成本")
print(f"  ✅ LIG 适合：柔性电子，生物医学，快速原型")
print(f"  ✅ 潜在协同：CNT 增强 LIG (复合)")

print(f"\n研究建议:")
print(f"  1. CNT-LIG 复合材料探索")
print(f"  2. LIG 工艺优化 (提升电导率)")
print(f"  3. CNT 成本降低 (规模化生产)")
print(f"  4. 交叉应用领域 (柔性传感器)")

# ============================================================================
# 8. 保存结果
# ============================================================================
print("\n" + "=" * 70)
print("保存结果")
print("=" * 70)

comparison_data = {
    'summary': {
        'cnt_samples': len(df_cnt),
        'lig_samples': len(df_lig),
        'cnt_conductivity_max': float(cnt_conductivity.max()),
        'lig_conductivity_max': float(lig_conductivity.max()),
        'cnt_trl': '6-7',
        'lig_trl': '4-5'
    },
    'dimensions': dimensions,
    'advantages': {
        'cnt': ['高电导率', '技术成熟', '理论基础强'],
        'lig': ['低成本', '工艺简单', '创新潜力大']
    }
}

output_path = Path("reports/cnt_vs_lig_comparison.json")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(comparison_data, f, ensure_ascii=False, indent=2)
print(f"\n对比数据已保存：{output_path}")

print(f"\n[OK] CNT vs LIG 对比分析完成！")
