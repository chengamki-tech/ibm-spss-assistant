# 问卷分析标准流程

## 问卷分析完整路线图

```
数据录入 → 数据清洗 → 信度分析 → 效度分析 → 描述统计
→ 差异分析 → 相关分析 → 回归分析 → 报告撰写
```

---

## 第一阶段：数据准备

### 数据录入规范

| 编码类型 | 示例 | 说明 |
|---------|------|------|
| 人口学变量 | gender: 1=男, 2=女 | 用数字编码，加值标签 |
| 李克特量表 | 1=非常不同意 ~ 5=非常同意 | 保持编码一致 |
| 反向计分题 | 用 RECODE 反转 | 信度分析前必须处理 |
| 多选题 | 每个选项一个变量 | 0=未选, 1=已选 |

### 反向计分处理

```spss
* 假设 item3, item5, item7 为反向题.
RECODE item3 item5 item7 (1=5)(2=4)(3=3)(4=2)(5=1) INTO r_item3 r_item5 r_item7.
EXECUTE.

* 或直接覆盖原变量.
RECODE item3 item5 item7 (1=5)(2=4)(3=3)(4=2)(5=1).
EXECUTE.
```

### 量表分维度汇总

```spss
* 计算各维度均分.
COMPUTE emo_score = MEAN(r_item3, item1, item2, item4).
COMPUTE cog_score = MEAN(item5, item6, item7, item8).
COMPUTE beh_score = MEAN(item9, item10, item11, item12).
EXECUTE.

* 或计算总分.
COMPUTE total_score = SUM(item1 TO item12).
EXECUTE.
```

---

## 第二阶段：信度分析

### Cronbach's α 信度系数

```spss
* 整体信度.
RELIABILITY
  /VARIABLES=item1 TO item12
  /SCALE('整体量表') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE CORR
  /SUMMARY=TOTAL.

* 各维度信度.
RELIABILITY
  /VARIABLES=item1 item2 item3 item4
  /SCALE('情感维度') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE CORR
  /SUMMARY=TOTAL.

RELIABILITY
  /VARIABLES=item5 item6 item7 item8
  /SCALE('认知维度') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE CORR
  /SUMMARY=TOTAL.
```

### 信度判断标准

| Cronbach's α | 判断 | 行动 |
|--------------|------|------|
| ≥ .90 | 优秀 | 无需修改 |
| .80 - .89 | 良好 | 可以接受 |
| .70 - .79 | 可接受 | 考虑改进 |
| .60 - .69 | 勉强接受 | 需要修改 |
| < .60 | 不可接受 | 必须修改量表 |

### 删题判断

- "删除该项后的 α" > 整体 α → 考虑删除
- CITC (校正项总相关) < .30 → 考虑删除
- 删除后 α 上升幅度 > .02 → 建议删除

---

## 第三阶段：效度分析

### 内容效度
- 专家评审 (定性描述即可)
- 在方法部分说明

### 结构效度 — 探索性因子分析

```spss
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

### 效度判断标准

| 指标 | 标准 | 说明 |
|------|------|------|
| KMO | > .70 | 适合做因子分析 |
| Bartlett | p < .05 | 变量间有共同因子 |
| 因子载荷 | > .40 | 题项归属该因子 |
| 累计方差解释率 | > 60% | 因子解释力足够 |
| 交叉载荷 | < .40 | 题项不跨因子 |

---

## 第四阶段：描述统计

### 人口学变量频率分析

```spss
FREQUENCIES VARIABLES=gender age education income
  /BARCHART FREQ
  /ORDER=ANALYSIS.
```

### 量表得分描述统计

```spss
DESCRIPTIVES VARIABLES=emo_score cog_score beh_score total_score
  /STATISTICS=MEAN STDDEV MIN MAX SKEWNESS KURTOSIS.
```

### 描述统计表模板

```
表 1  各变量描述统计结果 (N = xxx)
───────────────────────────────────────────
变量          n      %      M      SD
───────────────────────────────────────────
性别
  男          xx    xx.xx
  女          xx    xx.xx
