# SPSS 高级分析程序完整指南

> 覆盖 IBM SPSS Statistics 全部分析程序。每个程序包含：适用场景、SPSS 路径、关键语法、输出解读、论文表述。

---

## 一、聚类分析 (Classify)

### 1.1 K-Means 快速聚类

**适用场景**：将个案分为预设数量的组，适用于大样本、连续变量。

**SPSS 路径**：`Analyze → Classify → K-Means Cluster`

**语法**：
```spss
QUICK CLUSTER var1 var2 var3 var4
  /MISSING=LISTWISE
  /CRITERIA=CLUSTER(3) MXITER(100) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /SAVE CLUSTER DISTANCE
  /PRINT INITIAL ANOVA CLUSTER DISTAN.
```

**关键输出**：
- 初始聚类中心 / 最终聚类中心
- ANOVA 表：各变量在聚类间的 F 值（越大说明该变量区分力越强）
- 每个聚类的样本量

**确定 K 值的方法**：
- 理论依据
- 层次聚类先探索
- 肘部法则 (Elbow)：尝试不同 K，看总组内平方和的拐点
- SPSS 的 TwoStep 自动确定

**论文表述**：
```
采用 K-Means 快速聚类分析，基于 [变量1]、[变量2]、[变量3]
对 [N] 名被试进行分类。根据 [确定K值的方法]，
最终确定聚类数为 [K]。聚类结果表明，[描述各聚类特征]。
ANOVA 结果显示，[变量X] 的 F 值最大 (F = [值])，
说明该变量对聚类的区分贡献最大。
```

### 1.2 层次聚类

**适用场景**：探索性分析，不确定分几组，样本量较小（< 500）。

**SPSS 路径**：`Analyze → Classify → Hierarchical Cluster`

**语法**：
```spss
CLUSTER var1 var2 var3 var4
  /METHOD=WARD
  /MEASURE=SEUCLID
  /PLOT=DENDROGRAM VICICLE
  /PRINT=CLUSTER(2,4) SCHEDULE
  /SAVE=CLUSTER(3).
```

**聚类方法选择**：
| 方法 | 特点 | 推荐场景 |
|------|------|---------|
| Ward's Method | 最小化组内方差 | 最常用，效果好 |
| Between-groups linkage | 组间平均连接 | 通用 |
| Within-groups linkage | 组内平均连接 | 产生紧凑聚类 |
| Nearest/Furthest neighbor | 最近/最远邻 | 链状/紧凑聚类 |

**距离度量**：
- Euclidean 距离：连续变量
- Squared Euclidean：最常用
- Chi-square measure：分类变量

**论文表述**：
```
采用层次聚类分析（Ward 法，Squared Euclidean 距离），
基于 [变量] 对 [N] 名被试进行分类。
根据树状图和理论判断，最终确定分为 [K] 类。
第一类 [特征描述] (n = [值])，第二类 [特征描述] (n = [值])。
```

### 1.3 TwoStep 聚类

**适用场景**：自动确定最优聚类数，支持混合变量类型（连续+分类），大样本。

**SPSS 路径**：`Analyze → Classify → TwoStep Cluster Analysis`

**语法**：
```spss
TWOSTEP CLUSTER
  /CONTINUOUS VARIABLES=age income score
  /CATEGORICAL VARIABLES=gender edu
  /DISTANCE LIKELIHOOD
  /NUMCLUSTERS AUTO 15 BIC
  /HANDLENOISE 0
  /MEMALLOCATE 64
  /PRINT INITIAL SUMMARY
  /SAVE VARIABLE=TSC_501.
```

**关键输出**：
- 模型摘要：聚类数、Silhouette 系数（> 0.5 好，> 0.7 优）
- 聚类大小
- 预测变量重要性排序

**论文表述**：
```
采用 TwoStep 聚类分析，纳入 [连续变量] 和 [分类变量]，
模型自动确定最优聚类数为 [K]。
聚类质量指标 Silhouette 系数为 [值]，表明聚类结构 [好/可接受]。
[变量X] 的重要性最高，是区分各聚类的主要因素。
```

