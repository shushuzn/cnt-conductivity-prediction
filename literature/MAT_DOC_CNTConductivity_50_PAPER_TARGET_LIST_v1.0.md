# 50 篇 LIG 论文目标列表

**创建日期:** 2026-03-06  
**目标:** 从 50 篇论文提取 500+ 样本数据  
**用途:** Nature 级别升级 - 阶段 1 数据扩充

---

## 📚 论文列表 (按优先级排序)

### 优先级 1: 高引用综述 (5 篇) ⭐⭐⭐⭐⭐

| # | 论文 | 年份 | 引用 | 数据量预估 |
|---|------|------|------|------------|
| 1 | Tour JM. Laser-induced graphene: from discovery to translation | 2019 | 2000+ | 50+ 样本 |
| 2 | Lin J et al. Laser-induced porous graphene films from commercial polymers | 2014 | 3000+ | 30+ 样本 |
| 3 | Chyan Y et al. Laser-induced graphene by multiple lasing | 2018 | 1500+ | 40+ 样本 |
| 4 | Zhang W et al. Laser-induced graphene: from fundamentals to applications | 2021 | 800+ | 60+ 样本 |
| 5 | Guo Z et al. Laser-induced graphene for flexible electronics and sensors | 2020 | 600+ | 30+ 样本 |

**检索链接:**
```
https://scholar.google.com/scholar?q=Laser-induced+graphene+Tour+review+2019
https://scholar.google.com/scholar?q=Laser-induced+porous+graphene+Lin+Nature+2014
https://scholar.google.com/scholar?q=Laser-induced+graphene+multiple+lasing+Chyan+2018
https://scholar.google.com/scholar?q=Laser-induced+graphene+fundamentals+applications+Zhang+2021
https://scholar.google.com/scholar?q=Laser-induced+graphene+flexible+electronics+sensors+Guo+2020
```

---

### 优先级 2: 电导率优化论文 (15 篇) ⭐⭐⭐⭐⭐

| # | 关键词 | 年份范围 | 数据量预估 |
|---|--------|----------|------------|
| 6-10 | LIG electrical conductivity optimization | 2019-2024 | 100+ 样本 |
| 11-15 | LIG conductivity laser parameters | 2018-2023 | 100+ 样本 |
| 16-20 | LIG electrical properties laser power speed | 2017-2023 | 100+ 样本 |

**批量检索:**
```
https://scholar.google.com/scholar?q=LIG+electrical+conductivity+optimization+laser+parameters+2019..2024
https://scholar.google.com/scholar?q=laser-induced+graphene+conductivity+laser+power+scanning+speed+2018..2023
https://scholar.google.com/scholar?q=laser-induced+graphene+electrical+properties+process+parameters+2017..2023
```

---

### 优先级 3: 工艺参数研究 (15 篇) ⭐⭐⭐⭐

| # | 关键词 | 年份范围 | 数据量预估 |
|---|--------|----------|------------|
| 21-25 | LIG laser power density conductivity | 2018-2024 | 80+ 样本 |
| 26-30 | LIG scanning speed electrical properties | 2017-2023 | 80+ 样本 |
| 31-35 | LIG multi-pass laser conductivity | 2019-2024 | 60+ 样本 |

**批量检索:**
```
https://scholar.google.com/scholar?q=LIG+laser+power+density+electrical+conductivity+2018..2024
https://scholar.google.com/scholar?q=laser-induced+graphene+scanning+speed+electrical+2017..2023
https://scholar.google.com/scholar?q=laser-induced+graphene+multi-pass+lasing+conductivity+2019..2024
```

---

### 优先级 4: 特殊条件研究 (10 篇) ⭐⭐⭐⭐

| # | 关键词 | 年份范围 | 数据量预估 |
|---|--------|----------|------------|
| 36-40 | LIG controlled atmosphere conductivity | 2018-2024 | 50+ 样本 |
| 41-45 | LIG heated substrate electrical properties | 2019-2024 | 50+ 样本 |

**批量检索:**
```
https://scholar.google.com/scholar?q=laser-induced+graphene+controlled+atmosphere+electrical+2018..2024
https://scholar.google.com/scholar?q=laser-induced+graphene+heated+substrate+electrical+conductivity+2019..2024
```

