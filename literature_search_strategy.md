# CNT 文献检索策略

**创建日期:** 2026-03-06  
**目标:** 收集 50 篇核心论文，提取 300+ 数据点

---

## 🔍 检索式

### Web of Science / Scopus

```
#1: ("carbon nanotube*" OR CNT OR "carbon nanotubes")
#2: ("electrical conductivity" OR "electronic propert*" OR "mechanical propert*" OR "tensile strength" OR "Young's modulus")
#3: (dataset OR "data compil*" OR "data extract*" OR review OR "state of the art")

# 组合检索:
#1 AND #2 AND #3  → 数据集/综述论文

# 或者更广泛的检索:
#1 AND #2  → 所有 CNT 性能论文
```

### Google Scholar

```
"carbon nanotube" electrical conductivity dataset
"carbon nanotube" mechanical properties data
CNT conductivity prediction machine learning
```

### arXiv

```
carbon nanotube AND (conductivity OR "electronic properties")
carbon nanotube AND "machine learning"
```

---

## 📊 纳入标准

### 优先级 1: 数据集/综述论文 ⭐⭐⭐

**特征:**
- 明确提供数据表
- 汇总多篇文献数据
- 数据量大 (50+ 样本)

**示例标题:**
- "A comprehensive dataset of carbon nanotube properties"
- "Review of carbon nanotube electrical conductivity: Data and trends"

**预期产出:** 5-10 篇论文 → 200+ 数据点

---

### 优先级 2: 实验论文 ⭐⭐

**特征:**
- 报告具体电导率/力学性能值
- 提供完整制备参数
- 同行评议期刊

**目标期刊:**
- Carbon
- ACS Nano
- Nano Letters
- Advanced Materials
- Small
- Nanoscale

**预期产出:** 30-40 篇论文 → 100+ 数据点

---

### 优先级 3: 机器学习论文 ⭐

**特征:**
- 使用 ML 预测 CNT 性能
- 提供数据集描述
- 可与本研究对比

**预期产出:** 5-10 篇论文 → 方法对比

---

## 📋 数据提取清单

### 每篇论文提取

| 字段 | 必填 | 说明 |
|------|------|------|
| paper_id | ✅ | CNT_001, CNT_002... |
| doi | ✅ | 永久标识符 |
| year | ✅ | 发表年份 |
| journal | ✅ | 期刊名 |
| diameter | ✅ | 直径 (nm) |
| length | ✅ | 长度 (μm) |
| layers | ✅ | 层数 (SWCNT=1) |
| conductivity | ✅ | 电导率 (S/m) |
| method | ⏳ | 制备方法 |
| cvd_temperature | ⏳ | CVD 温度 |
| catalyst | ⏳ | 催化剂 |
| tensile_strength | ⏳ | 拉伸强度 |
| youngs_modulus | ⏳ | 杨氏模量 |

---

## 🎯 检索目标

| 阶段 | 时间 | 目标 | 累计 |
|------|------|------|------|
| 1 | Day 1-2 | 10 篇数据集论文 | 10 篇 |
| 2 | Day 3-5 | 20 篇实验论文 | 30 篇 |
| 3 | Day 6-7 | 20 篇补充论文 | 50 篇 |

**数据点目标:** 300+

---

## 📝 文献管理

### 推荐工具

| 工具 | 用途 | 链接 |
|------|------|------|
| Zotero | 文献管理 | zotero.org |
| Mendeley | 文献管理 + PDF 标注 | mendeley.com |
| Notion/Excel | 数据提取表格 | - |

### 文件夹结构

```
CNT_Literature/
├── Datasets/           # 数据集/综述论文 (Priority 1)
├── Experimental/       # 实验论文 (Priority 2)
├── ML_Papers/          # 机器学习论文 (Priority 3)
└── To_Read/            # 待筛选
```

---

## ✅ 质量控制

### 数据质量检查

1. **单位核实:** 电导率单位是否一致 (S/m vs S/cm)
2. **异常值检测:** 超出物理范围的值
3. **完整性:** 关键参数是否缺失
4. **可追溯性:** 数据来源是否清晰

### 排除标准

- ❌ 数据不完整
- ❌ 无法确定制备参数
- ❌ 明显异常值 (无法核实)
- ❌ 模拟数据 (除非明确标注)

---

## 📊 进度追踪

| 日期 | 论文数 | 数据点数 | 备注 |
|------|--------|----------|------|
| 2026-03-06 | 0 | 0 | 启动 |
| 2026-03-08 | 10 | - | 第一阶段目标 |
| 2026-03-11 | 30 | - | 第二阶段目标 |
| 2026-03-13 | 50 | 300+ | 完成目标 |

---

## 🔗 起点论文

### 建议先读 (高引用综述/数据集)

1. **[待填写]** - CNT 电导率综述
2. **[待填写]** - CNT 力学性能综述
3. **[待填写]** - CNT 数据集论文

*(开始检索后填充具体论文)*

---

*创建日期：2026-03-06*  
*状态：准备就绪*
