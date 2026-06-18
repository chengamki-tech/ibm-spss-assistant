# SPSS 图表制作完整指导

> 覆盖 SPSS 全部图表类型：何时用、怎么画、怎么定制、怎么导出。

---

## 一、图表类型选择指南

| 研究目的 | 推荐图表 | SPSS 路径 |
|---------|---------|-----------|
| 展示分布 | 直方图、箱线图、茎叶图 | Graphs → Chart Builder |
| 比较组间差异 | 分组箱线图、分组条形图+误差棒 | Graphs → Chart Builder |
| 展示关联 | 散点图、散点图矩阵 | Graphs → Chart Builder |
| 展示比例 | 饼图、堆叠条形图 | Graphs → Chart Builder |
| 展示变化趋势 | 折线图 | Graphs → Chart Builder |
| 展示交互效应 | 分组折线图 | Graphs → Chart Builder |
| 回归诊断 | 残差图、P-P 图 | Regression → Plots |
| 生存分析 | 生存曲线图 | Survival → Kaplan-Meier → Plot |
| 因子分析 | 碎石图 | Factor → Plot → Scree |
| ROC 曲线 | ROC 图 | Analyze → ROC Curve → Plot |

---

## 二、常用图表语法

### 2.1 直方图 (连续变量分布)

```spss
GRAPH
  /HISTOGRAM(NORMAL)=score.

* 分组直方图.
GRAPH
  /HISTOGRAM(NORMAL)=score BY group.
```

### 2.2 箱线图 (分布 + 异常值)

```spss
* 简单箱线图.
GRAPH
  /BOXPLOT(SIMPLE)=score.

* 分组箱线图.
GRAPH
  /BOXPLOT(SIMPLE)=score BY group.

* 多变量箱线图.
GRAPH
  /BOXPLOT(MULTIPLE)=score1 score2 score3.
```

### 2.3 条形图 (分类变量频率)

```spss
* 简单条形图.
GRAPH
  /BAR(SIMPLE)=COUNT BY gender.

* 分组条形图.
GRAPH
  /BAR(GROUPED)=COUNT BY edu BY gender.

* 带均值和误差棒的条形图.
GRAPH
  /BAR(SIMPLE)=MEAN(score) BY group
  /INTERVAL CI(95.0).

* 带标准误的条形图.
GRAPH
  /BAR(SIMPLE)=MEAN(score) BY group
  /INTERVAL SE(1.0).
```

### 2.4 散点图 (两变量关系)

```spss
* 简单散点图.
GRAPH
  /SCATTERPLOT(BIVAR)=x WITH y.

* 分组散点图.
GRAPH
  /SCATTERPLOT(BIVAR)=x WITH y BY group.

* 带回归线的散点图.
GRAPH
  /SCATTERPLOT(BIVAR)=x WITH y
  /REGRESSION=LINEAR CI(95).

* 散点图矩阵.
GRAPH
  /SCATTERPLOT(MATRIX)=var1 var2 var3 var4.
```

### 2.5 折线图 (趋势/交互)

```spss
* 时间趋势.
GRAPH
  /LINE(SIMPLE)=MEAN(score) BY time.

* 交互效应图 (X 轴: time, 分组线: group).
GRAPH
  /LINE(MULTIPLE)=MEAN(score) BY time BY group.

* 带误差棒的折线图.
GRAPH
  /LINE(MULTIPLE)=MEAN(score) BY time BY group
  /INTERVAL CI(95.0).
```

### 2.6 饼图 (比例)

```spss
GRAPH
  /PIE=COUNT BY group.
```

### 2.7 Q-Q 图 (正态性检查)

```spss
* 正态 Q-Q 图.
GRAPH
  /QQ(NORMAL)=score.

* 分组 Q-Q 图.
GRAPH
  /QQ(NORMAL)=score BY group.
```

### 2.8 P-P 图 (概率图)

```spss
GRAPH
  /PP(NORMAL)=score.
```