---

## 二、判别分析 (Discriminant Analysis)

**适用场景**：已知分组，找出能区分各组的变量组合；或用于分类预测。

**SPSS 路径**：`Analyze → Classify → Discriminant`

**语法**：
```spss
DISCRIMINANT
  /GROUPS=group(1 3)
  /VARIABLES=var1 var2 var3 var4
  /ANALYSIS ALL
  /METHOD=WILKS
  /FIN=3.84
  /FOUT=2.71
  /ROTATE=UNRAW
  /HISTOGRAM
  /STATISTICS=MEAN STDDEV COEFF RAW CORR CROSSVALID
  /PLOT=COMBINED MAP SEPARATE
  /CLASSIFY=NONMISSING POOLED.
```

**关键输出**：
- Wilks' Lambda：越小组间差异越大
- 标准化典型判别函数系数：判别变量权重
- 结构矩阵：变量与判别函数的相关
- 分类结果：正确分类百分比
- 交叉验证结果：更可靠的正确率估计

**论文表述**：
```
以 [分组变量] 为分组变量，[自变量1-4] 为预测变量，
采用 Fisher 判别分析。Wilks' Lambda = [值]，χ² = [值]，
df = [值]，p = [值]，表明判别函数显著。
标准化判别函数系数显示，[变量X] (系数 = [值]) 和
[变量Y] (系数 = [值]) 是区分各组的主要因素。
判别函数对 [百分比]% 的个案正确分类（交叉验证: [百分比]%）。
```

---

## 三、生存分析

### 3.1 Kaplan-Meier 生存分析

**适用场景**：比较两组或多组的生存时间（如患者存活时间、设备故障时间）。

**SPSS 路径**：`Analyze → Survival → Kaplan-Meier`

**语法**：
```spss
KM time BY group
  /STATUS=event(1)
  /PRINT TABLE MEAN
  /PLOT SURVIVAL
  /TEST LOGRANK BRESLOW TARONE
  /COMPARE OVERALL POOLED.
```

**关键输出**：
- 生存表：各时间点的累积生存率
- 生存曲线图
- Log-Rank 检验：比较各组生存曲线是否有显著差异
- 中位生存时间

**论文表述**：
```
采用 Kaplan-Meier 生存分析比较 [组A] 和 [组B] 的生存时间差异。
结果表明，[组A] 的中位生存时间为 [值] ([95% CI])，
[组B] 的中位生存时间为 [值] ([95% CI])。
Log-Rank 检验显示两组生存曲线差异 [显著/不显著]
(χ² = [值], df = [值], p = [值])。
```

### 3.2 Cox 回归

**适用场景**：分析多个因素对生存时间的影响，允许纳入协变量。

**SPSS 路径**：`Analyze → Survival → Cox Regression`

**语法**：
```spss
COXREG time
  /STATUS=event(1)
  /METHOD=ENTER age treatment stage
  /CATEGORICAL=treatment
  /CONTRAST(treatment)=INDICATOR(1)
  /PRINT=CI(95) BASELINE SURVIVAL TABLE(1,5,10)
  /PLOT SURVIVAL HAZARDS LML
  /SAVE=RESID.
```

**关键输出**：
- Omnibus 检验：模型整体是否显著
- 各变量的 B、Wald、p、Exp(B) (风险比 HR)
- HR 的 95% CI
- 生存曲线

**HR 解读**（类似 OR）：
- HR = 1：该变量不影响生存
- HR > 1：增加风险（生存时间缩短）
- HR < 1：降低风险（生存时间延长）

**论文表述**：
```
采用 Cox 比例风险回归模型分析 [因素] 对 [生存结局] 的影响。
模型整体显著，χ²([df]) = [值], p = [值]。
在控制其他变量后，[变量X] 的风险比 HR = [值]
(95% CI [下限, 上限], p = [值])，表明 [解释 HR 含义]。
[变量Y] 的预测作用不显著 (HR = [值], p = [值])。
```

---

## 四、ROC 曲线

**适用场景**：评估诊断测试或预测模型的准确性，确定最佳截断值。

