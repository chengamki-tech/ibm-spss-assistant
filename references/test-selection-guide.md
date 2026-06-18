# 统计检验选择决策树

## 第一步：确定研究目的

```
你的研究目的是什么？
├── 比较差异 → 跳到"第二步A"
├── 探索关联 → 跳到"第二步B"
├── 预测结果 → 跳到"第二步C"
└── 降维/结构 → 跳到"第二步D"
```

## 第二步A：比较差异

```
有几个组？
├── 两组
│   ├── 独立样本?
│   │   ├── 数据正态 → 独立样本 t 检验
│   │   └── 数据非正态 → Mann-Whitney U 检验
│   └── 配对样本?
│       ├── 数据正态 → 配对样本 t 检验
│       └── 数据非正态 → Wilcoxon 符号秩检验
│
└── 三组及以上
    ├── 独立样本?
    │   ├── 数据正态 + 方差齐性 → 单因素 ANOVA
    │   ├── 数据正态 + 方差不齐 → Welch ANOVA
    │   └── 数据非正态 → Kruskal-Wallis 检验
    └── 配对样本?
        ├── 数据正态 → 重复测量 ANOVA
        └── 数据非正态 → Friedman 检验
```

### 两组比较 — 详细条件

| 条件 | 方法 | SPSS 路径 |
|------|------|-----------|
| 独立、连续DV、正态 | 独立样本 t 检验 | Compare Means → Independent-Samples T Test |
| 独立、连续DV、非正态 | Mann-Whitney U | Nonparametric Tests → Legacy → 2 Independent |
| 配对、连续DV、正态 | 配对样本 t 检验 | Compare Means → Paired-Samples T Test |
| 配对、连续DV、非正态 | Wilcoxon | Nonparametric Tests → Legacy → 2 Related |
| 独立、分类DV | 卡方检验 | Descriptive → Crosstabs → Statistics → Chi-square |
| 独立、分类DV、期望频<5 | Fisher 精确检验 | 同上，自动计算 |

### 多组比较 — 详细条件

| 条件 | 方法 | SPSS 路径 |
|------|------|-----------|
| 独立、连续DV、正态 | 单因素 ANOVA | Compare Means → One-Way ANOVA |
| 独立、连续DV、正态、多因子 | 多因素 ANOVA | General Linear Model → Univariate |
| 配对、连续DV、正态 | 重复测量 ANOVA | General Linear Model → Repeated Measures |
| 独立、连续DV、非正态 | Kruskal-Wallis | Nonparametric → Legacy → K Independent |
| 配对、连续DV、非正态 | Friedman | Nonparametric → Legacy → K Related |

### 事后检验选择

| 场景 | 推荐方法 |
|------|---------|
| 各组样本量相等 | Tukey HSD |
| 各组样本量不等 | Bonferroni 或 Scheffé |
| 只比较实验组与对照组 | Dunnett |
| 方差不齐 | Games-Howell |
| 需要最保守的校正 | Bonferroni |

## 第二步B：探索关联

```
两个变量的类型？
├── 两个连续变量
│   ├── 双变量正态 → Pearson 相关
│   └── 非正态或有异常值 → Spearman 秩相关
├── 两个分类变量
│   ├── 有序分类 → Kendall tau-b
│   └── 名义分类 → 卡方检验 + Cramer's V
└── 一个连续 + 一个分类
    ├── 分类变量二水平 → 点二列相关
    └── 分类变量多水平 → Eta 系数
```

| 变量组合 | 方法 | 指标 |
|---------|------|------|
| 连续 × 连续 (正态) | Pearson r | r 值 [-1, 1] |
| 连续 × 连续 (非正态) | Spearman ρ | ρ 值 |
| 有序 × 有序 | Kendall tau-b | τb 值 |
| 名义 × 名义 (2×2) | Fisher 精确检验 | OR 值 |
| 名义 × 名义 (更大) | 卡方检验 | Cramer's V |
| 连续 × 二分类 | 点二列相关 | rpb 值 |

## 第二步C：预测结果

```
因变量类型？
├── 连续变量
│   ├── 一个自变量 → 简单线性回归
│   ├── 多个自变量 → 多元线性回归
│   └── 自变量间高度相关 → 岭回归 / LASSO
├── 二分类变量
│   └── 逻辑回归
└── 多分类变量
    ├── 有序多分类 → 有序逻辑回归
    └── 名义多分类 → 多项逻辑回归
```

### 回归分析前提检查

| 检查项 | 方法 | 标准 |
|--------|------|------|
| 线性关系 | 散点图 | 应呈线性 |
| 正态性 | 残差 Q-Q 图 | 点在对角线附近 |
| 等方差性 | 残差 vs 预测值图 | 无漏斗形 |
| 独立性 | Durbin-Watson | 1.5-2.5 |
| 无多重共线性 | VIF | < 10 (理想 < 5) |
| 样本量 | N ≥ 50 + 8×IV 数 | 越多越好 |

## 第二步D：降维 / 结构发现

| 目的 | 方法 | 前提 |
|------|------|------|
| 探索潜在因子结构 | 探索性因子分析 (EFA) | KMO > .7, Bartlett 显著 |
| 验证已有理论结构 | 验证性因子分析 (CFA) | 需要 AMOS / Mplus |
| 测量量表信度 | Cronbach's α | α > .7 |
| 将个案分组 | 聚类分析 | 标准化变量 |

## 效应量速查

| 分析类型 | 效应量指标 | 小 | 中 | 大 |
|---------|-----------|---|---|---|
| t 检验 | Cohen's d | 0.2 | 0.5 | 0.8 |
| ANOVA | η² | .01 | .06 | .14 |
| ANOVA | 偏 η² | .01 | .06 | .14 |
| 相关 | r | .10 | .30 | .50 |
| 回归 | f² | .02 | .15 | .35 |
| 卡方 | Cramer's V | .10 | .30 | .50 |

## 样本量参考

| 分析类型 | 最小样本量 | 建议样本量 |
|---------|-----------|-----------|
| t 检验 (每组) | 20 | 30+ |
| ANOVA (每组) | 20 | 30+ |
| 相关分析 | 30 | 50+ |
| 多元回归 | 50 | IV数 × 15-20 |
| 因子分析 | 题项数 × 5 | 题项数 × 10 |
| 逻辑回归 | EPV ≥ 10 | EPV ≥ 20 |

EPV = Events Per Variable，即每个自变量至少需要 10 个事件（阳性案例）
