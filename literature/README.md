# CNT 文献收集中心

**启动日期:** 2026-03-06  
**目标:** 50 篇核心论文 → 300+ 数据点 → GP 模型 R² > 0.75

---

## 📚 快速开始

### 第一步：阅读策略文档

1. **检索策略:** `SEARCH_GUIDE.md` - 如何高效检索
2. **周计划:** `WEEKLY_PLAN.md` - 每日任务分解
3. **起点论文:** `starter_papers.md` - 高优先级论文列表

### 第二步：准备工具

- [ ] Zotero (文献管理) - https://zotero.org
- [ ] Excel/Google Sheets (数据提取)
- [ ] Tabula (PDF 表格提取) - https://tabula.technology
- [ ] WebPlotDigitizer (图表数据) - https://automeris.io/WebPlotDigitizer

### 第三步：开始检索

**今日任务 (Day 1):**
- 浏览 100+ 论文标题
- 保存 10+ 篇核心论文
- 下载 5 篇 PDF

---

## 📁 文件结构

```
literature/
├── README.md                      # 本文件 (快速开始)
├── starter_papers.md              # 起点论文列表 ⭐
├── SEARCH_GUIDE.md                # 检索实操指南
├── WEEKLY_PLAN.md                 # 周计划分解
├── literature_tracking.xlsx       # 进度追踪表
└── pdfs/                          # [待创建] 下载的 PDF
    ├── Datasets/
    ├── Reviews/
    └── Experimental/
```

---

## 🎯 目标

| 指标 | 目标值 | 截止时间 |
|------|--------|----------|
| 核心论文 | 50 篇 | Week 2 |
| 数据点 | 300+ | Week 3 |
| 直径覆盖 | 1-50 nm | - |
| 长度覆盖 | 1-500 μm | - |
| 电导率覆盖 | 10⁴-10⁷ S/m | - |

---

## 📊 进度追踪

### 累计统计

| 日期 | 论文数 | 数据点数 | 状态 |
|------|--------|----------|------|
| 2026-03-06 | 10 | 0 | ✅ Day 1 完成 |
| 2026-03-07 | - | - | ⏳ Day 2 |
| 2026-03-08 | - | - | ⏳ Day 3 |
| ... | ... | ... | ... |

### 数据分布 (实时更新)

| 参数 | 范围 | 当前覆盖 | 状态 |
|------|------|----------|------|
| 直径 | 1-50 nm | - | ⏳ |
| 长度 | 1-500 μm | - | ⏳ |
| 层数 | 1-20 | - | ⏳ |
| 电导率 | 10⁴-10⁷ S/m | - | ⏳ |

---

## 🔍 检索入口

### 直接链接

| 平台 | 链接 | 访问 |
|------|------|------|
| Google Scholar | https://scholar.google.com | 免费 |
| Web of Science | https://www.webofscience.com | 需订阅 |
| Scopus | https://www.scopus.com | 需订阅 |
| arXiv | https://arxiv.org | 免费 |

### 检索式 (复制即用)

**Google Scholar:**
```
"carbon nanotube" electrical conductivity data
```

**Web of Science:**
```
TS=("carbon nanotube*" OR CNT) AND TS=("electrical conductivity" OR "electronic properties")
```

---

## 📝 数据提取

### 提取模板

见 `literature_tracking.xlsx`

**必填字段:**
- paper_id: CNT_001, CNT_002...
- doi: 永久标识符
- diameter_nm: 直径 (nm)
- length_um: 长度 (μm)
- layers: 层数 (SWCNT=1)
- conductivity_Sm: 电导率 (S/m)

### 单位转换

| 原始单位 | 目标单位 | 转换 |
|----------|----------|------|
| S/cm | S/m | × 100 |
| nm | nm | 不变 |
| μm | μm | 不变 |
| MPa | GPa | ÷ 1000 |

---

## ✅ 质量检查

### 纳入标准

- ✅ 明确报告电导率/力学性能
- ✅ 提供结构参数 (直径、层数)
- ✅ 同行评议或预印本

### 排除标准

- ❌ 数据不完整
- ❌ 纯模拟无实验
- ❌ 无法获取全文

---

## 📞 帮助

### 常见问题

**Q: 论文只给图表怎么办？**  
A: 使用 WebPlotDigitizer 提取数据

**Q: 单位不统一怎么办？**  
A: 使用转换表统一为标准单位

**Q: 数据不完整怎么办？**  
A: 标注"部分数据"，优先级降低

---

## 🔗 相关文档

| 文档 | 位置 |
|------|------|
| 研究计划 | `../../docs/CNT_RESEARCH_PLAN.md` |
| 方向总览 | `../../docs/NEXT_RESEARCH_DIRECTIONS.md` |
| 数据模板 | `../data/data_extraction_template.md` |

---

*最后更新：2026-03-06 19:45*  
*状态：准备就绪，开始检索 🚀*
