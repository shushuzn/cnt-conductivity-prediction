# CNT 性能预测研究

**启动日期:** 2026-03-06  
**方向:** B1 + C3 (CNT 电导率预测 + SHAP 可解释性)  
**状态:** 🚀 启动准备中

---

## 📊 研究目标

| 目标 | 值 |
|------|-----|
| 数据集规模 | 300+ 样本 |
| 模型 | GP 回归 |
| 目标 R² | > 0.75 |
| SHAP 洞见 | 3+ 关键发现 |
| 预期论文 | 2 篇 |

---

## 📁 项目结构

```
cnt-research/
├── README.md                 # 本文件
├── data/
│   ├── data_extraction_template.md   # 数据提取模板
│   └── cnt_dataset_v1.csv            # [待创建] 数据集
├── scripts/
│   ├── cnt_shap_analysis.py          # SHAP 分析
│   ├── cnt_gp_run.py                 # [待创建] GP 模型
│   └── cnt_feature_selection.py      # [待创建] 特征选择
├── figures/                          # [待创建] 图表
├── models/                           # [待创建] 模型
└── paper/
    ├── cnt_paper_draft.md            # [待创建] 论文草稿
    └── cnt_dataset_paper.md          # [待创建] 数据论文
```

---

## 🚀 快速开始

### 安装依赖

```bash
pip install shap scikit-learn pandas numpy matplotlib
```

### 测试 SHAP 分析

```bash
cd cnt-research
py scripts/cnt_shap_analysis.py
```

---

## 📋 研究计划

| 阶段 | 时间 | 任务 | 里程碑 |
|------|------|------|--------|
| 1 | W1-W2 | 文献调研 | 50 篇论文 |
| 1 | W2-W3 | 数据收集 | 300+ 数据点 |
| 2 | W4-W6 | 模型开发 | R² > 0.75 |
| 3 | W7-W8 | SHAP 分析 | 3+ 物理洞见 |
| 4 | W9-W13 | 论文撰写 | 2 篇初稿 |

**详细计划:** `../../docs/CNT_RESEARCH_PLAN.md`

---

## 📊 数据提取模板

**位置:** `data/data_extraction_template.md`

**提取字段:**
- 结构参数：直径、长度、层数、手性
- 制备参数：方法、温度、催化剂、碳源
- 性能指标：电导率、拉伸强度、杨氏模量

---

## 🔬 方法

### 模型

- **基线:** 高斯过程回归 (GP)
- **核函数:** RBF + WhiteKernel
- **评估:** R², MAE, RMSE, 95% CI 覆盖率

### 可解释性

- **方法:** SHAP (KernelSHAP)
- **分析:** 特征重要性、依赖图、交互效应
- **目标:** 发现 3+ 物理洞见

---

## 📝 预期产出

| 产出 | 数量 | 目标期刊 |
|------|------|----------|
| 数据集 | 300+ 样本 | Scientific Data |
| 预测模型 | GP, R²>0.75 | - |
| 应用论文 | 1 篇 | Carbon / ACS Nano |
| 数据论文 | 1 篇 | Scientific Data |

---

## 🔗 相关链接

| 文档 | 位置 |
|------|------|
| 研究计划 | `../../docs/CNT_RESEARCH_PLAN.md` |
| 方向总览 | `../../docs/NEXT_RESEARCH_DIRECTIONS.md` |
| 启动总结 | `../../docs/CNT_RESEARCH_STARTUP_SUMMARY.md` |

---

## 📅 进度追踪

| 日期 | 里程碑 | 状态 |
|------|--------|------|
| 2026-03-06 | 项目启动 | ✅ |
| 2026-03-06 | SHAP 测试完成 | ✅ |
| 2026-03-06 | GP 模型 Pipeline 建立 | ✅ |
| 2026-03-13 | 50 篇论文收集 | ⏳ |
| 2026-03-20 | 300+ 数据点 | ⏳ |
| 2026-04-17 | R² > 0.75 | ⏳ |
| 2026-05-01 | SHAP 分析完成 | ⏳ |
| 2026-06-05 | 论文初稿完成 | ⏳ |

---

*最后更新：2026-03-06 19:38*