### 2.9 误差棒图

```spss
* 95% CI 误差棒.
GRAPH
  /BAR(SIMPLE)=MEAN(score) BY group
  /INTERVAL CI(95.0).

* 标准误误差棒.
GRAPH
  /BAR(SIMPLE)=MEAN(score) BY group
  /INTERVAL SE(2.0).

* 标准差误差棒.
GRAPH
  /BAR(SIMPLE)=MEAN(score) BY group
  /INTERVAL SD(1.0).
```

### 2.10 组合图 (多面板)

```spss
GRAPH
  /SCATTERPLOT(BIVAR)=iv WITH dv BY group
  /PANEL ROWVAR=group COLVAR=group.
```

---

## 三、图表定制

### 3.1 修改标题和标签

通过 Chart Editor（双击图表）修改：
- 双击图表打开 Chart Editor
- 双击标题/轴标签直接编辑
- 右键元素 → Properties 修改颜色、字体、线型

### 3.2 通过模板批量应用

```spss
* 保存图表模板.
GRAPH
  /SCATTERPLOT(BIVAR)=x WITH y
  /TEMPLATE='my_template.sgt'.
```

### 3.3 通过语法设置图表外观

```spss
* 设置图表默认外观.
SET CBACK=WHITE CBRUSH=BLUE CBARS=1.
* CBACK: 背景色
* CBRUSH: 默认填充色
* CBARS: 条形图样式
```

---

## 四、论文图表规范

### 4.1 通用要求

| 要求 | 说明 |
|------|------|
| 清晰可读 | 字号 ≥ 8pt，避免过密 |
| 黑白兼容 | 即使彩色打印，黑白也能区分 |
| 标题规范 | 图标题在下方，表标题在上方 |
| 编号连续 | 图 1、图 2...；表 1、表 2... |
| 独立可读 | 不看正文也能理解图表含义 |
| 单位标注 | 轴标签包含单位 |
| 误差标注 | 说明是 CI、SE 还是 SD |

### 4.2 导出设置

```spss
* 导出为高分辨率 PNG.
OUTPUT EXPORT
  /CONTENTS EXPORT=ALL
  /PNG IMAGFILE='C:\output\chart.png'
  WIDTH=1200 HEIGHT=800 PERCENT=100.

* 导出为矢量格式 (推荐用于论文).
OUTPUT EXPORT
  /CONTENTS EXPORT=ALL
  /EMF IMAGFILE='C:\output\chart.emf'.

* 导出为 PDF.
OUTPUT EXPORT
  /CONTENTS EXPORT=VISIBLE
  /PDF DOCUMENTFILE='C:\output\charts.pdf'.
```

### 4.3 各分析类型的推荐图表

| 分析类型 | 推荐图表 | 说明 |
|---------|---------|------|
| t 检验 (两组) | 分组箱线图 | 展示分布和中位数差异 |
| ANOVA (多组) | 分组条形图 + 95% CI 误差棒 | 可加显著性标记 |
| 交互效应 | 分组折线图 | X 轴为因素A，线为因素B |
| 相关 | 散点图 + 回归线 | 展示方向和强度 |
| 回归残差 | 残差 vs 预测值散点图 | 检验等方差 |
| 回归残差 | 标准化残差 Q-Q 图 | 检验正态性 |
| 频率分布 | 直方图 (连续) / 条形图 (分类) | 连续变量用直方图 |
| 因子分析 | 碎石图 | 确定因子数 |
| 信度分析 | 项间相关矩阵热力图 | 可用 SPSS 或导出数据绘制 |
| 中介效应 | 路径图 (需手动绘制) | 标注 a, b, c' 系数 |
| 生存分析 | 生存曲线 | 比较各组生存率 |
| ROC | ROC 曲线 | 展示 AUC |
| 聚类 | 树状图 (层次聚类) | 展示聚类过程 |
| 判别分析 | 判别函数得分散点图 | 展示组间分离 |
