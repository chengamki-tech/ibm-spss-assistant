# 高级分析指南

## 一、中介效应分析 (Mediation Analysis)

### 什么是中介效应

中介效应是指自变量 X 不是直接影响因变量 Y，而是通过一个中间变量 M 间接影响 Y。

```
        a           b
    X ------→ M ------→ Y
    |                   ↑
    |       c'          |
    +-------------------+
    
    c = 总效应 = c' + a×b
    c' = 直接效应
    a×b = 间接效应 (中介效应)
```

### Baron-Kenny 逐步法

**Step 1**：检验总效应 c (X → Y 显著)
```
REGRESSION /DEPENDENT Y /METHOD=ENTER X.
```

**Step 2**：检验路径 a (X → M 显著)
```
REGRESSION /DEPENDENT M /METHOD=ENTER X.
```

**Step 3**：检验路径 b 和 c' (同时放入 X 和 M)
```
REGRESSION /DEPENDENT Y /METHOD=ENTER X M.
```

**判断标准**：
- a 显著 + b 显著 → 中介效应存在
- c' 不显著 → 完全中介
- c' 显著但比 c 小 → 部分中介

### Bootstrap 法 (推荐)

Baron-Kenny 法的局限：间接效应 ab 的分布通常非正态，传统检验不准确。

Bootstrap 法通过对数据反复重抽样（通常 5000 次），计算间接效应的置信区间。如果 95% CI 不包含 0，则中介效应显著。

**使用 PROCESS 宏**：
```spss
* 下载 PROCESS: https://processmacro.org/download.html
* 安装: Utilities → Extension Bundles → Install Local

PROCESS y=Y /x=X /m=M /model=4 /boot=5000 /seed=12345.
```

**解读 PROCESS 输出**：
- Effect → 间接效应值 (a×b)
- BootSE → Bootstrap 标准误
- BootLLCI / BootULCI → Bootstrap 95% CI 下限和上限
- CI 不包含 0 → 中介效应显著

### 论文表述

```
采用 Bootstrap 法（重复抽样 5000 次）检验 [中介变量] 的中介效应。
结果表明，[自变量] 通过 [中介变量] 对 [因变量] 的间接效应
显著 (ab = [值], BootSE = [值], 95% BootCI [下限, 上限])，
置信区间不包含 0，说明 [中介变量] 在 [自变量] 与 [因变量] 之间
发挥了 [完全/部分] 中介作用。
```

---

## 二、调节效应分析 (Moderation Analysis)

### 什么是调节效应

调节效应是指自变量 X 对因变量 Y 的影响大小（或方向）取决于第三个变量 Z 的水平。

```
    X ------→ Y
    |          
    |  Z (调节)
    ↓
    X × Z → Y
```

### 分析步骤

**Step 1**：对 X 和 Z 做中心化处理（减少多重共线性）
```spss
* 中心化.
COMPUTE X_c = X - [X的均值].
COMPUTE Z_c = Z - [Z的均值].
EXECUTE.

* 或使用 AGGREGATE 自动计算均值.
AGGREGATE /OUTFILE=* /BREAK= /mean_X=MEAN(X) /mean_Z=MEAN(Z).
COMPUTE X_c = X - mean_X.
COMPUTE Z_c = Z - mean_Z.
EXECUTE.
DELETE VARIABLES mean_X mean_Z.
```

**Step 2**：计算交互项
```spss
COMPUTE XZ = X_c * Z_c.
EXECUTE.
```

**Step 3**：层次回归
```spss
* Step 1: 纳入主效应.
REGRESSION
  /STATISTICS COEFF R ANOVA CHANGE
  /DEPENDENT Y
  /METHOD=ENTER X_c Z_c
  /METHOD=ENTER XZ.
```

**Step 4**：判断交互项是否显著
- ΔR² 显著 (p < .05) → 调节效应成立
- 交互项 β 显著 → 调节效应方向可解释

### 简单斜率分析

当交互效应显著时，需要进一步分析在 Z 的不同水平上，X 对 Y 的效应：

```spss
* 在 Z = 均值±1SD 水平上计算简单斜率.
* Z 高 (+1SD): X 的效应 = b1 + b3*(+1SD)
* Z 低 (-1SD): X 的效应 = b1 + b3*(-1SD)

* 使用 PROCESS 宏更方便:
PROCESS y=Y /x=X /w=Z /model=1 /boot=5000 /plot=1.
```

### 论文表述

```
采用层次回归分析检验 [调节变量] 的调节作用。
第一步纳入中心化后的 [自变量] 和 [调节变量]，第二步纳入交互项。
结果表明，交互项对 [因变量] 的预测作用显著
(β = [值], t = [值], p = [值])，ΔR² = [值],
ΔF([df1], [df2]) = [值], p = [值]，
说明 [调节变量] 显著调节了 [自变量] 与 [因变量] 之间的关系。

简单斜率分析表明，在 [调节变量] 较高 (+1SD) 时，
[自变量] 对 [因变量] 的效应 [显著/不显著] (β = [值], p = [值])；
在 [调节变量] 较低 (-1SD) 时，
[自变量] 对 [因变量] 的效应 [显著/不显著] (β = [值], p = [值])。
```

