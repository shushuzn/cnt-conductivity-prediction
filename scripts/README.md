# CNT 研究脚本说明

**位置:** `cnt-research/scripts/`

---

## 📜 脚本清单

### 已完成

| 脚本 | 功能 | 状态 |
|------|------|------|
| `cnt_shap_analysis.py` | SHAP 可解释性分析 | ✅ 完成 |
| `cnt_gp_run.py` | GP 模型训练和评估 | ✅ 完成 |

### 待创建

| 脚本 | 功能 | 优先级 |
|------|------|--------|
| `cnt_feature_selection.py` | 特征选择和分析 | 🟡 中 |
| `cnt_feature_selection.py` | 特征选择和分析 | 🟡 中 |
| `cnt_data_visualization.py` | 数据探索性分析 | 🟡 中 |
| `cnt_baseline_comparison.py` | 基准模型对比 | 🟢 低 |

---

## 🔧 使用说明

### cnt_shap_analysis.py

**用途:** SHAP 可解释性分析（当前使用示例数据）

**运行:**
```bash
py scripts/cnt_shap_analysis.py
```

**输出:**
- `figures/cnt_shap_feature_importance.png` - 特征重要性
- `figures/cnt_shap_dependence_*.png` - SHAP 依赖图 (5 个)
- `figures/cnt_shap_force_plot.png` - 单个样本解释

**下一步:** 替换为真实 CNT 数据集

---

### cnt_gp_run.py (待创建)

**用途:** GP 模型训练和评估

**功能:**
- 加载 CNT 数据集
- GP 模型训练
- 交叉验证
- 性能评估 (R², MAE, RMSE)
- 保存模型

**预计创建时间:** 数据收集完成后

---

### cnt_feature_selection.py (待创建)

**用途:** 特征选择

**方法:**
- 相关性分析
- 递归特征消除 (RFE)
- 基于 GP 长度尺度
- SHAP 值分析

**输出:** 最终特征子集

---

## 📊 数据流程

```
文献数据 → 数据提取 → cnt_dataset_v1.csv
                      ↓
              cnt_gp_run.py (训练模型)
                      ↓
              cnt_feature_selection.py (特征选择)
                      ↓
              cnt_shap_analysis.py (可解释性)
                      ↓
              图表 + 物理解释 → 论文
```

---

## 📝 创建顺序

1. ✅ `cnt_shap_analysis.py` - 已完成
2. 🔴 `cnt_data_visualization.py` - 数据收集后创建
3. 🔴 `cnt_gp_run.py` - 数据收集后创建
4. 🟡 `cnt_feature_selection.py` - 模型训练后创建
5. 🟢 `cnt_baseline_comparison.py` - 可选

---

*最后更新：2026-03-06 19:40*
