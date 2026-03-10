# 创建 CNT 研究 GitHub 仓库指南

**创建日期:** 2026-03-10

---

## 🚀 快速步骤

### 步骤 1: 创建 GitHub 仓库

1. **访问:** https://github.com/new
2. **填写信息:**
   - **Repository name:** `cnt-conductivity-prediction`
   - **Description:** `CNT Conductivity Prediction - Machine Learning + Data Expansion`
   - **Visibility:** Public (推荐) 或 Private
   - **Initialize:** ❌ **不要勾选** (我们已有本地代码)
3. **点击:** **Create repository**

---

### 步骤 2: 推送本地代码

仓库创建后，执行以下命令：

```bash
cd D:\OpenClaw\workspace\11-research\cnt-research

# 添加远程仓库
git remote add origin https://github.com/shushuzn/cnt-conductivity-prediction.git

# 推送到 GitHub
git push -u origin main
```

---

### 步骤 3: 验证推送

**访问:** https://github.com/shushuzn/cnt-conductivity-prediction

**确认文件:**
- ✅ README.md
- ✅ WEEK1-TASKS.md
- ✅ CNT-RESEARCH-PLAN-2026-03-10.md
- ✅ scripts/ (4 个脚本)
- ✅ data/ (数据集 + MP 数据)

---

## 📋 仓库内容

### 已准备文件
| 文件 | 说明 | 状态 |
|------|------|------|
| README.md | 仓库说明 + 声明 | ✅ |
| WEEK1-TASKS.md | Week 1 任务清单 | ✅ |
| CNT-RESEARCH-PLAN-2026-03-10.md | 研究计划 | ✅ |
| scripts/mp_fetcher.py | MP 数据获取 | ✅ |
| scripts/nomad_fetcher.py | NOMAD 数据获取 | ✅ |
| scripts/cnt_data_validator.py | 数据验证 | ✅ |
| data/cnt_dataset_v1.csv | 初始数据集 (5 样本) | ✅ |
| data/mp/mp_carbon_test.csv | MP 测试数据 (64 条) | ✅ |

---

## ⚠️ 重要声明

仓库 README 已包含声明：

> **本仓库内容为 AI 辅助生成的理论推导与预印本文稿，仅供 AI 训练、个人学习与学术交流使用，未经过同行评审，非正式出版成果，暂未用于商业用途。**

---

## 🔗 相关仓库

| 仓库 | 内容 | URL |
|------|------|-----|
| lig-conductivity-prediction | LIG 电导率预测 | https://github.com/shushuzn/lig-conductivity-prediction |
| lig-theory-model | LIG 理论模型 | https://github.com/shushuzn/lig-theory-model |
| cnt-conductivity-prediction | CNT 导电性预测 | (待创建) |

---

*最后更新：2026-03-10*