---

## 三、多元方差分析 (MANOVA)

### 什么时候用 MANOVA

- 有 2 个以上的因变量 (DV)
- 这些 DV 在理论上相关
- 想同时检验组间在多个 DV 上的整体差异

### SPSS 语法

```spss
* MANOVA.
GLM dv1 dv2 dv3 BY group
  /METHOD=SSTYPE(3)
  /INTERCEPT=INCLUDE
  /PRINT=ETASQ DESCRIPTIVE HOMOGENEITY (BOXM)
  /PLOT=PROFILE(group) TYPE=LINE ERRORBAR=CI
  /CRITERIA=ALPHA(.05)
  /DESIGN=group.
```

### 关键输出解读

| 指标 | 含义 | 判断标准 |
|------|------|---------|
| Box's M | 方差-协方差矩阵齐性 | p > .001 即可接受 |
| Pillai's Trace | 多变量检验统计量（最稳健） | p < .05 显著 |
| Wilks' Lambda | 多变量检验统计量 | p < .05 显著 |
| Hotelling's Trace | 多变量检验统计量 | p < .05 显著 |
| Roy's Largest Root | 最大特征值（最严格） | p < .05 显著 |

**选择哪个指标**：
- 样本量小或方差不齐 → Pillai's Trace（最稳健）
- 样本量大且方差齐 → Wilks' Lambda（最常用）
- 违反假设时避免使用 Roy's Largest Root

### 事后检验

MANOVA 整体显著后，对每个 DV 做单变量 ANOVA：
```spss
UNIANOVA dv1 dv2 dv3 BY group
  /METHOD=SSTYPE(3)
  /POSTHOC=group(TUKEY)
  /PRINT=ETASQ DESCRIPTIVE
  /CRITERIA=ALPHA(.05).
```

### 论文表述

```
多元方差分析结果表明，在 [自变量] 的不同水平上，
[因变量1]、[因变量2]、[因变量3] 的整体差异显著，
Pillai's Trace = [值], F([df1], [df2]) = [值], p = [值],
偏 η² = [值]。

随后的单变量检验和事后比较表明：
- [因变量1]: F([df1], [df2]) = [值], p = [值], 偏 η² = [值]
- [因变量2]: F([df1], [df2]) = [值], p = [值], 偏 η² = [值]
- [因变量3]: F([df1], [df2]) = [值], p = [值], 偏 η² = [值]
```

---

## 四、统计功效与样本量

### 什么是统计功效 (Power)

统计功效 = 当真实效应存在时，正确拒绝零假设的概率。

- Power = 1 - β (β 是 II 类错误概率)
- 一般要求 Power ≥ .80 (即 80% 的概率检测到真实效应)

### 为什么重要

| 场景 | Power | 结果 |
|------|-------|------|
| 真有差异 + Power 高 | ≥ .80 | 正确拒绝 H₀ ✓ |
| 真有差异 + Power 低 | < .80 | 可能错过真实效应 ✗ |
| 真无差异 | 任何 | 正确不拒绝 H₀ ✓ |

### 事后功效分析 (Post-hoc Power)

当结果不显著时，需要报告功效：

```
事后功效分析表明，在当前样本量 (N = [值])、效应量 ([指标] = [值])、
α = .05 (双尾) 条件下，本研究的检验功效为 [值]。
[功效 ≥ .80: 检验功效充足，不显著结果可信。
 功效 < .80: 检验功效不足，不显著结果可能源于样本量不足，
 建议未来研究将样本量增加至 N ≥ [值]。]
```

### G*Power 计算步骤