**SPSS 路径**：`Analyze → ROC Curve`

**语法**：
```spss
ROC score BY disease(1)
  /PLOT=CURVE(REFERENCE)
  /PRINT=SE SP COORDINATES
  /CRITERIA=CUTOFF=INCLUDE TESTPOS=LR DISTRIBUTION=FREE
  /CI=TRUE(95).
```

**关键输出**：
- AUC（曲线下面积）：0.5=无判别力, 0.7-0.8=可接受, 0.8-0.9=良好, >0.9=优秀
- 最佳截断值（Youden 指数 = 敏感度+特异度-1 最大处）
- 各截断值的敏感度、特异度、1-特异度
- 渐近显著性检验：AUC 是否显著大于 0.5

**论文表述**：
```
采用 ROC 曲线分析评估 [指标] 对 [疾病/事件] 的诊断价值。
结果表明，AUC = [值] (95% CI [下限, 上限], p = [值])，
表明该指标具有 [优秀/良好/可接受/较差] 的判别能力。
当截断值取 [值] 时，敏感度为 [值]，特异度为 [值]，
Youden 指数为 [值]，为最佳截断点。
```

---

## 五、广义线性模型

### 5.1 泊松回归 (计数数据)

**适用场景**：因变量是计数数据（如就诊次数、事故次数、缺陷数）。

**SPSS 路径**：`Analyze → Generalized Linear Models`

**语法**：
```spss
GENLIN events BY treatment WITH age (ORDER=ASCENDING)
  /MODEL treatment age
    DISTRIBUTION=POISSON LINK=LOG
  /CRITERIA METHOD=FISHER(1) SCALE=1 COVB=MODEL MAXITERATIONS=100
  /MISSING CLASSMISSING=EXCLUDE
  /PRINT CPS DESCRIPTIVES MODELINFO FIT SUMMARY SOLUTION.
```

**关键输出**：
- 模型拟合：偏差 (Deviance)、AIC、BIC
- 参数估计：B、Exp(B)（发生率比 IRR）、Wald、p

**IRR 解读**：
- IRR = 1：无影响
- IRR > 1：每增加 1 单位 X，事件发生率增加 (IRR-1)×100%
- IRR < 1：事件发生率降低

**论文表述**：
```
因变量 [Y] 为计数数据，采用泊松回归分析。
模型拟合良好 (Deviance/df = [值])。
[变量X] 的发生率比 IRR = [值] (95% CI [下限, 上限], p = [值])，
表明 [变量X] 每增加一个单位，[事件] 发生率增加 [百分比]%。
```

### 5.2 负二项回归 (过离散计数数据)

**适用场景**：计数数据存在过离散（方差远大于均值）时，优于泊松回归。

**语法**：
```spss
GENLIN events BY treatment WITH age
  /MODEL treatment age
    DISTRIBUTION=NEGBIN(MLE) LINK=LOG
  /PRINT CPS DESCRIPTIVES MODELINFO FIT SUMMARY SOLUTION.
```

### 5.3 GEE (广义估计方程)

**适用场景**：聚类/纵向/重复测量数据，非正态因变量。

**语法**：
```spss
GENLIN response BY group time WITH covariate (ORDER=ASCENDING)
  /MODEL group time group*time covariate
    DISTRIBUTION=NORMAL LINK=IDENTITY
  /REPEATED SUBJECT=id SORT=YES CORRTYPE=AR(1)
  /MISSING CLASSMISSING=EXCLUDE
  /PRINT CPS DESCRIPTIVES MODELINFO FIT SUMMARY SOLUTION.
```

---

## 六、混合线性模型

**适用场景**：多层嵌套数据（学生嵌套在班级、患者嵌套在医院）、重复测量有缺失、随机效应模型。

**SPSS 路径**：`Analyze → Mixed Models → Linear`