年龄
  18-25岁     xx    xx.xx
  26-35岁     xx    xx.xx
学历
  本科        xx    xx.xx
  研究生      xx    xx.xx
量表得分
  情感维度                      x.xx   x.xx
  认知维度                      x.xx   x.xx
  行为维度                      x.xx   x.xx
  总分                          x.xx   x.xx
───────────────────────────────────────────
```

---

## 第五阶段：差异分析

### 两组比较 (t 检验)

```spss
* 性别差异.
T-TEST GROUPS=gender(1 2)
  /VARIABLES=emo_score cog_score beh_score total_score
  /ES DISPLAY(TRUE)
  /CRITERIA=CI(.95).
```

### 多组比较 (ANOVA)

```spss
* 年龄差异.
ONEWAY emo_score cog_score beh_score BY age_group
  /STATISTICS DESCRIPTIVES HOMOGENEITY WELCH
  /PLOT MEANS
  /POSTHOC=TUKEY BONFERRONI ALPHA(0.05).

* 学历差异.
ONEWAY emo_score cog_score beh_score BY education
  /STATISTICS DESCRIPTIVES HOMOGENEITY WELCH
  /PLOT MEANS
  /POSTHOC=GAMESHOWELL ALPHA(0.05).
```

---

## 第六阶段：相关分析

```spss
* 各维度间相关.
CORRELATIONS
  /VARIABLES=emo_score cog_score beh_score total_score
  /PRINT=TWOTAIL NOSIG FULL
  /MISSING=PAIRWISE.

* 与外部变量相关 (如有).
CORRELATIONS
  /VARIABLES=emo_score cog_score beh_score age income
  /PRINT=TWOTAIL NOSIG FULL
  /MISSING=PAIRWISE.
```

### 相关矩阵表模板

```
表 X  各变量相关系数矩阵 (N = xxx)
───────────────────────────────────────────────
变量            1       2       3       4
───────────────────────────────────────────────
1. 情感维度    1
2. 认知维度    .xx**   1
3. 行为维度    .xx**   .xx**   1
4. 总分        .xx**   .xx**   .xx**   1
───────────────────────────────────────────────
注: ** p < .01, * p < .05
```

---

## 第七阶段：回归分析

### 线性回归

```spss
* 以总分为因变量，各维度为自变量.
REGRESSION
  /DESCRIPTIVES MEAN STDDEV CORR SIG N
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS CI(95) R ANOVA COLLIN TOL CHANGE
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT total_score
  /METHOD=ENTER emo_score cog_score beh_score
  /SCATTERPLOT=(*ZRESID ,*ZPRED)
  /RESIDUALS DURBIN HISTOGRAM NORMPROB.
```

### 层次回归

```spss
* 第一层: 控制变量, 第二层: 核心变量.
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF R ANOVA CHANGE
  /CRITERIA=PIN(.05) POUT(.10)
  /DEPENDENT dv
  /METHOD=ENTER control1 control2
  /METHOD=ENTER iv1 iv2 iv3.
```

---

## 常见问题处理

### 样本量不足
- 探索性因子分析: 题项数 × 5-10 倍
- 回归分析: 自变量数 × 15-20 倍
- 一般问卷: N ≥ 200 为佳

### 信度过低 (α < .70)
1. 检查是否有反向题未反转
2. 查看删题后 α，删除低 CITC 题项
3. 检查是否混入了不同维度的题项
4. 考虑增加题项

### 因子分析结果不理想
1. 检查 KMO 是否 > .70
2. 删除载荷 < .40 的题项后重新分析
3. 尝试不同的旋转方法 (Varimax vs Promax)
4. 考虑调整因子数量

### 多重共线性 (VIF > 10)
1. 删除高度相关的自变量
2. 使用层次回归分步纳入
3. 考虑岭回归或主成分回归
