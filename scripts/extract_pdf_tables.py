#!/usr/bin/env python3
"""
从 PDF 中提取表格数据
使用 PyMuPDF (fitz)
"""

import fitz
import pandas as pd
from pathlib import Path
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("PDF 表格提取工具")
print("=" * 70)

# PDF 路径 - 使用通配符查找
PDF_DIR = Path("D:/OpenClaw/workspace/11-research/cnt-research/literature/pdfs")
PDF_FILES = list(PDF_DIR.glob("*.pdf"))

if not PDF_FILES:
    print(f"❌ PDF 目录为空：{PDF_DIR}")
    exit(1)

# 找到最新的 PDF
PDF_PATH = max(PDF_FILES, key=lambda p: p.stat().st_mtime)
print(f"📄 使用 PDF: {PDF_PATH.name}")

print(f"\n📄 打开 PDF: {PDF_PATH.name}")
print(f"   大小：{PDF_PATH.stat().st_size / 1024 / 1024:.2f} MB")

# 打开 PDF
doc = fitz.open(PDF_PATH)
print(f"   页数：{len(doc)}")

# 提取文本（搜索表格）
print("\n🔍 搜索表格...")

all_tables = []

for page_num in range(min(len(doc), 15)):  # 前 15 页
    page = doc[page_num]
    text = page.get_text()
    
    # 搜索 Table 关键字
    if 'Table' in text or 'table' in text:
        print(f"\n   第 {page_num + 1} 页可能包含表格")
        
        # 提取包含 Table 的文本块
        blocks = page.get_text("blocks")
        for block in blocks:
            text_block = block[4] if len(block) > 4 else ""
            if 'Table' in text_block or any(x in text_block.lower() for x in ['swcnt', 'mwcnt', 'conductivity', 'strength']):
                print(f"   - {text_block[:200]}...")

# 提取所有文本
print("\n📝 提取全文文本...")
full_text = ""
for page_num in range(len(doc)):
    page = doc[page_num]
    full_text += page.get_text()

# 保存到文件
OUTPUT_TXT = PDF_PATH.parent / "meta-analysis-2021-full-text.txt"
with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
    f.write(full_text)
print(f"✅ 全文已保存：{OUTPUT_TXT}")

# 搜索电导率相关段落
print("\n🔍 搜索电导率数据...")
keywords = ['conductivity', 'S/m', 'S/cm', 'SWCNT', 'MWCNT', 'diameter', 'strength']
for kw in keywords:
    count = full_text.lower().count(kw.lower())
    print(f"   {kw}: {count} 次")

# 查找表格区域
print("\n📊 尝试提取表格数据...")

# 使用 fitz 的表格提取功能（如果可用）
try:
    tables = doc.find_tables()
    print(f"   找到 {len(tables.tables)} 个表格")
    
    for i, table in enumerate(tables.tables):
        print(f"\n   Table {i+1}:")
        df = table.to_pandas()
        print(f"   行数：{len(df)}, 列数：{len(df.columns)}")
        print(df.head())
        
        # 保存表格
        if len(df) > 2:
            output_csv = PDF_PATH.parent / f"meta-analysis-2021-table-{i+1}.csv"
            df.to_csv(output_csv, index=False)
            print(f"   ✅ 已保存：{output_csv}")
            
except Exception as e:
    print(f"   ⚠️ 表格提取失败：{e}")
    print("   尝试手动解析文本...")

doc.close()

print("\n" + "=" * 70)
print("✅ 提取完成！")
print("=" * 70)
