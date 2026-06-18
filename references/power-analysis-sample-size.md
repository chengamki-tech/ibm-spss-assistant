# 统计功效与样本量计算指南

## 一、核心概念

### 什么是统计功效 (Statistical Power)

统计功效 = 当真实效应存在时，研究能正确检测到它的概率。

```
                    实际情况
                H₀ 为真     H₀ 为假
决策   拒绝 H₀   I 类错误     正确 ✓ (Power)
       不拒绝 H₀  正确 ✓      II 类错误 (β)
```

- **Power = 1 - β**
- 一般要求 **Power ≥ .80** (80% 概率检测到真实效应)
- 高风险研究建议 **Power ≥ .90**

### 四个核心参数

| 参数 | 含义 | 通常设定 |
|------|------|---------|
| α (显著性水平) | I 类错误概率 | .05 |
| Power (功效) | 1 - β | .80 |
| 效应量 (Effect Size) | 效应的实际大小 | 参考下表 |
| 样本量 (N) | 被试数量 | 由计算得出 |

**给定任意三个，可计算第四个。**

---

## 二、G*Power 使用指南

### 下载与安装

- 官网: https://www.gpower.hhu.de/
- 免费，支持 Windows 和 macOS
- 最新版本: G*Power 3.1

### 四种功效分析类型

| 类型 | 英文 | 用途 | 输入 | 输出 |
|------|------|------|------|------|
| 事前分析 | A priori | 确定需要多少样本 | α, Power, 效应量 | N |
| 事后分析 | Post hoc | 已有数据功效够不够 | α, N, 效应量 | Power |
| 敏感性分析 | Sensitivity | 能检测到多小的效应 | α, Power, N | 效应量 |
| 标准分析 | Criterion | 给定 N 和效应量的 α | N, 效应量 | α |

### 常用分析的 G*Power 设置

#### 独立样本 t 检验

```
Test family: t tests
Statistical test: Means: Difference between two independent means
Type of power analysis: A priori
Tail(s): Two
Effect size d: 0.5 (中等效应)
α err prob: 0.05
Power (1-β err prob): 0.80
Allocation ratio N2/N1: 1 (等组)
→ Output: Total sample size = 128 (每组 64)
```

#### 配对样本 t 检验

```
Test family: t tests
Statistical test: Means: Difference between two dependent means (matched pairs)
Type of power analysis: A priori
Tail(s): Two
Effect size dz: 0.5
α err prob: 0.05
Power: 0.80
→ Output: Total sample size = 34 对
```

#### 单因素 ANOVA

```
Test family: F tests
Statistical test: ANOVA: Fixed effects, omnibus, one-way
Type of power analysis: A priori
Effect size f: 0.25 (中等)
α err prob: 0.05
Power: 0.80
Number of groups: 3
→ Output: Total sample size = 159 (每组约 53)
```

#### 相关分析

```
Test family: t tests
Statistical test: Correlation: Bivariate normal model
Type of power analysis: A priori
Tail(s): Two
Effect size ρ: 0.3 (中等相关)
α err prob: 0.05
Power: 0.80
→ Output: Total sample size = 85
```

#### 线性回归

```
Test family: F tests
Statistical test: Linear multiple regression: Fixed model, R² deviation from zero
Type of power analysis: A priori
Effect size f²: 0.15 (中等)
α err prob: 0.05
Power: 0.80
Number of predictors: 5
→ Output: Total sample size = 92
```

#### 卡方检验

```
Test family: χ² tests
Statistical test: Goodness-of-fit tests: Contingency tables
Type of power analysis: A priori
Effect size w: 0.3 (中等)
α err prob: 0.05
Power: 0.80
Df: 2 (自由度 = (行数-1) × (列数-1))
→ Output: Total sample size = 108
```

#### 逻辑回归

```
Test family: z tests
Statistical test: Logistic regression
Type of power analysis: A priori
Effect size: OR = 2.6 (对应中等效应)
α err prob: 0.05
Power: 0.80
R² of covariates: 0 (无协变量)
X distribution: Binomial (p = 0.5)
→ Output: 总样本量取决于事件发生率和 OR
```

---

## 三、效应量参考表

### 常见效应量指标

