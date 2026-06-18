# SPSS Syntax 速查卡

> 精简版速查。完整语法生成请使用 `/spss-syntax` skill。

---

## 数据管理

```spss
GET FILE='data.sav'.                          * 打开文件.
SAVE OUTFILE='cleaned.sav'.                   * 保存文件.
GET DATA /TYPE=XLSX /FILE='data.xlsx'.        * 导入 Excel.
DISPLAY DICTIONARY.                           * 查看所有变量信息.

VARIABLE LABELS var1 '变量标签'.              * 变量标签.
VALUE LABELS var1 1 '是' 2 '否'.             * 值标签.
VARIABLE LEVEL var1 (NOMINAL).                * 设置测量层次.
MISSING VALUES var1 (9, 99).                  * 设定用户缺失值.

COMPUTE new = old1 + old2.                    * 计算新变量.
RECODE old (1=5)(2=4)(3=3)(4=2)(5=1).        * 反向计分.
IF (age>=18) adult=1.                         * 条件赋值.
EXECUTE.                                      * 执行计算.
```

## 描述统计

```spss
FREQUENCIES VARIABLES=var1 var2.              * 频率表.
DESCRIPTIVES VARIABLES=var1 var2.             * 均值/标准差.
EXAMINE VARIABLES=score /PLOT BOXPLOT HISTOGRAM NPPLOT.  * 探索性分析.
CROSSTABS /TABLES=var1 BY var2 /STATISTICS=CHISQ /CELLS=ROW. * 交叉表.
```

## t 检验

```spss
T-TEST GROUPS=group(1 2) /VARIABLES=score /ES DISPLAY(TRUE).           * 独立 t.
T-TEST PAIRS=pre WITH post (PAIRED) /ES DISPLAY(TRUE).                 * 配对 t.
T-TEST /TESTVAL=50 /VARIABLES=score.                                   * 单样本 t.
```

## ANOVA

```spss
ONEWAY score BY group /POSTHOC=TUKEY ALPHA(0.05).                      * 单因素.
UNIANOVA score BY fA fB /DESIGN=fA fB fA*fB.                           * 双因素.
GLM t1 t2 t3 /WSFACTOR=time 3 /WSDESIGN=time.                         * 重复测量.
```

## 非参数检验

```spss
NPTESTS /INDEPENDENT TEST(score) GROUP(group) MANN_WHITNEY.            * Mann-Whitney.
NPTESTS /INDEPENDENT TEST(score) GROUP(group) KRUSKAL_WALLIS.          * Kruskal-Wallis.
NPTESTS /RELATED TEST(t1 t2) WILCOXON.                                 * Wilcoxon.
NPTESTS /RELATED TEST(t1 t2 t3) FRIEDMAN.                              * Friedman.
```

## 相关分析

```spss
CORRELATIONS /VARIABLES=v1 v2 v3 /PRINT=TWOTAIL NOSIG.                * Pearson.
NONPAR CORR /VARIABLES=v1 v2 v3 /PRINT=SPEARMAN TWOTAIL.              * Spearman.
PARTIAL CORR /VARIABLES=v1 v2 BY control.                              * 偏相关.
```

## 回归分析

```spss
REGRESSION /DEPENDENT=dv /METHOD=ENTER iv1 iv2 iv3                     * 多元回归.
  /STATISTICS COEFF R ANOVA COLLIN TOL.

REGRESSION /DEPENDENT=dv /METHOD=ENTER c1 c2 /METHOD=ENTER iv1 iv2.   * 层次回归.

LOGISTIC REGRESSION VARIABLES dv /METHOD=ENTER iv1 iv2                 * 逻辑回归.
  /PRINT=GOODFIT CI(95).
```

## 因子分析与信度

```spss
FACTOR /VARIABLES=item1 TO item20 /EXTRACTION PC /ROTATION VARIMAX    * EFA.
  /PRINT KMO EXTRACTION ROTATION /FORMAT SORT BLANK(.40).

RELIABILITY /VARIABLES=item1 TO item10 /MODEL=ALPHA                   * 信度.
  /STATISTICS=SCALE CORR.
```

## 输出导出

```spss
OUTPUT EXPORT /CONTENTS EXPORT=VISIBLE
  /DOCX DOCUMENTFILE='results.docx'.            * 导出 Word.
OUTPUT EXPORT /CONTENTS EXPORT=VISIBLE
  /HTML DOCUMENTFILE='results.html'.            * 导出 HTML.
OUTPUT EXPORT /PNG IMAGFILE='chart.png'.         * 导出图片.
```

## 常用子命令速查

| 子命令 | 含义 | 示例 |
|--------|------|------|
| `/VARIABLES=` | 指定分析变量 | `/VARIABLES=score1 score2` |
| `/DEPENDENT=` | 因变量 | `/DEPENDENT=dv` |
| `/METHOD=ENTER` | 纳入变量 | `/METHOD=ENTER iv1 iv2` |
| `/STATISTICS=` | 输出统计量 | `/STATISTICS=MEAN STDDEV` |
| `/PLOT=` | 输出图表 | `/PLOT=BOXPLOT HISTOGRAM` |
| `/POSTHOC=` | 事后检验 | `/POSTHOC=TUKEY BONFERRONI` |
| `/MISSING=` | 缺失值处理 | `/MISSING LISTWISE` |
| `/CRITERIA=` | 分析标准 | `/CRITERIA=PIN(.05) POUT(.10)` |
| `/ES DISPLAY(TRUE)` | 效应量 | t 检验加此参数 |
| `/PRINT=` | 输出选项 | `/PRINT=TWOTAIL NOSIG` |
| `/FORMAT=` | 输出格式 | `/FORMAT=SORT BLANK(.40)` |
| `/ROTATION=` | 旋转方法 | `/ROTATION VARIMAX` |

## 批处理

```spss
DO REPEAT dv = score1 score2 score3.           * 循环多个变量.
  T-TEST GROUPS=group(1 2) /VARIABLES=dv.
END REPEAT.

SPLIT FILE LAYERED BY group.                   * 按组分别分析.
SPLIT FILE OFF.                                * 取消拆分.
```
