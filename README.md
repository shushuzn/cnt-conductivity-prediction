# CNT 导电性预测研究

## ⚠️ 重要声明
**本仓库内容为 AI 辅助生成的理论推导与预印本文稿，仅供 AI 训练、个人学习与学术交流使用，未经过同行评审，非正式出版成果，暂未用于商业用途。**

---

## 📊 研究目标

**目标:** 建立 CNT 导电性预测模型  
**方法:** 机器学习 (GP/RF/XGB) + 数据扩充  
**时间:** 2026-03-10 至 2026-03-31

### Week 1 目标 (2026-03-10 ~ 03-14)
- 数据扩充：5 样本 → 150 样本
- 来源：文献提取 (200) + NOMAD (50) + Materials Project (30)

---

## 📁 目录结构

```
cnt-research/
├── README.md                    # 本文件
├── WEEK1-TASKS.md              # Week 1 任务清单
├── CNT-RESEARCH-PLAN-2026-03-10.md  # 研究计划
├── data/
│   ├── cnt_dataset_v1.csv      # 初始数据集 (5 样本)
│   ├── mp/                     # Materials Project 数据
│   └── nomad/                  # NOMAD 数据
├── scripts/
│   ├── cnt_data_extractor.py   # 数据提取
│   ├── cnt_data_validator.py   # 数据验证
│   ├── mp_fetcher.py           # MP 数据获取
│   └── nomad_fetcher.py        # NOMAD 数据获取
└── models/                     # 模型文件
```

---

## 🚀 快速开始

### 安装依赖
```bash
pip install pandas numpy scikit-learn mp-api
```

### 获取 Materials Project 数据
```bash
py scripts/mp_fetcher.py --query "carbon nanotube"
```

### 数据验证
```bash
py scripts/cnt_data_validator.py --input data/cnt_dataset_v1.csv
```

---

## 📈 当前进度

| 任务 | 状态 | 完成度 |
|------|------|--------|
| 研究计划 | ✅ 完成 | 100% |
| 工具开发 | ✅ 完成 | 100% |
| MP 数据获取 | ✅ 测试成功 | 64 条记录 |
| NOMAD 数据获取 | ⏸️ 待认证 | 0% |
| 文献提取 | ⏸️ 待开始 | 0% |
| 数据集 v2 | ⏸️ 待发布 | 0% |

---

## 📧 联系

**作者:** shushuzn  
**邮箱:** [待填写]

---

*最后更新：2026-03-10*
