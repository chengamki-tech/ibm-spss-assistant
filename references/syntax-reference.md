# 常用 SPSS Syntax 速查

## 通用规则

- 每个命令以句号 `.` 结尾
- `*` 开头的行是注释
- 命令关键字不区分大小写
- 变量名必须与数据文件中完全一致

---

## 数据管理

### 打开/保存文件
```spss
* 打开数据文件.
GET FILE='C:\data\mydata.sav'.

* 保存数据文件.
SAVE OUTFILE='C:\data\cleaned.sav'.

* 导入 Excel.
GET DATA /TYPE=XLSX
  /FILE='C:\data\mydata.xlsx'
  /SHEET=name 'Sheet1'
  /CELLRANGE=FULL
  /READNAMES=ON.

* 导入 CSV.
GET DATA /TYPE=TXT
  /FILE='C:\data\mydata.csv'
  /DELCASE=LINE
  /DELIMITERS=","
  /QUALIFIER='"'
  /ARRANGEMENT=DELIMITED
  /FIRSTCASE=2
  /VARIABLES=var1 A10 var2 F5.2 var3 F3.0.
```

### 变量操作
```spss
* 添加变量标签.
VARIABLE LABELS gender '性别' age '年龄' score '测试得分'.

* 添加值标签.
VALUE LABELS gender 1 '男' 2 '女'.
VALUE LABELS group 1 '实验组' 2 '对照组' 3 '控制组'.

* 设置测量层次.
VARIABLE LEVEL gender group (NOMINAL).
VARIABLE LEVEL likert1 likert2 (ORDINAL).
VARIABLE LEVEL age score (SCALE).

* 重命名变量.
RENAME VARIABLES (old_name = new_name).

* 计算新变量.
COMPUTE total = SUM(item1 TO item10).
COMPUTE mean_score = MEAN(item1 TO item10).
COMPUTE age_group = 1.
IF (age >= 26) age_group = 2.
IF (age >= 36) age_group = 3.
EXECUTE.

* 条件重编码.
RECODE score (LOWEST THRU 59=1)(60 THRU 79=2)(80 THRU HIGHEST=3) INTO level.
EXECUTE.

* 反向计分.
RECODE item3 item5 item7 (1=5)(2=4)(3=3)(4=2)(5=1).
EXECUTE.
```

### 个案筛选
```spss
* 选择个案.
SELECT IF (gender = 1).
EXECUTE.

* 条件选择.
USE ALL.
FILTER BY group.
EXECUTE.

* 加权个案.
WEIGHT BY freq_var.

* 拆分文件 (按组分别分析).
SORT CASES BY group.
SPLIT FILE LAYERED BY group.

* 取消拆分.
SPLIT FILE OFF.
```

---

## 描述统计

```spss
* 频率分析.
FREQUENCIES VARIABLES=gender education
  /BARCHART FREQ
  /ORDER=ANALYSIS.

* 描述统计.
DESCRIPTIVES VARIABLES=age score
  /STATISTICS=MEAN STDDEV MIN MAX.

* 探索性分析.
EXAMINE VARIABLES=score BY group
  /PLOT BOXPLOT HISTOGRAM NPPLOT
  /COMPARE GROUPS
  /STATISTICS DESCRIPTIVES
  /CINTERVAL 95
  /MISSING LISTWISE
  /NOTOTAL.

* 交叉表.
CROSSTABS
  /TABLES=gender BY education
  /FORMAT=AVALUE TABLES
  /STATISTICS=CHISQ CC PHI
  /CELLS=COUNT ROW COLUMN TOTAL
  /BARCHART.
```

---

## 比较均值

```spss
* 单样本 t 检验.
T-TEST
  /TESTVAL=50
  /VARIABLES=score
  /CRITERIA=CI(.95).

* 独立样本 t 检验.
T-TEST GROUPS=group(1 2)
  /VARIABLES=score
  /ES DISPLAY(TRUE)
  /CRITERIA=CI(.95).

* 配对样本 t 检验.
T-TEST PAIRS=pre_test WITH post_test (PAIRED)
  /ES DISPLAY(TRUE)
  /CRITERIA=CI(.95).

* 单因素 ANOVA.
ONEWAY score BY group
  /STATISTICS DESCRIPTIVES HOMOGENEITY WELCH
  /PLOT MEANS
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

---

## 相关分析

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

---

## 回归分析

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

* 逐步回归.
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF R ANOVA CHANGE
  /CRITERIA=PIN(.05) POUT(.10)
  /DEPENDENT dv
  /METHOD=STEPWISE(iv1 iv2 iv3 iv4).

* 层次回归.
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF R ANOVA CHANGE
  /CRITERIA=PIN(.05) POUT(.10)
  /DEPENDENT dv
  /METHOD=ENTER control1 control2
  /METHOD=ENTER iv1 iv2.

* 逻辑回归.
LOGISTIC REGRESSION VARIABLES dv
  /METHOD=ENTER iv1 iv2 iv3
  /PRINT=GOODFIT CI(95)
  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5).
```

---

## 因子分析

```spss
* 探索性因子分析.
FACTOR
  /VARIABLES item1 TO item12
  /MISSING LISTWISE
  /PRINT INITIAL KMO AIC EXTRACTION ROTATION
  /FORMAT SORT BLANK(.40)
  /PLOT EIGEN
  /CRITERIA MINEIGEN(1) ITERATE(25)
  /EXTRACTION PC
  /CRITERIA ITERATE(25)
  /ROTATION VARIMAX
  /METHOD=CORRELATION.
```

---

## 信度分析

```spss
* Cronbach's α.
RELIABILITY
  /VARIABLES=item1 TO item12
  /SCALE('量表名称') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE CORR
  /SUMMARY=TOTAL.

* 分维度信度.
RELIABILITY
  /VARIABLES=item1 item2 item3 item4
  /SCALE('维度1') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE CORR
  /SUMMARY=TOTAL.
```

---

## 非参数检验

```spss
* Mann-Whitney U (两独立样本).
NPTESTS
  /INDEPENDENT TEST (score) GROUP (group) MANN_WHITNEY
  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE.

* Kruskal-Wallis (多独立样本).
NPTESTS
  /INDEPENDENT TEST (score) GROUP (group) KRUSKAL_WALLIS(COMPARE=PAIRWISE)
  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE.

* Wilcoxon (两配对样本).
NPTESTS
  /RELATED TEST(pre_test post_test) WILCOXON
  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE.

* Friedman (多配对样本).
NPTESTS
  /RELATED TEST(time1 time2 time3) FRIEDMAN(COMPARE=PAIRWISE)
  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE.
```

---

## 批处理技巧

```spss
* 对多个变量重复同一分析.
DO REPEAT dv = score1 score2 score3 score4 score5.
  T-TEST GROUPS=group(1 2)
    /VARIABLES=dv
    /CRITERIA=CI(.95).
END REPEAT.

* 循环生成多个图表.
GRAPH
  /BAR(SIMPLE)=MEAN BY group BY var.
* 重复以上命令，替换 var 即可.
```

---

## 输出管理

```spss
* 将输出导出为 HTML.
OUTPUT EXPORT
  /CONTENTS EXPORT=ALL
  /HTML DOCUMENTFILE='C:\output\results.html'.

* 将输出导出为 Word.
OUTPUT EXPORT
  /CONTENTS EXPORT=ALL
  /DOCX DOCUMENTFILE='C:\output\results.docx'.

* 将图表导出为图片.
OUTPUT EXPORT
  /CONTENTS EXPORT=ALL
  /PNG IMAGFILE='C:\output\chart.png'.
```
