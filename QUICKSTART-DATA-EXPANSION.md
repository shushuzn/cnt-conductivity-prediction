# CNT 数据扩充 - 快速开始指南

**更新日期:** 2026-03-10  
**目标:** 5 → 300+ 样本 (第一周 150+)

---

## 🚀 快速开始

### 步骤 1: 安装依赖

```bash
pip install pandas numpy requests mp-api
```

### 步骤 2: 配置 API Key (Materials Project)

```bash
# 获取 API Key: https://materialsproject.org/openid-connect/login
setx MP_API_KEY "your_actual_api_key"
```

### 步骤 3: 运行数据获取

```bash
cd 11-research/cnt-research

# NOMAD 数据 (无需 API Key)
py scripts/nomad_fetcher.py --query "carbon nanotube" --limit 100

# Materials Project 数据 (需要 API Key)
py scripts/mp_fetcher.py --query "carbon nanotube"

# 数据验证
py scripts/cnt_data_validator.py --input data/cnt_dataset_v1.csv --output data/validation_report.md
```

---

## 📊 数据来源

| 来源 | 目标样本 | 优先级 | API Key | 状态 |
|------|----------|--------|---------|------|
| 文献提取 | 200 | 🔴 HIGH | 否 | 手动 |
| NOMAD | 50 | 🟡 MEDIUM | 否 | ✅ 就绪 |
| Materials Project | 30 | 🟡 MEDIUM | 是 | ✅ 就绪 |
| 已有数据 | 5 | ✅ | - | ✅ 完成 |

---

## 🔧 脚本说明

### nomad_fetcher.py
**功能:** 从 NOMAD Repository 获取 CNT 计算数据  
**输入:** 搜索关键词  
**输出:** `data/nomad/nomad_cnt_data_YYYYMMDD_HHMMSS.csv`  
**字段:** entry_id, title, band_gap, n_atoms, dimensionality 等

**示例:**
```bash
py scripts/nomad_fetcher.py --query "carbon nanotube" --limit 100
```

### mp_fetcher.py
**功能:** 从 Materials Project 获取材料数据  
**输入:** 搜索关键词 + API Key  
**输出:** `data/mp/mp_cnt_data_YYYYMMDD_HHMMSS.csv`  
**字段:** material_id, formula, band_gap, density, elements 等

**示例:**
```bash
py scripts/mp_fetcher.py --query "carbon nanotube"
```

### cnt_data_validator.py
**功能:** 数据质量验证  
**输入:** CSV 数据文件  
**输出:** Markdown 验证报告  
**验证项:** 范围检查/完整性/异常值检测

**示例:**
```bash
py scripts/cnt_data_validator.py --input data/cnt_dataset_v2.csv
```

---

## 📈 数据合并流程

```bash
# 1. 获取各来源数据
py scripts/nomad_fetcher.py
py scripts/mp_fetcher.py

# 2. 手动提取文献数据 (使用 cnt_data_extractor.py)

# 3. 合并数据集 (待创建合并脚本)
# 4. 数据验证
py scripts/cnt_data_validator.py --input data/cnt_dataset_merged.csv

# 5. 发布新版本数据集
# data/cnt_dataset_v2.csv
```

---

## 🎯 第一周目标

| 日期 | 任务 | 目标样本 | 累计 |
|------|------|----------|------|
| 3/10 | 研究启动 ✅ | 5 | 5 |
| 3/11 | NOMAD + MP 获取 | 80 | 85 |
| 3/12 | 文献提取 | 120 | 205 |
| 3/13 | 数据验证 | - | 205 |
| 3/14 | 周总结 | ≥150 | ≥150 |

---

## ⚠️ 注意事项

1. **API 配额:** Materials Project 有请求限制，分批获取
2. **数据去重:** 合并时检查重复记录
3. **质量优先:** 宁可少提，不可错提
4. **及时备份:** 每次更新前备份数据集

---

## 🔗 相关资源

- [NOMAD API](https://nomad-lab.eu/production/REPO/docs/api/)
- [Materials Project API](https://materialsproject.org/api)
- [CNT Research Plan](CNT-RESEARCH-PLAN-2026-03-10.md)
- [Week 1 Tasks](WEEK1-TASKS.md)

---

*最后更新：2026-03-10*
