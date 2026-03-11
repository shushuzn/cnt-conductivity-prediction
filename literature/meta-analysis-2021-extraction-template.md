# CNT Meta-Analysis 2021 数据提取模板

**论文：** A meta-analysis of conductive and strong carbon nanotube materials  
**作者：** JS Bulmer, A Kaniyoor, JA Elliott  
**期刊：** Advanced Materials (2021)  
**引用：** 167 次  
**DOI:** 10.1002/adma.202008432

---

## 📊 待提取字段

### 核心数据（Tables）

| 字段 | 说明 | 单位 | 目标列名 |
|------|------|------|----------|
| 材料类型 | SWCNT/MWCNT/Graphene/Fiber | - | material_type |
| 直径 | 纳米管/纤维直径 | nm | diameter_nm |
| 长度 | 纳米管/纤维长度 | μm | length_um |
| 层数 | SWCNT=1, MWCNT=n | - | layers |
| 电导率 | 电导率值 | S/m | conductivity_Sm |
| 拉伸强度 | 拉伸强度 | GPa | tensile_strength_GPa |
| 杨氏模量 | 弹性模量 | GPa | youngs_modulus_GPa |
| 密度 | 材料密度 | g/cm³ | density |
| 制备方法 | CVD/电弧/激光/纺丝等 | - | method |
| 数据来源 | 原始文献引用 | - | source_reference |

### 辅助数据（Figures）

- Figure X: 电导率 vs 密度散点图
- Figure Y: 强度 vs 模量对比图
- Figure Z: 不同材料类型性能分布

**工具：** WebPlotDigitizer (https://automeris.io/WebPlotDigitizer/)

---

## 📝 提取记录

### Table 1: CNT 电导率汇总
| 样本 ID | 材料类型 | 直径 | 长度 | 层数 | 电导率 | 方法 | 来源 |
|---------|----------|------|------|------|--------|------|------|
| MA-001 | SWCNT | | | | | | |
| MA-002 | MWCNT | | | | | | |

### Table 2: CNT 力学性能汇总
| 样本 ID | 材料类型 | 直径 | 长度 | 层数 | 拉伸强度 | 杨氏模量 | 方法 | 来源 |
|---------|----------|------|------|------|----------|----------|------|------|
| MA-001 | SWCNT | | | | | | | |

### Figure 数据提取
| 图号 | 数据点数 | 提取状态 | 备注 |
|------|----------|----------|------|
| Fig 1 | - | ⏳ | 电导率 vs 密度 |
| Fig 2 | - | ⏳ | 强度 vs 模量 |

---

## 🔗 快速链接

- **PDF:** https://advanced.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/adma.202008432
- **HTML:** https://advanced.onlinelibrary.wiley.com/doi/abs/10.1002/adma.202008432
- **Google Scholar:** https://scholar.google.com/scholar?q=10.1002/adma.202008432

---

## 💡 提取技巧

### 技巧 1: 优先提取 Tables
- 查找论文中的 Table 1, Table 2 等
- 直接复制数值到 Excel
- 注意单位转换

### 技巧 2: Figure 数据提取
使用 WebPlotDigitizer:
1. 上传论文截图
2. 设置 X/Y 轴范围
3. 自动/手动提取数据点
4. 导出 CSV

### 技巧 3: 单位统一
- 电导率：S/cm → S/m (×100)
- 直径：nm 保持不变
- 长度：μm 保持不变
- 强度/模量：GPa 保持不变

---

## ✅ 质量标准

### 纳入标准
- ✅ 明确报告电导率或力学性能
- ✅ 提供结构参数 (直径、层数等)
- ✅ 实验数据 (非纯模拟)

### 排除标准
- ❌ 数据不完整
- ❌ 无法确定参数
- ❌ 明显异常值

---

## 📈 目标

**从此论文提取：**
- Tables: 50-100 样本
- Figures: 50-100 样本
- **总计：100-200 真实样本**

**预期 R²提升：**
- 当前：0.441 (Ridge, 合成数据)
- 目标：0.65-0.75 (加入真实数据)

---

*创建日期：2026-03-11*  
*状态：等待 PDF 下载*