---

### 优先级 5: 数据集/汇总论文 (5 篇) ⭐⭐⭐⭐⭐

| # | 关键词 | 数据量预估 |
|---|--------|------------|
| 46-50 | LIG dataset database machine learning | 200+ 样本 |

**检索:**
```
https://scholar.google.com/scholar?q=laser-induced+graphene+dataset+database+machine+learning+2020..2024
```

---

## 📊 数据提取目标

| 优先级 | 论文数 | 目标样本数 | 截止时间 |
|--------|--------|------------|----------|
| 优先级 1 | 5 篇 | 200+ 样本 | Week 1 |
| 优先级 2 | 15 篇 | 300+ 样本 | Week 2 |
| 优先级 3 | 15 篇 | 200+ 样本 | Week 3 |
| 优先级 4 | 10 篇 | 100+ 样本 | Week 4 |
| 优先级 5 | 5 篇 | 200+ 样本 | Week 2 |
| **总计** | **50 篇** | **1000+ 样本** | **Week 4** |

---

## 📝 提取流程

### 步骤 1: 获取论文 (Day 1-2)

1. 点击上述检索链接
2. 下载 PDF (通过机构订阅或 ResearchGate)
3. 保存到 `cnt-research/literature/pdfs/`
4. 记录到追踪表

### 步骤 2: 数据提取 (Day 3-14)

使用工具：`cnt-research/scripts/cnt_data_extractor.py`

**提取字段:**
- 直径/厚度 (nm/μm)
- 激光功率 (W)
- 扫描速度 (mm/s)
- 功率密度 (J/cm²)
- 扫描次数
- 电导率 (S/m)
- 环境气氛
- 基底温度

### 步骤 3: 质量检查 (Day 15-20)

- 检查数据范围合理性
- 单位统一转换
- 去除重复数据
- 标注数据来源

### 步骤 4: 数据分析 (Day 21-28)

- 统计分布
- 相关性分析
- 可视化图表
- 准备论文使用

---

## 📈 进度追踪

| 日期 | 获取论文数 | 提取样本数 | 累计样本数 | 状态 |
|------|------------|------------|------------|------|
| Day 1 | 10 | 0 | 0 | ⏳ |
| Day 2 | 20 | 0 | 0 | ⏳ |
| Day 3 | 30 | 50 | 50 | ⏳ |
| Day 4 | 40 | 100 | 150 | ⏳ |
| Day 5 | 50 | 100 | 250 | ⏳ |
| Day 7 | 50 | 150 | 400 | ⏳ |
| Day 10 | 50 | 200 | 600 | ⏳ |
| Day 14 | 50 | 400 | 1000+ | ✅ |

---

## 🔗 快速检索入口

### 全部 LIG 电导率论文
```
https://scholar.google.com/scholar?q=laser-induced+graphene+electrical+conductivity+properties+2017..2024
```

### 全部 LIG 工艺参数论文
```
https://scholar.google.com/scholar?q=laser-induced+graphene+laser+parameters+power+speed+conductivity+2018..2024
```

### 全部 LIG 优化论文
```
https://scholar.google.com/scholar?q=laser-induced+graphene+optimization+electrical+conductivity+2019..2024
```

---

## 💡 提取技巧

### 技巧 1: 优先提取数据表

- 查找论文中的 Tables
- 优先提取有具体数值的表格
- 注意单位转换

### 技巧 2: 图表数据提取

使用 WebPlotDigitizer:
```
https://automeris.io/WebPlotDigitizer/
```

### 技巧 3: 批量处理

- 使用 Excel 模板批量录入
- 5 篇论文一批次
- 定期保存备份

---

## ✅ 质量标准

### 纳入标准
- ✅ 明确报告电导率值
- ✅ 提供激光参数 (功率、速度等)
- ✅ 实验论文 (非纯模拟)

### 排除标准
- ❌ 数据不完整
- ❌ 无法确定参数
- ❌ 明显异常值

---

*创建日期：2026-03-06*  
*目标：50 篇论文 → 1000+ 样本*  
*状态：准备就绪，开始获取！*