| 分析类型 | 指标 | 计算公式 | 小 | 中 | 大 |
|---------|------|---------|---|---|---|
| t 检验 | Cohen's d | (M₁-M₂)/SD_pooled | 0.2 | 0.5 | 0.8 |
| ANOVA | f | √(η²/(1-η²)) | 0.10 | 0.25 | 0.40 |
| ANOVA | η² | SS_between/SS_total | .01 | .06 | .14 |
| ANOVA | 偏 η² | SS_effect/(SS_effect+SS_error) | .01 | .06 | .14 |
| 相关 | r | Pearson/Spearman | .10 | .30 | .50 |
| 回归 | f² | R²/(1-R²) | .02 | .15 | .35 |
| 回归 | R² | 模型解释方差比 | .02 | .13 | .26 |
| 卡方 | Cramer's V | √(χ²/(N×(k-1))) | .10 | .30 | .50 |
| 卡方 | w | √(Σ(p₁-p₀)²/p₀) | .10 | .30 | .50 |
| 逻辑回归 | OR | exp(B) | 1.5 | 3.0 | 9.0 |

### 如何确定效应量

1. **参考前人研究** — 最佳方案，用同类研究的效应量
2. **参考 Cohen 标准** — 保守但通用
3. **做 pilot study** — 用预实验数据估计
4. **使用最小有意义效应** — 实际意义上最小的有意义差异

---

## 四、样本量规划实用表

### t 检验 (α=.05, Power=.80, 双尾)

| 效应量 (d) | 每组 n | 总 N |
|-----------|--------|------|
| 0.20 (小) | 394 | 788 |
| 0.30 | 176 | 352 |
| 0.40 | 100 | 200 |
| 0.50 (中) | 64 | 128 |
| 0.60 | 45 | 90 |
| 0.70 | 34 | 68 |
| 0.80 (大) | 26 | 52 |
| 1.00 | 17 | 34 |

### ANOVA (α=.05, Power=.80)

| 效应量 (f) | 3 组 | 4 组 | 5 组 |
|-----------|------|------|------|
| 0.10 (小) | 201 | 252 | 300 |
| 0.20 | 57 | 69 | 80 |
| 0.25 (中) | 39 | 48 | 55 |
| 0.30 | 28 | 34 | 39 |
| 0.40 (大) | 18 | 21 | 24 |

### 相关分析 (α=.05, Power=.80, 双尾)

| 效应量 (r) | 需要的 N |
|-----------|---------|
| .10 (小) | 783 |
| .15 | 350 |
| .20 | 199 |
| .25 | 129 |
| .30 (中) | 85 |
| .40 | 47 |
| .50 (大) | 29 |

### 回归分析 (α=.05, Power=.80, R²检验)

| 效应量 (f²) | 3 个 IV | 5 个 IV | 10 个 IV |
|------------|---------|---------|----------|
| 0.02 (小) | 258 | 395 | 725 |
| 0.10 | 60 | 89 | 160 |
| 0.15 (中) | 43 | 63 | 113 |
| 0.20 | 34 | 49 | 87 |
| 0.35 (大) | 21 | 30 | 52 |

---

## 五、论文表述模板

### 事前样本量计算

```
采用 G*Power 3.1 (Faul et al., 2007) 进行事前功效分析。
设定显著性水平 α = .05，统计功效 1-β = .80，
效应量为 [小/中/大] 等 ([指标] = [值]，依据 [来源])，
[检验类型] 所需的最小样本量为 [N]。
本研究实际收集 [N] 份有效数据，满足样本量要求。
```

### 事后功效分析 (显著结果)

```
采用 G*Power 3.1 进行事后功效分析。基于当前样本量 (N = [值])、
观测效应量 ([指标] = [值])、α = .05 (双尾)，
计算得到检验功效为 [值]，表明本研究具有足够的统计功效。
```

### 事后功效分析 (不显著结果)

```
采用 G*Power 3.1 进行事后功效分析。基于当前样本量 (N = [值])、
观测效应量 ([指标] = [值])、α = .05 (双尾)，
计算得到检验功效为 [值]。

[功效 ≥ .80: 检验功效充足，不显著结果可信。]
[功效 < .80: 检验功效不足 (1-β = [值])，不显著结果可能源于
 样本量不足。根据功效分析，要达到 .80 的功效，
 至少需要 [N] 名被试。建议未来研究增加样本量。]
```

### 样本量不足时的应对

当实际样本量无法达到计算值时：

1. **报告功效不足** — 诚实说明
2. **使用更敏感的分析方法** — 如非参数检验
3. **增大效应量预期** — 但需有理论依据
4. **接受较低的功效** — 并在讨论中说明局限性
5. **使用精确检验** — 小样本时更准确
