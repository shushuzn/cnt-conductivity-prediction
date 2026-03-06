# CNT 数据提取模板

**版本:** V1  
**日期:** 2026-03-06

---

## 📋 提取字段

### 文献信息

| 字段 | 说明 | 示例 |
|------|------|------|
| paper_id | 唯一标识 | CNT_001 |
| title | 论文标题 | ... |
| authors | 作者列表 | ... |
| journal | 期刊名 | Carbon |
| year | 发表年份 | 2024 |
| doi | DOI | 10.1016/j.carbon.2024... |

---

### 结构参数

| 字段 | 单位 | 说明 | 必填 |
|------|------|------|------|
| diameter | nm | 碳管直径 | ✅ |
| length | μm | 碳管长度 | ✅ |
| layers | - | 层数 (SWCNT=1, MWCNT=n) | ✅ |
| chirality_n | - | 手性 (n,m)，如未知填 NA | ⏳ |
| chirality_m | - | 手性 (n,m)，如未知填 NA | ⏳ |
| purity | % | 纯度 | ⏳ |

---

### 制备参数

| 字段 | 单位 | 说明 | 必填 |
|------|------|------|------|
| method | - | 制备方法 (CVD/电弧/激光) | ✅ |
| cvd_temperature | °C | CVD 温度 | ⏳ |
| catalyst | - | 催化剂类型 (Fe/Co/Ni 等) | ⏳ |
| carbon_source | - | 碳源 (CH4/C2H2/CO 等) | ⏳ |
| growth_time | min | 生长时间 | ⏳ |
| pressure | Pa | 反应压力 | ⏳ |
| carrier_gas | - | 载气 (Ar/H2/N2 等) | ⏳ |

---

### 性能指标

| 字段 | 单位 | 说明 | 必填 |
|------|------|------|------|
| conductivity | S/m | 电导率 | ✅ |
| tensile_strength | GPa | 拉伸强度 | ⏳ |
| youngs_modulus | GPa | 杨氏模量 | ⏳ |
| measurement_method | - | 测量方法 (四探针等) | ⏳ |

---

## 📊 CSV 格式

```csv
paper_id,diameter_nm,length_um,layers,method,cvd_temperature_C,catalyst,carbon_source,growth_time_min,conductivity_Sm,tensile_strength_GPa,youngs_modulus_GPa,notes
CNT_001,2.5,100,1,CVD,800,Fe,CH4,30,1.2e6,50,1000,pristine
CNT_002,5.0,50,5,CVD,750,Co,C2H2,20,8.5e5,45,900,doped
...
```

---

## 🔍 数据来源优先级

1. **实验论文** - 直接测量数据 (最高优先级)
2. **综述论文** - 汇总数据 (需核实原始来源)
3. **模拟论文** - 计算数据 (标注为 simulation)
4. **数据集论文** - 已整理的数据集 (最高效率)

---

## ⚠️ 注意事项

1. **单位统一:**
   - 电导率：统一转换为 S/m
   - 长度：nm 和 μm 注意区分
   - 温度：统一为 °C

2. **数据质量:**
   - 优先选择明确报告误差范围的数据
   - 注意区分单根 CNT vs CNT 薄膜/阵列
   - 标注是否经过后处理

3. **排除标准:**
   - 数据不完整
   - 无法确定制备参数
   - 明显异常值 (需核实)

---

## 📝 提取工具

### 推荐工具

| 工具 | 用途 | 链接 |
|------|------|------|
| Zotero | 文献管理 | zotero.org |
| Excel/Sheets | 数据录入 | - |
| Tabula | PDF 表格提取 | tabula.technology |
| WebPlotDigitizer | 图表数据提取 | arohatgi.info/WebPlotDigitizer |

---

*创建日期：2026-03-06*
