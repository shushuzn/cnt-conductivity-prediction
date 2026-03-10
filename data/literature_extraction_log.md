# CNT 文献数据提取日志

**启动日期:** 2026-03-10  
**目标:** 从 50 篇文献提取 200+ 样本数据  
**当前进度:** 0/50 篇 (0%)

---

## 📊 提取进度

| 日期 | 文献数 | 样本数 | 累计样本 | 备注 |
|------|--------|--------|----------|------|
| 2026-03-10 | 0 | 0 | 5 (初始) | 研究启动 |
| 2026-03-11 | - | - | - | 计划：20 篇 → 80 样本 |
| 2026-03-12 | - | - | - | 计划：30 篇 → 120 样本 |
| 2026-03-13 | - | - | - | 数据验证 + 合并 |
| 2026-03-14 | - | - | ≥150 | Week 1 目标 |

---

## 📚 待提取文献 (优先级排序)

### 优先级 1: 高引用综述 (5 篇)

- [ ] Tour JM. Laser-induced graphene: from discovery to translation (2019) - 目标：50 样本
- [ ] Lin J et al. Laser-induced porous graphene films (2014) - 目标：30 样本
- [ ] Chyan Y et al. Laser-induced graphene by multiple lasing (2018) - 目标：40 样本
- [ ] Zhang W et al. LIG: from fundamentals to applications (2021) - 目标：60 样本
- [ ] Guo Z et al. LIG for flexible electronics and sensors (2020) - 目标：30 样本

### 优先级 2: 电导率优化 (15 篇)

- [ ] LIG electrical conductivity optimization (2019-2024) - 目标：100 样本
- [ ] LIG conductivity laser parameters (2018-2023) - 目标：100 样本
- [ ] LIG electrical properties laser power speed (2017-2023) - 目标：100 样本

### 优先级 3: 工艺参数研究 (15 篇)

- [ ] LIG laser power density conductivity (2018-2024) - 目标：80 样本
- [ ] LIG scanning speed electrical properties (2017-2023) - 目标：80 样本
- [ ] LIG multi-pass laser conductivity (2019-2024) - 目标：60 样本

### 优先级 4: 特殊条件研究 (10 篇)

- [ ] LIG controlled atmosphere conductivity (2018-2024) - 目标：50 样本
- [ ] LIG heated substrate electrical properties (2019-2024) - 目标：50 样本

---

## 📝 提取记录

### 2026-03-10

**提取文献:** 0 篇  
**新增样本:** 0  
**累计样本:** 5 (初始数据集)

**备注:**
- 研究启动
- 工具准备完成
- MP 测试数据获取 (64 条碳材料记录)

### 2026-03-10 (晚间检索)

**检索平台:** Google Scholar  
**检索词:** "carbon nanotube electrical conductivity dataset"  
**结果数:** ~24,100 篇

**高价值候选论文 (优先级排序):**

| # | 标题 | 年份 | 引用 | 数据潜力 |
|---|------|------|------|----------|
| 1 | A meta-analysis of conductive and strong carbon nanotube materials | 2021 | 167 | ⭐⭐⭐⭐⭐ (compiled datasets) |
| 2 | Probing electrical transport in nanomaterials: conductivity of individual CNTs | 1996 | 1508 | ⭐⭐⭐⭐⭐ (经典论文) |
| 3 | Electronic conduction in polymers, CNTs and graphene | 2011 | 282 | ⭐⭐⭐⭐ (综述) |
| 4 | Conductivity in CNT polymer composites: model vs experiment | 2016 | 68 | ⭐⭐⭐⭐ |
| 5 | Electrical conductivity modeling of densely packed SWCNT networks | 2010 | 62 | ⭐⭐⭐⭐ |
| 6 | Multi-fidelity high-throughput optimization of P3HT-CNT | 2021 | 58 | ⭐⭐⭐⭐ (有 dataset) |
| 7 | Machine learning + high-throughput design of P3HT-CNT | 2020 | 13 | ⭐⭐⭐⭐ (ML + dataset) |

