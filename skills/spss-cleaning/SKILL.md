---
name: spss-cleaning
description: |
  SPSS 数据清洗检查 — 缺失值分析、异常值检测、变量类型检查、
  编码一致性验证、重复样本检查，并生成对应的 SPSS Syntax。
  触发词: "数据清洗"、"缺失值"、"异常值"、"data cleaning"、"data check"、
  "数据预处理"、"数据准备"。
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
version: 1.0.0
license: MIT
compatibility: Designed for Claude Code
---

# SPSS 数据清洗检查

你是数据质量检查专家。帮用户在正式分析前发现并解决数据问题。

## 清洗检查流程

### 1. 变量类型检查

确认每个变量的测量层次设置正确：

```spss
* 查看所有变量的测量层次.
DISPLAY DICTIONARY.
```

**常见错误**：
- 数值型分类变量被设为 Scale → 应为 Nominal 或 Ordinal
- 字符串变量需要转为数值型才能分析
- 日期变量格式不统一

**修正语法**：
```spss
* 修正变量测量层次.
VARIABLE LEVEL gender group (NOMINAL).
VARIABLE LEVEL likert1 likert2 likert3 (ORDINAL).
VARIABLE LEVEL age income score (SCALE).
```

### 2. 缺失值分析

**第一步：查看缺失情况**
```spss
* 各变量缺失值频率.
FREQUENCIES VARIABLES=ALL
  /ORDER=ANALYSIS.

* 缺失值模式分析 (需要 Missing Values Analysis 模块).
MVA VARIABLES=var1 var2 var3 var4 var5
  /MAXCAT=25
  /CROSSTAB
  /TPATTERN.
```

**第二步：判断缺失类型**
- **完全随机缺失 (MCAR)**: Little's MCAR 检验不显著 → 可删除
- **随机缺失 (MAR)**: 与其他变量有关 → 可用多重插补
- **非随机缺失 (MNAR)**: 与缺失值本身有关 → 需谨慎处理

**第三步：处理方案**

| 缺失比例 | 建议处理 |
|---------|---------|
| < 5% | 列表删除 (listwise) 即可 |
| 5-15% | 均值插补或回归插补 |
| 15-25% | 多重插补 |
| > 25% | 考虑删除该变量 |

**插补语法**：
```spss
* 均值插补 (简单但降低方差).
RECODE var1 (MISSING=MEAN(var1)).

* 多重插补 (推荐).
MULTIPLE IMPUTATION var1 var2 var3
  /IMPUTE METHOD=AUTO NIMPUTATIONS=5
  /MISSINGSUMMARIES NONE
  /OUTFILE IMPUTATIONS=imputed_data.
```

### 3. 异常值检测

**方法一：描述统计初筛**
```spss
DESCRIPTIVES VARIABLES=age income score
  /STATISTICS=MEAN STDDEV MIN MAX.
```
看最小值和最大值是否在合理范围内。

**方法二：箱线图法 (IQR 法)**
```spss
EXAMINE VARIABLES=score
  /PLOT BOXPLOT HISTOGRAM
  /STATISTICS EXTREME
  /MISSING LISTWISE.
```
超过 Q1-1.5×IQR 或 Q3+1.5×IQR 为异常值。

**方法三：Z-score 法**
```spss
* 计算 Z 分数.
DESCRIPTIVES VARIABLES=score
  /SAVE
  /STATISTICS=MEAN STDDEV.

* 筛选 |Z| > 3 的个案.
SELECT IF (ABS(Zscore) > 3).
LIST VARIABLES=id score Zscore.
```

**异常值处理**：
- 首先检查是否为录入错误 → 修正
- 若为真实极端值 → 可 Winsorize 或转换
- 不建议直接删除，除非确认是错误

```spss
* Winsorize: 将极端值限制在 P5-P95.
RANK VARIABLES=score (A) /PERCENTILES=5 95.
* 根据百分位数进行截断处理.
```

### 4. 编码一致性检查

```spss
* 检查分类变量的编码是否一致.
FREQUENCIES VARIABLES=gender education level
  /ORDER=ANALYSIS.

* 检查反向题是否需要反转.
RECODE item3 item5 item7 (1=5)(2=4)(3=3)(4=2)(5=1) INTO r_item3 r_item5 r_item7.
EXECUTE.
```

**检查项**：
- 同一变量是否有多种编码（如 1=男 / M=男 混用）
- 反向计分题是否已反转
- 用户缺失值编码是否统一（如 99, 999, -1）

### 5. 重复样本检查

```spss
* 按关键变量检查重复.
SORT CASES BY id(A).
MATCH FILES /FILE=* /BY id /FIRST=first_dup /LAST=last_dup.
SELECT IF (first_dup=0 OR last_dup=0).
LIST VARIABLES=id first_dup last_dup.

* 或使用数据校验功能.
DATA VALIDATION
  /RULES CHECKS=id DUPLICATE
  /SAVE DUPLICATES.
```

## 完整清洗脚本模板

```spss
* ========== 数据清洗流程 ==========.
* Step 1: 查看数据概况.
DISPLAY DICTIONARY.
FREQUENCIES VARIABLES=ALL.

* Step 2: 检查并修正变量类型.
VARIABLE LEVEL gender group (NOMINAL).
VARIABLE LEVEL age score (SCALE).

* Step 3: 缺失值分析.
DESCRIPTIVES VARIABLES=ALL
  /STATISTICS=MEAN STDDEV MIN MAX.

* Step 4: 异常值检测.
EXAMINE VARIABLES=age income score
  /PLOT BOXPLOT
  /STATISTICS EXTREME.

* Step 5: 编码检查.
FREQUENCIES VARIABLES=gender education.

* Step 6: 重复检查.
SORT CASES BY id(A).
MATCH FILES /FILE=* /BY id /FIRST=first.
FREQUENCIES VARIABLES=first.

* Step 7: 清洗后保存.
SAVE OUTFILE='cleaned_data.sav'.
```

## 输出格式

```
### 🧹 数据清洗报告

**数据概况**: N = [样本量], 变量数 = [数量]

**发现的问题**:
1. [问题描述] — [处理建议]
2. ...

**生成的清洗语法**:
[完整可运行的 SPSS Syntax]

**清洗后检查项**:
- [ ] 确认缺失值处理合理
- [ ] 确认异常值已处理
- [ ] 保存清洗后的数据文件
```
