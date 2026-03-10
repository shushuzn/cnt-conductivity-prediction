#!/usr/bin/env python3
"""
Materials Project 数据获取脚本
从 Materials Project API 获取 CNT 相关材料数据

Usage:
    py mp_fetcher.py --query "carbon nanotube" --api_key YOUR_API_KEY

API Key:
    Get free API key from: https://materialsproject.org/openid-connect/login

Dependencies:
    pip install mp-api pandas
"""

import os
from pathlib import Path
from datetime import datetime

print("=" * 70)
print("Materials Project 数据获取脚本")
print("=" * 70)

# ============================================================================
# 配置
# ============================================================================
OUTPUT_DIR = Path("D:/OpenClaw/workspace/11-research/cnt-research/data/mp")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.getenv('MP_API_KEY', 'your_api_key_here')

# ============================================================================
# 检查 API Key
# ============================================================================
if API_KEY == 'your_api_key_here':
    print("\n⚠️  未配置 API Key!")
    print("\n获取方法:")
    print("1. 访问：https://materialsproject.org/openid-connect/login")
    print("2. 注册/登录账户")
    print("3. 在 Dashboard 获取 API Key")
    print("4. 设置环境变量：")
    print("   setx MP_API_KEY \"your_actual_api_key\"")
    print("\n或直接在脚本中修改 API_KEY 变量")
    exit(1)

# ============================================================================
# Materials Project API 查询
# ============================================================================
try:
    from mp_api.client import MPRester
    
    print(f"\n✅ MP API 库已安装")
    print(f"   API Key: {API_KEY[:10]}...")
    
except ImportError:
    print("\n❌ mp-api 未安装!")
    print("\n安装命令:")
    print("   pip install mp-api")
    exit(1)

# ============================================================================
# 主流程
# ============================================================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Materials Project 数据获取")
    parser.add_argument('--query', type=str, default='carbon nanotube', help='搜索关键词')
    parser.add_argument('--output', type=str, default=None, help='输出文件名')
    args = parser.parse_args()
    
    print(f"\n🔍 搜索 Materials Project: '{args.query}'")
    
    try:
        with MPRester(API_KEY) as mpr:
            # 搜索材料
            docs = mpr.materials.summary.search(
                formula=args.query,
                fields=['material_id', 'formula_pretty', 'structure', 
                       'band_gap', 'is_metal', 'density', 'elements']
            )
            
            print(f"   ✅ 找到 {len(docs)} 条记录")
            
            if not docs:
                print("\n❌ 未找到数据")
                exit(1)
            
            # 提取数据
            print("\n📝 提取数据...")
            extracted = []
            
            for doc in docs:
                try:
                    record = {
                        'source': 'Materials Project',
                        'material_id': doc.material_id,
                        'formula': doc.formula_pretty,
                        'band_gap': doc.band_gap,
                        'is_metal': doc.is_metal,
                        'density': doc.density,
                        'elements': ','.join(doc.elements),
                        'n_elements': len(doc.elements),
                        'extracted_at': datetime.now().isoformat()
                    }
                    extracted.append(record)
                
                except Exception as e:
                    print(f"   ⚠️ 提取失败：{e}")
                    continue
            
            # 保存
            import pandas as pd
            output_file = OUTPUT_DIR / f"mp_cnt_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            if args.output:
                output_file = Path(args.output)
            
            df = pd.DataFrame(extracted)
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            print(f"\n✅ 数据已保存：{output_file}")
            print(f"   记录数：{len(df)}")
            print(f"   列：{', '.join(df.columns)}")
            
            # 统计
            print(f"\n📊 数据统计:")
            if 'band_gap' in df.columns:
                print(f"   Band Gap: {df['band_gap'].mean():.3f} eV (mean)")
            if 'density' in df.columns:
                print(f"   Density: {df['density'].mean():.2f} g/cm³ (mean)")
            if 'n_elements' in df.columns:
                print(f"   Elements: {df['n_elements'].mean():.1f} (mean)")
    
    except Exception as e:
        print(f"\n❌ API 错误：{e}")
        print("\n请检查:")
        print("1. API Key 是否正确")
        print("2. 网络连接是否正常")
        print("3. API 配额是否用完")