### 2026-03-10 21:04 - arXiv:2011.10382 记录完成

**检索平台:** Google Scholar  
**检索词:** "carbon nanotube electrical conductivity dataset"  
**结果数:** ~24,100 篇

**已获取论文:**
- ✅ #7 arXiv:2011.10382 - 已记录
  - **标题:** Machine learning and high-throughput robust design of P3HT-CNT composite thin films for high electrical conductivity
  - **作者:** Bash D, Cai Y, Chellappan V, et al.
  - **年份:** 2020 (arXiv)
  - **类型:** P3HT-CNT 复合材料 (非纯 CNT)
  - **数据规模:** ~160 样本/天 (高通量)
  - **电导率范围:** 最高 1200 S/cm (复合材料)
  - **关键发现:** 10% DWCNT + 长 SWCNT 混合 → 700 S/cm 局部最优
  - **适用性:** ⚠️ 复合材料数据，可作参考但非本征 CNT 电导率
  - **状态:** 已记录到日志，待决定是否提取到数据集

**下一步:** 
1. 获取 #1 meta-analysis (Advanced Materials 2021, 167 引用)
2. 继续检索纯 CNT 本征电导率数据
3. 决定是否将复合材料数据纳入数据集 (标注为 composite)

### 2026-03-10 21:14 - 精确检索完成 (第二轮)

**检索平台:** Google Scholar  
**检索词:** "carbon nanotube intrinsic electrical conductivity SWCNT MWCNT dataset"  
**结果数:** ~15,800 篇 (更精确)

**高价值候选论文 (Top 5):**

| # | 标题 | 年份 | 期刊 | 引用 | 数据潜力 |
|---|------|------|------|------|----------|
| 1 | A meta-analysis of conductive and strong carbon nanotube materials | 2021 | Advanced Materials | 167 | ⭐⭐⭐⭐⭐ 明确提到 "intrinsic electrical conductivity...datasets" |
| 2 | Electrical conductivity modeling and experimental study of densely packed SWCNT networks | 2010 | Nanotechnology | 62 | ⭐⭐⭐⭐ "intrinsic resistance of SWCNTs" |
| 3 | Modeling electrical conductivity of nanocomposites by considering CNT deformation at junctions | 2013 | J. Appl. Phys. | 106 | ⭐⭐⭐⭐ "intrinsic electrical conductivity of CNTs" |
| 4 | Intrinsic conductivity of carbon nanotubes and graphene sheets having a realistic geometry | 2015 | J. Chem. Phys. | 40 | ⭐⭐⭐⭐ 直接研究本征电导率 (模拟) |
| 5 | Uncertainties in electric circuit analysis of anisotropic electrical conductivity of CNT nanocomposites | 2022 | Polymers | 20 | ⭐⭐⭐ "intrinsic CNT conductivity" + "dataset" |

**关键发现:**
- #1 (Advanced Materials 2021) 最有希望 - snippet 明确提到汇总多个数据集
- 检索词优化有效：24,100 → 15,800 篇 (更精确)
- 多篇论文提到 "intrinsic" 本征电导率，符合研究需求

**累计候选论文:** 12 篇 (7 篇第一轮 + 5 篇第二轮)

**明日计划:**
1. 优先获取 #1 meta-analysis (Advanced Materials 2021)
2. 从综述表格中提取多源数据
3. 目标：20 篇论文 → 80+ 样本

---

## 📋 数据提取模板

对于每篇文献，提取以下信息：

```markdown
### 文献 [编号]

**标题:** [论文标题]  
**作者:** [作者列表]  
**期刊:** [期刊名]  
**年份:** [年份]  
**DOI:** [DOI 链接]

**提取数据:**
- 样本数：[X 个]
- 能量密度范围：[X-Y J/cm²]
- 扫描速度范围：[X-Y mm/s]
- 电导率范围：[X-Y S/m]

**关键发现:**
- [发现 1]
- [发现 2]

**数据质量:** ⭐⭐⭐⭐⭐ (5 星制)
```

---

*最后更新：2026-03-10*