**语法**：
```spss
* 两层模型: 学生(level 1) 嵌套在班级(level 2).
MIXED score BY treatment WITH age
  /FIXED=treatment age treatment*age | SSTYPE(3)
  /RANDOM=INTERCEPT | SUBJECT(class_id) COVTYPE(VC)
  /METHOD=REML
  /PRINT=SOLUTION TESTCOV
  /SAVE=PRED RESID.

* 随机斜率模型.
MIXED score BY group WITH time
  /FIXED=group time group*time | SSTYPE(3)
  /RANDOM=INTERCEPT time | SUBJECT(id) COVTYPE(UN)
  /METHOD=REML
  /PRINT=SOLUTION TESTCOV.
```

**关键输出**：
- 模型拟合：-2 Restricted Log Likelihood、AIC、BIC
- 固定效应：各变量的 F 值、p 值
- 随机效应：方差成分、ICC（组内相关系数）
- ICC = 组间方差 / (组间方差 + 组内方差) → 多大比例的变异来自组间

**论文表述**：
```
采用两层线性混合模型分析，以 [因变量] 为因变量，
[自变量] 为固定效应，[聚类变量] 为随机效应（随机截距模型）。
组内相关系数 ICC = [值]，表明 [因变量] 的 [百分比]% 变异
来自组间差异，有必要采用多层模型。

固定效应结果表明，[变量X] 的效应显著 (F = [值], p = [值])。
随机截距方差为 [值] (p = [值])，说明各组的基线水平存在显著差异。
```

---

## 七、决策树

**适用场景**：分类或回归的可视化决策规则，变量筛选。

### 7.1 CHAID

**SPSS 路径**：`Analyze → Classify → Tree`

**语法**：
```spss
TREE target_var BY predictor1 predictor2 predictor3 predictor4
  /TREE DISPLAY=TOPDOWN NODES=BRANCHES
  /PRINT MODELSUMMARY CLASSIFICATION RISK
  /METHOD TYPE=CHAID ALPHASPLIT=0.05 ALPHAMERGE=0.05
    MAXDEPTH=3 MINPARENTSIZE=100 MINCHILDSIZE=50
  /SAVE PREDVAL NODEID.
```

**关键输出**：
- 树结构图
- 节点纯度
- 预测变量重要性
- 分类正确率

**论文表述**：
```
采用 CHAID 决策树分析预测 [结果变量]。
模型以 [变量X] 为最重要的分割变量，其次为 [变量Y]。
树的深度为 [N] 层，共形成 [M] 个终端节点。
模型的分类正确率为 [百分比]%。
```

---

## 八、神经网络

**适用场景**：非线性分类/回归预测，变量间存在复杂交互。

**SPSS 路径**：`Analyze → Neural Networks → Multilayer Perceptron`

**语法**：
```spss
MLP target_var BY predictor1 predictor2 WITH predictor3 predictor4
  /PARTITION TRAINING=70 TEST=30 HOLDOUT=0
  /ARCHITECTURE HIDDENLAYERS=AUTO(5) RESILIENCE=AUTO
  /STOPPING RULES=STEPS(1) TIME(15) ERROR(0)
  /PRINT NETWORK INFORMATION PREDICTORS CLASSIFICATION
  /SAVE PREDICTED.
```

---

## 九、曲线估计

**适用场景**：探索两个变量之间的非线性关系，选择最佳拟合曲线。

**SPSS 路径**：`Analyze → Regression → Curve Estimation`

**语法**：
```spss
CURVEFIT
  /VARIABLES=y WITH x
  /CONSTANT
  /MODEL=LINEAR QUADRATIC CUBIC EXPONENTIAL S GROWTH LOGISTIC
  /UPPERBOUND=100
  /PLOT FIT.
```

**曲线类型**：
| 类型 | 公式 | 适用场景 |
|------|------|---------|
| Linear | y = b₀ + b₁x | 线性关系 |
| Quadratic | y = b₀ + b₁x + b₂x² | U 形/倒 U 形 |
| Cubic | y = b₀ + b₁x + b₂x² + b₃x³ | S 形 |
| Exponential | y = b₀·e^(b₁x) | 指数增长/衰减 |
| S-curve | y = e^(b₀+b₁/x) | 饱和型增长 |
| Growth | y = e^(b₀+b₁x) | 指数增长 |
| Logistic | y = 1/(1/u+b₀·b₁^x) | 有上限的增长 |

