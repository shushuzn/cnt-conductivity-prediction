# CNT 导电性预测研究计划

**任务 ID:** cnt-research-001  
**启动日期:** 2026-03-10  
**预计完成:** 2026-03-31 (3 周)  
**优先级:** 🔴 HIGH

---

## 📋 研究目标

### 主要目标
1. **数据扩充:** 5 样本 → 300+ 样本 (60x)
2. **模型优化:** R² NaN → >0.75
3. **特征工程:** 4 特征 → 10+ 特征
4. **对比分析:** CNT vs LIG 性能对比

### 验收标准
| 指标 | 当前 | 目标 | 提升 |
|------|------|------|------|
| 样本数 | 5 | 300+ | 60x |
| R² | NaN | >0.75 | - |
| 特征数 | 4 | 10+ | 2.5x |
| 文献覆盖 | 0/50 | 50/50 | 100% |

---

## 📚 技术方案

### 阶段 1: 数据扩充 (Week 1-2)

**方法 A: 文献数据挖掘**
- 目标：50 篇核心论文 → 200+ 数据点
- 工具：`cnt_data_extractor.py`
- 提取参数：
  - 结构参数：直径/长度/层数/手性
  - 工艺参数：CVD 温度/催化剂/碳源
  - 性能参数：电导率/拉伸强度/杨氏模量

**方法 B: 高通量计算数据**
- 目标：DFT 计算数据 → 50+ 样本
- 来源：NOMAD/Materials Project
- 自动化：API 批量获取

**方法 C: 主动学习筛选**
- 目标：优先提取高价值样本
- 工具：`active_learning_simulator.py`
- 策略：不确定性采样 + 多样性采样

### 阶段 2: 模型优化 (Week 2)

**基线模型:** Gaussian Process (已有)
**优化方向:**
1. 特征工程
   - 添加衍生特征 (长径比/体积分数)
   - 类别特征编码 (催化剂/碳源/方法)
   - 交互特征 (温度×催化剂)

2. 模型选择
   - GP (RBF/Matern 核)
   - Random Forest
   - XGBoost
   - Neural Network (小样本友好)

3. 超参数优化
   - Grid Search
   - Bayesian Optimization
   - Cross-Validation (5-fold)

### 阶段 3: 对比分析 (Week 3)

**CNT vs LIG 对比维度:**
1. 电导率范围
2. 制造工艺复杂度
3. 成本效益分析
4. 应用场景重叠度
5. 技术成熟度 (TRL)

**产出:**
- M-Note: CNT vs LIG 跨材料对比
- 可视化：雷达图/散点图
- 洞察：优势/劣势/互补性

---

## 📁 文件结构

```
11-research/cnt-research/
├── data/
│   ├── cnt_dataset_v1.csv          # 当前数据集 (5 样本)
│   ├── cnt_dataset_v2.csv          # [目标] 扩充后 (300+ 样本)
│   └── extraction/                  # 文献提取数据
├── models/
│   ├── CNT_GP_v1.pkl               # 当前 GP 模型
│   ├── CNT_GP_v2.pkl               # [目标] 优化后模型
│   ├── CNT_RF_v1.pkl               # Random Forest
│   └── CNT_XGB_v1.pkl              # XGBoost
├── scripts/
│   ├── cnt_data_extractor.py       # 数据提取
│   ├── cnt_gp_baseline.py          # GP 基线
│   ├── cnt_model_comparison.py     # [新增] 模型对比
│   └── active_learning_simulator.py # 主动学习
├── figures/                         # 可视化图表
├── literature/                      # 文献追踪
└── reports/                         # 研究报告
    ├── CNT-Progress-Weekly.md      # 周报
    └── CNT-Final-Report.md         # [目标] 最终报告
```

---

## 📈 实施步骤

### Week 1: 数据扩充启动
- [ ] Day 1-2: 文献数据提取 (20 篇 → 80 样本)
- [ ] Day 3-4: 高通量数据获取 (50 样本)
- [ ] Day 5: 数据清洗 + 合并

### Week 2: 模型优化
- [ ] Day 6-7: 特征工程 (4→10+ 特征)
- [ ] Day 8-9: 多模型训练 (GP/RF/XGB)
- [ ] Day 10: 超参数优化 + 交叉验证

### Week 3: 分析总结
- [ ] Day 11-12: CNT vs LIG 对比分析
- [ ] Day 13: 撰写 M-Note
- [ ] Day 14: 最终报告 + Git 提交

---

## 📊 每周里程碑

| 周次 | 目标 | 验收标准 |
|------|------|----------|
| Week 1 | 数据扩充 | 样本数≥150 |
| Week 2 | 模型优化 | R²≥0.60 |
| Week 3 | 分析总结 | M-Note 完成 |

---

## 🔗 相关资源

### 数据集
- [NOMAD Repository](https://nomad-lab.eu/) - 计算材料数据
- [Materials Project](https://materialsproject.org/) - 材料特性
- [Nanohub](https://nanohub.org/) - 纳米材料数据

### 文献检索
- Google Scholar: "carbon nanotube electrical conductivity"
- Web of Science: CNT + conductivity + fabrication
- Scopus: CNT + electrical properties

### 工具
- `cnt_data_extractor.py` - 数据提取脚本
- `active_learning_simulator.py` - 主动学习
- `cnt_gp_baseline.py` - GP 模型基线

---

## 📝 进度日志

### 2026-03-10 (Day 1) - 研究启动
- ✅ 现有资产分析完成
- ✅ 研究计划制定
- ✅ 任务清单创建
- ⏸️ 等待数据提取启动

**当前状态:**
- 样本数：5
- R²: NaN (样本不足)
- 文献收集：0/50

---

*最后更新：2026-03-10*
