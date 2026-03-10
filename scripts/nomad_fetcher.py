#!/usr/bin/env python3
"""
NOMAD 数据获取脚本
从 NOMAD Repository 获取 CNT 相关计算数据

Usage:
    py nomad_fetcher.py --query "carbon nanotube" --limit 100

Dependencies:
    pip install requests pandas

API Docs:
    https://nomad-lab.eu/production/
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

print("=" * 70)
print("NOMAD 数据获取脚本")
print("=" * 70)

# ============================================================================
# 配置
# ============================================================================
OUTPUT_DIR = Path("D:/OpenClaw/workspace/11-research/cnt-research/data/nomad")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NOMAD_API_BASE = "https://nomad-lab.eu/production/repo/api/v1"
QUERY = "carbon nanotube"
LIMIT = 100

# ============================================================================
# NOMAD API 查询
# ============================================================================
def search_nomad(query, limit=100):
    """搜索 NOMAD 数据库"""
    print(f"\n🔍 搜索 NOMAD: '{query}' (limit={limit})")
    
    url = f"{NOMAD_API_BASE}/entries"
    params = {
        'q': query,
        'limit': limit,
        'include': 'metadata'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        print(f"   ✅ 找到 {len(data.get('entries', []))} 条记录")
        return data.get('entries', [])
    
    except Exception as e:
        print(f"   ❌ 错误：{e}")
        return []

# ============================================================================
# 数据提取
# ============================================================================
def extract_cnt_data(entries):
    """从 NOMAD 数据中提取 CNT 相关参数"""
    extracted = []
    
    for entry in entries:
        try:
            metadata = entry.get('metadata', {})
            
            # 提取关键信息
            record = {
                'source': 'NOMAD',
                'entry_id': entry.get('entry_id', ''),
                'title': metadata.get('title', ''),
                'year': metadata.get('year', None),
                'material': metadata.get('material', {}).get('name', ''),
                
                # 结构参数
                'dimensionality': metadata.get('structure', {}).get('dimensionality', None),
                'n_atoms': metadata.get('structure', {}).get('n_atoms', None),
                
                # 电子性质
                'band_gap': metadata.get('electronic', {}).get('band_gap', None),
                'is_metal': metadata.get('electronic', {}).get('is_metal', None),
                
                # 提取时间
                'extracted_at': datetime.now().isoformat()
            }
            
            extracted.append(record)
        
        except Exception as e:
            print(f"   ⚠️ 提取失败：{e}")
            continue
    
    return extracted

# ============================================================================
# 主流程
# ============================================================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="NOMAD 数据获取")
    parser.add_argument('--query', type=str, default=QUERY, help='搜索关键词')
    parser.add_argument('--limit', type=int, default=LIMIT, help='结果数量限制')
    args = parser.parse_args()
    
    # 搜索
    entries = search_nomad(args.query, args.limit)
    
    if not entries:
        print("\n❌ 未找到数据")
        exit(1)
    
    # 提取
    print("\n📝 提取数据...")
    extracted = extract_cnt_data(entries)
    
    # 保存
    output_file = OUTPUT_DIR / f"nomad_cnt_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    if extracted:
        df = pd.DataFrame(extracted)
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"\n✅ 数据已保存：{output_file}")
        print(f"   记录数：{len(df)}")
        print(f"   列：{', '.join(df.columns)}")
        
        # 统计
        print(f"\n📊 数据统计:")
        if 'band_gap' in df.columns:
            print(f"   Band Gap: {df['band_gap'].mean():.3f} eV (mean)")
        if 'n_atoms' in df.columns:
            print(f"   Atoms: {df['n_atoms'].mean():.1f} (mean)")
    else:
        print("\n❌ 无有效数据")