1. 打开 G*Power (免费下载: https://www.gpower.hhu.de/)
2. 选择 Test family: t tests / F tests / χ² tests
3. 选择 Statistical test: 具体检验类型
4. 选择 Power analysis: A priori (计算需要的样本量) 或 Post hoc (计算已有数据的功效)
5. 输入参数：α = .05, Power = .80, Effect size (参考下表)

### 各分析类型的效应量和样本量参考

| 分析类型 | 效应量指标 | 小 | 中 | 大 | 每组最小 n |
|---------|-----------|---|---|---|-----------|
| t 检验 | Cohen's d | 0.2 | 0.5 | 0.8 | 小:394 / 中:64 / 大:26 |
| ANOVA (3 组) | f | 0.10 | 0.25 | 0.40 | 小:600 / 中:100 / 大:40 |
| 相关 | r | .10 | .30 | .50 | 小:783 / 中:85 / 大:29 |
| 回归 (3 个 IV) | f² | .02 | .15 | .35 | 小:550 / 中:77 / 大:36 |
| 卡方 (2×2) | w | .10 | .30 | .50 | 小:1000 / 中:108 / 大:40 |

### 论文表述

**事前样本量计算**：
```
采用 G*Power 3.1 进行事前功效分析。设定 α = .05，功效 = .80，
效应量为中等 (Cohen's d = 0.5)，计算得到每组最小样本量为 64 人。
本研究实际每组 [值] 人，满足样本量要求。
```

**事后功效分析**：
```
采用 G*Power 3.1 进行事后功效分析。基于当前样本量 (N = [值]) 和
观测效应量 ([指标] = [值])，设定 α = .05 (双尾)，
计算得到检验功效为 [值]。
```

---

## 五、逻辑回归诊断

### 模型拟合指标

| 指标 | 含义 | 判断标准 |
|------|------|---------|
| -2 Log Likelihood (-2LL) | 模型拟合的负对数似然 | 越小越好 |
| Hosmer-Lemeshow | 拟合优度检验 | p > .05 拟合良好 |
| Nagelkerke R² | 伪 R² | 类比线性回归的 R² |
| 分类表 | 预测正确率 | > 70% 可接受 |
| Omnibus Tests | 模型整体检验 | p < .05 模型有效 |

### 前提假设检查

```spss
* 1. 多重共线性 (先用线性回归检查 VIF).
REGRESSION
  /STATISTICS COEFF COLLIN TOL
  /DEPENDENT dv
  /METHOD=ENTER iv1 iv2 iv3.

* 2. 样本量: EPV (Events Per Variable) ≥ 10
*    即每个自变量至少需要 10 个阳性案例
*    例: 3 个 IV 需要至少 30 个事件

* 3. 线性关系 (Box-Tidwell 检验).
*    对每个连续 IV，计算 IV × LN(IV)，纳入模型
COMPUTE iv1_ln = iv1 * LN(iv1).
EXECUTE.
LOGISTIC REGRESSION VARIABLES dv
  /METHOD=ENTER iv1 iv1_ln iv2 iv3.
* 如果 iv1_ln 显著，说明 iv1 与 logit 不是线性关系
```

### OR 解读指南

```
[自变量] 的优势比 OR = [值]，95% CI [下限, 上限]。

- OR = 1.0: 该变量对结果无影响
- OR > 1.0: 每增加 1 单位，事件发生的优势增加 (OR-1)×100%
  例: OR = 1.5 → 优势增加 50%
  例: OR = 3.0 → 优势增加 200% (是原来的 3 倍)
- OR < 1.0: 每增加 1 单位，事件发生的优势减少 (1-OR)×100%
  例: OR = 0.7 → 优势减少 30%
- CI 包含 1.0 → 效应不显著
- CI 不包含 1.0 → 效应显著
```

### 论文表述

```
逻辑回归分析结果如表 X 所示。模型整体显著，
χ²([df]) = [值], p = [值]，Nagelkerke R² = [值]，
Hosmer-Lemeshow 检验不显著 (χ² = [值], p = [值])，
表明模型拟合良好。模型对 [事件] 的预测正确率为 [百分比]%。

[自变量1] 的 Wald 检验显著 (β = [值], Wald χ² = [值],
p = [值])，OR = [值], 95% CI [下限, 上限]，表明在控制其他变量后，
[自变量1] 每增加一个单位，[事件] 发生的优势增加 [百分比]%。

[自变量2] 的预测作用不显著 (β = [值], Wald χ² = [值],
p = [值], OR = [值], 95% CI [下限, 上限])。
```

---

## 六、重复测量诊断

### 球形假设 (Sphericity)

重复测量 ANOVA 的前提：不同时间点/条件之间的差值方差相等。

```spss
GLM time1 time2 time3
  /WSFACTOR=time 3
  /PRINT=ETASQ DESCRIPTIVE HOMOGENEITY
  /WSDESIGN=time.
```

**关键输出**：
- Mauchly 球形检验：p > .05 → 满足球形假设
- p < .05 → 不满足，需要看校正结果

**校正方法**：
| 方法 | 何时使用 | 说明 |
|------|---------|------|
| Greenhouse-Geisser | ε < .75 | 最常用校正 |
| Huynh-Feldt | ε ≥ .75 | 当 G-G 过于保守时 |
| 球形假设 | Mauchly p > .05 | 无需校正 |

### 论文表述

```
Mauchly 球形检验结果表明，[变量] 的方差-协方差矩阵
[满足/不满足] 球形假设 (χ²([df]) = [值], p = [值])。
[不满足时: 因此采用 Greenhouse-Geisser 校正结果。
 F([校正df1], [校正df2]) = [值], p = [值], 偏 η² = [值]。]
```