**论文表述**：
```
采用曲线估计探索 [X] 与 [Y] 的关系。
比较了线性、二次、指数等 [N] 种模型，
[最佳模型] 的拟合效果最好 (R² = [值], F = [值], p = [值])。
关系方程为 [方程]。
```

---

## 十、多重插补结果汇总分析

**适用场景**：对多重插补生成的多个数据集进行综合分析。

**分析步骤**：
```spss
* 第 1 步: 多重插补.
MULTIPLE IMPUTATION var1 var2 var3
  /IMPUTE METHOD=AUTO NIMPUTATIONS=5
  /OUTFILE IMPUTATIONS=imputed_data.sav.

* 第 2 步: 打开插补数据.
GET FILE='imputed_data.sav'.

* 第 3 步: 对每个插补数据集做分析.
* SPSS 会自动对所有插补数据集执行分析并汇总结果.
REGRESSION
  /MISSING=ANALYSIS
  /DEPENDENT dv
  /METHOD=ENTER iv1 iv2 iv3.

* 第 4 步: 查看汇总结果.
* 输出中的 "Multiple Imputation Statistics" 表格显示:
* - 各插补数据集的估计值
* - 汇总估计值 (Pooled)
* - 95% CI 和 p 值 (基于 Rubin 规则)
```

**论文表述**：
```
采用多重插补法处理缺失值，生成 5 个插补数据集。
对每个数据集进行 [分析方法]，采用 Rubin 规则汇总结果。
汇总结果显示，[变量X] 的效应显著 (B = [值], 95% CI [下限, 上限],
p = [值])。
```

---

## 十一、Bootstrap (SPSS 内建)

**适用场景**：不依赖分布假设的参数估计和假设检验，小样本特别有用。

**SPSS 路径**：`Analyze → Bootstrapping`

**语法**：
```spss
BOOTSTRAP
  /SAMPLING METHOD=SIMPLE
  /VARIABLES INPUT=var1 var2 var3
  /CRITERIA CILEVEL=95 CITYPE=BCA  NSAMPLES=1000
  /MISSING USERMISSING=EXCLUDE.

* 后面跟任何分析命令.
T-TEST GROUPS=group(1 2) /VARIABLES=score.

* 或回归.
REGRESSION /DEPENDENT=dv /METHOD=ENTER iv1 iv2.
```

**关键输出**：
- Bootstrap 标准误
- Bootstrap 95% CI（BCa 置信区间最准确）
- 偏差校正

**论文表述**：
```
采用 Bootstrap 方法 (重复抽样 1000 次，BCa 95% CI)
检验 [效应] 的显著性。
Bootstrap 结果显示，[变量X] 的效应为 [值]
(BootSE = [值], 95% BCa CI [下限, 上限])，
置信区间不包含 0，效应显著。
```

---

## 十二、自定义表格 (Custom Tables)

**适用场景**：创建出版级质量的多维表格，比默认输出更灵活。

**SPSS 路径**：`Analyze → Tables → Custom Tables`

**语法**：
```spss
CTABLES
  /VLABELS VARIABLES=gender edu income
    DISPLAY=LABEL
  /TABLE gender [C][COUNT F40.0, COLPCT.COUNT PCT40.1] BY edu [C]
  /CATEGORIES VARIABLES=gender edu ORDER=A KEY=VALUE EMPTY=INCLUDE
  /SIGTEST TYPE=CHISQUARE ALPHA=0.05 INCLUDEMRSETS=YES
    CATEGORIES=ALLVISIBLE.

* 带均值和标准差的表格.
CTABLES
  /TABLE group [C] BY score [MEAN, STDDEV, COUNT]
  /FORMAT EMPTY=BLANK.
```

---

## 十三、对应分析

**适用场景**：可视化两个分类变量之间的关系（类似卡方检验的可视化版本）。

**SPSS 路径**：`Analyze → Dimension Reduction → Correspondence Analysis`

