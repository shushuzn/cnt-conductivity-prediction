# CNT 数据提取工具 - 快速入门指南

**创建日期:** 2026-03-06  
**工具:** `cnt-research/scripts/cnt_data_extractor.py`

---

## 🚀 快速开始

### 方法 1: 运行工具

```bash
cd D:\OpenClaw\workspace\11-research\cnt-research
py scripts\cnt_data_extractor.py
```

**主菜单:**
```
[1] 手动录入模式    - 逐篇论文录入数据
[2] 批量导入模式    - 从 Excel/CSV 导入
[3] 查看数据统计    - 查看当前数据集统计
[4] 退出
```

---

### 方法 2: 批量导入示例数据

已准备示例数据：`data/sample_dataset.csv`

**导入步骤:**
1. 运行工具
2. 选择 `[2] 批量导入模式`
3. 输入路径：`D:\OpenClaw\workspace\11-research\cnt-research\data\sample_dataset.csv`
4. 确认导入

**结果:** 5 条示例数据导入完成

---

## 📊 数据字段说明

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| paper_id | ✅ | 论文 ID | CNT_001 |
| doi | ⏳ | DOI | 10.1038/nature06964 |
| title | ⏳ | 论文标题 | ... |
| year | ⏳ | 年份 | 2024 |
| journal | ⏳ | 期刊名 | Carbon |
| diameter_nm | ✅ | 直径 (nm) | 2.5 |
| length_um | ✅ | 长度 (μm) | 100 |
| layers | ✅ | 层数 | 1 (SWCNT) |
| method | ⏳ | 制备方法 | CVD |
| cvd_temperature_C | ⏳ | CVD 温度 | 800 |
| catalyst | ⏳ | 催化剂 | Fe |
| carbon_source | ⏳ | 碳源 | CH4 |
| conductivity_Sm | ✅ | 电导率 (S/m) | 1.2e6 |
| tensile_strength_GPa | ⏳ | 拉伸强度 | 50 |
| youngs_modulus_GPa | ⏳ | 杨氏模量 | 1000 |
| notes | ⏳ | 备注 | SWCNT example |
| status | ✅ | 状态 | Extracted |

---

## 📝 手动录入流程

### 步骤 1: 选择手动录入

```
请选择 (1-4): 1
```

### 步骤 2: 逐项输入

```
录入新记录：CNT_006

DOI (可选): 10.1016/j.carbon.2024.01.001
论文标题：Electrical conductivity of carbon nanotubes...
年份：2024
期刊：Carbon
直径 (nm): 3.5
长度 (μm): 150
层数：1
制备方法：CVD
CVD 温度 (°C): 750
催化剂：Co
碳源：C2H2
电导率 (S/m): 9.5e5
拉伸强度 (GPa): 45
杨氏模量 (GPa): 950
备注 (可选): High quality sample
```

### 步骤 3: 保存

```
请选择 (1-4): 3
✓ 数据已保存
```

---

## 📈 查看统计

选择 `[3] 查看数据统计`

**输出示例:**
```
总记录数：50
已提取：45
已验证：5

数值统计:

  diameter_nm:
    最小值：1.00
    最大值：50.00
    平均值：8.50
    中位数：5.20

  conductivity_Sm:
    最小值：1.00e+05
    最大值：1.50e+07
    平均值：2.50e+06
    中位数：1.80e+06
```

---

## 💡 使用技巧

### 技巧 1: 分批录入

不要一次性录入所有数据，建议：
- 每次录入 5-10 篇论文
- 定期保存 (每录入 5 篇保存一次)
- 每天备份数据文件

### 技巧 2: 使用 Excel 预整理

1. 在 Excel 中整理数据
2. 保存为 CSV 格式
3. 使用批量导入模式

**Excel 模板:** `literature/literature_tracking.xlsx`

### 技巧 3: 数据验证

录入后检查：
- 直径范围：1-50 nm (合理范围)
- 电导率范围：10⁴-10⁷ S/m (合理范围)
- 层数：1=SWCNT, >1=MWCNT

### 技巧 4: 备份

工具会自动备份，但建议：
- 每天手动备份到云盘
- 使用版本控制 (Git)
- 定期导出为 Excel 备份

---

## ⚠️ 常见问题

### Q: 数据文件在哪里？

**A:** `cnt-research/data/cnt_dataset_v1.csv`

### Q: 如何恢复备份？

**A:** 
```bash
# 找到最新备份
data/cnt_dataset_backup_20260306_195000.csv

# 复制覆盖
copy cnt_dataset_backup_20260306_195000.csv cnt_dataset_v1.csv
```

### Q: 如何导出为 Excel？

**A:** 
```python
import pandas as pd
df = pd.read_csv('data/cnt_dataset_v1.csv')
df.to_excel('data/cnt_dataset_v1.xlsx', index=False)
```

### Q: 单位不对怎么办？

**A:** 工具会自动转换：
- 电导率：S/cm → S/m (×100)
- 长度：nm → μm (÷1000)
- 强度：MPa → GPa (÷1000)

---

## 📊 数据输出格式

**最终数据集:** `cnt_dataset_v1.csv`

**用途:**
- GP 模型训练
- 统计分析
- 论文中的数据集描述
- 上传 Zenodo

**目标:** 300+ 数据点

---

## 🔗 相关文件

| 文件 | 位置 |
|------|------|
| 提取工具 | `scripts/cnt_data_extractor.py` |
| 数据目录 | `data/` |
| 文献追踪 | `literature/literature_tracking.xlsx` |
| 提取模板 | `data/data_extraction_template.md` |

---

*创建日期：2026-03-06*  
*状态：测试完成，可以使用 ✅*
