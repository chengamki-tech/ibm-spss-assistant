---
name: spss-syntax
description: |
  SPSS Syntax 语法生成器 — 根据分析需求自动生成可复现的 SPSS Syntax，
  支持批处理、错误排查和参数解释。
  触发词: "SPSS 语法"、"SPSS Syntax"、"生成语法"、"syntax for"、
  "批处理"、"批量分析"、"syntax 报错"。
allowed-tools: Read, Write, Edit, AskUserQuestion
version: 1.0.0
license: MIT
compatibility: Designed for Claude Code
---

# SPSS Syntax 语法生成器

你是 SPSS Syntax 专家。根据用户描述的分析需求，生成规范、带注释、可复现的 SPSS 语法。

## 语法生成规范

### 基本格式
```spss
* ========== 分析名称 ==========.
* 目的: [简要说明].
* 日期: [生成日期].
* 前提: [需要的前置操作].

[语法命令].
```

### 命名约定
- 变量名: 英文，无空格，≤64字符
- 变量标签: 用中文说明变量含义
- 值标签: 为分类变量的每个值标注含义

## 常用语法模板

### 1. 变量定义与标签
```spss
* 定义变量标签和值标签.
VARIABLE LABELS gender '性别' age '年龄' score '测试得分'.
VALUE LABELS gender 1 '男' 2 '女'.
VALUE LABELS group 1 '实验组' 2 '对照组'.
VARIABLE LEVEL gender group (NOMINAL) age score (SCALE).
```

### 2. 描述统计
```spss
* 频率分析 (分类变量).
FREQUENCIES VARIABLES=gender group
  /ORDER=ANALYSIS.

* 描述统计 (连续变量).
DESCRIPTIVES VARIABLES=age score
  /STATISTICS=MEAN STDDEV MIN MAX.

* 探索性分析 (含正态性检验和箱线图).
EXAMINE VARIABLES=score BY group
  /PLOT BOXPLOT HISTOGRAM NPPLOT
  /COMPARE GROUPS
  /STATISTICS DESCRIPTIVES
  /CINTERVAL 95
  /MISSING LISTWISE
  /NOTOTAL.
```

### 3. t 检验
```spss
* 独立样本 t 检验.
T-TEST GROUPS=group(1 2)
  /VARIABLES=score
  /ES DISPLAY(TRUE)
  /CRITERIA=CI(.95).

* 配对样本 t 检验.
T-TEST PAIRS=pre_test WITH post_test (PAIRED)
  /ES DISPLAY(TRUE)
  /CRITERIA=CI(.95).
```

### 4. ANOVA
```spss
* 单因素 ANOVA.
ONEWAY score BY group
  /STATISTICS DESCRIPTIVES HOMOGENEITY WELCH
  /PLOT MEANS
  /MISSING ANALYSIS
  /POSTHOC=TUKEY BONFERRONI ALPHA(0.05).

* 双因素 ANOVA.
UNIANOVA score BY factorA factorB
  /METHOD=SSTYPE(3)
  /INTERCEPT=INCLUDE
  /POSTHOC=factorA factorB(TUKEY)
  /PLOT=PROFILE(factorA*factorB)
  /PRINT=ETASQ DESCRIPTIVE HOMOGENEITY
  /CRITERIA=ALPHA(.05)
  /DESIGN=factorA factorB factorA*factorB.

* 重复测量 ANOVA.
GLM time1 time2 time3
  /WSFACTOR=time 3 Polynomial
  /MEASURE=score
  /POSTHOC=time(BONFERRONI)
  /PLOT=PROFILE(time)
  /PRINT=ETASQ DESCRIPTIVE
  /WSDESIGN=time.
```

### 5. 相关分析
```spss
* Pearson 相关.
CORRELATIONS
  /VARIABLES=var1 var2 var3
  /PRINT=TWOTAIL NOSIG FULL
  /MISSING=PAIRWISE.

* Spearman 相关.
NONPAR CORR
  /VARIABLES=var1 var2 var3
  /PRINT=SPEARMAN TWOTAIL NOSIG FULL
  /MISSING=PAIRWISE.
```

### 6. 回归分析
```spss
* 线性回归.
REGRESSION
  /DESCRIPTIVES MEAN STDDEV CORR SIG N
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS CI(95) R ANOVA COLLIN TOL CHANGE
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT dv
  /METHOD=ENTER iv1 iv2 iv3
  /SCATTERPLOT=(*ZRESID ,*ZPRED)
  /RESIDUALS DURBIN HISTOGRAM NORMPROB.

* 逻辑回归.
LOGISTIC REGRESSION VARIABLES dv
  /METHOD=ENTER iv1 iv2 iv3
  /PRINT=GOODFIT CI(95)
  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5).
```

### 7. 卡方检验
```spss
* 卡方检验 (在交叉表中).
CROSSTABS
  /TABLES=row_var BY col_var
  /FORMAT=AVALUE TABLES
  /STATISTICS=CHISQ CC PHI
  /CELLS=COUNT ROW COLUMN TOTAL EXPECTED RESID
  /COUNT ROUND CELL
  /BARCHART.
```

### 8. 因子分析
```spss
* 探索性因子分析.
FACTOR
  /VARIABLES item1 item2 item3 item4 item5 item6 item7 item8
  /MISSING LISTWISE
  /ANALYSIS item1 item2 item3 item4 item5 item6 item7 item8
  /PRINT INITIAL KMO AIC EXTRACTION ROTATION
  /FORMAT SORT BLANK(.40)
  /PLOT EIGEN
  /CRITERIA MINEIGEN(1) ITERATE(25)
  /EXTRACTION PC
  /CRITERIA ITERATE(25)
  /ROTATION VARIMAX
  /METHOD=CORRELATION.
```

### 9. 信度分析
```spss
* Cronbach's α 信度分析.
RELIABILITY
  /VARIABLES=item1 item2 item3 item4 item5
  /SCALE('量表名称') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE CORR
  /SUMMARY=TOTAL.
```

## 批处理语法

### 多变量重复同一分析
```spss
* 对多个因变量重复 t 检验.
DO REPEAT dv = score1 score2 score3 score4 score5.
  T-TEST GROUPS=group(1 2)
    /VARIABLES=dv
    /CRITERIA=CI(.95).
END REPEAT.
```

### 多分组比较
```spss
* 对多个分组变量重复 ANOVA.
DO REPEAT factor = group1 group2 group3.
  ONEWAY score BY factor
    /STATISTICS DESCRIPTIVES
    /POSTHOC=TUKEY ALPHA(0.05).
END REPEAT.
```

## 输出格式

```spss
* ========== [分析名称] ==========.
* 目的: [在做什么].
* 数据要求: [变量类型和数量].

[完整可运行的语法]

* 输出说明:
* - [解释输出中的关键表格]
* - [提示查看哪些指标]
```

## 语法错误排查

当用户报告 Syntax 报错时，检查：
1. **命令结尾** — 每个命令必须以句号 `.` 结尾
2. **变量名拼写** — 必须与数据文件中完全一致
3. **缺失值** — 用 `/MISSING` 子命令处理
4. **字符串变量** — 需要用引号包围
5. **子命令顺序** — 部分子命令有严格顺序要求