**语法**：
```spss
CORRESPONDENCE
  /TABLE=var1(1,5) BY var2(1,4)
  /MEASURE=CHISQ
  /STANDARDIZE=RCOM
  /NORMALIZATION=SYMMETRICAL
  /DIMENSIONS=2
  /PLOT=ROWS COLUMNS JOINT
  /PRINT=OVERALL RSCORES CSCORES CONTRIBUTIONS.
```

**关键输出**：
- 惯量 (Inertia)：每个维度解释的变异量
- 行/列坐标：在二维图中的位置
- 贡献量：各变量对维度的贡献

---

## 十四、质量控制

### 控制图
**SPSS 路径**：`Analyze → Quality Control → Control Charts`

```spss
* X-bar R 图.
XCHART quality_measure BY batch
  /MRANGE
  /SIGMAS=3
  /RULES=ALL
  /PLOT=MEANS RANGES.
```

### Pareto 图
```spss
PARETO defect_type.
```

---

## 十五、比率统计

**SPSS 路径**：`Analyze → Descriptive Statistics → Ratio`

```spss
RATIO statistic1 BY group WITH statistic2
  /PRINT=ALL
  /SORT=ASCENDING
  /ID=case_id.
```

**关键输出**：离散系数、变异系数、价格相关差分、中位数中心化比率。

---

## 十六、OMS (输出管理系统)

**适用场景**：将 SPSS 输出表格自动保存为数据集，用于后续处理或自动化报告。

```spss
* 开始捕获回归结果到数据集.
OMS
  /SELECT TABLES
  /IF COMMANDS=['Regression'] SUBTYPES=['Coefficients']
  /DESTINATION FORMAT=SAV
    OUTFILE='regression_coeffs.sav'.

REGRESSION /DEPENDENT=dv /METHOD=ENTER iv1 iv2 iv3.

OMSEND.

* 此时 regression_coeffs.sav 中包含回归系数表.
GET FILE='regression_coeffs.sav'.
LIST.
```

---

## 十七、Python / R 集成

**适用场景**：SPSS 原生语法无法完成的复杂计算或自定义分析。

### Python 扩展
```spss
BEGIN PROGRAM PYTHON3.
import spss
import spssdata

# 获取数据
with spssdata.Spssdata(indexes=['var1', 'var2']) as cursor:
    for row in cursor:
        print(row)

# 执行 SPSS 命令
spss.Submit("""
DESCRIPTIVES VARIABLES=var1 var2
  /STATISTICS=MEAN STDDEV.
""")
END PROGRAM.
```

### 安装扩展命令
```spss
* 安装 PROCESS 宏.
SPSSINC INSTALL PROCESS.

* 安装其他扩展.
SPSSINC INSTALL PACKAGE="PackageName".
```

---

## 十八、复杂抽样

**适用场景**：调查数据使用了分层、整群或多阶段抽样设计。

```spss
* 定义抽样方案.
CSPLAN
  /PLAN FILE='sample_plan.csplan'
  /PLANVARS ANALYSISWEIGHT=weight
  /DESIGN STRATA=stratum CLUSTER=psu
  /METHOD SRWOR.

* 描述统计.
CSDESCRIPTIVES
  /PLAN FILE='sample_plan.csplan'
  /VARIABLES=income age score
  /MEAN SE CINTERVAL(95).

* 回归.
CSGLM income BY edu WITH age
  /PLAN FILE='sample_plan.csplan'
  /MODEL edu age
  /TESTTYPE=F
  /STATISTICS PARAMS SE.
```

---

## 十九、图表示例语法

```spss
* 分组箱线图.
GRAPH
  /BOXPLOT(SIMPLE)=score BY group.

* 分组条形图 (带误差棒).
GRAPH
  /BAR(SIMPLE)=MEAN(score) BY group
  /INTERVAL CI(95.0).

* 散点图 + 回归线.
GRAPH
  /SCATTERPLOT(BIVAR)=x WITH y
  /MISSING=LISTWISE
  /TEMPLATE='C:\templates\scatter_with_line.sgt'.

* 交互效应图.
GRAPH
  /LINE(MULTIPLE)=MEAN(score) BY time BY group.
```
