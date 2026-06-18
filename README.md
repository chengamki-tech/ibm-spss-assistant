# IBM SPSS Assistant

**IBM SPSS Statistics 智能助手** — 一套 Claude Code Skill 插件，专门面向使用 SPSS 做统计分析的学生、研究人员和教师。

> 不是代替 SPSS 做分析，而是帮你在最关键的地方少走弯路：**该做什么分析、结果说明什么、怎么写进论文**。

---

## 🎯 定位：解决三个核心问题

| 问题 | 困境 | 解决方式 |
|------|------|---------|
| **该做什么分析** | 面对一堆变量不知道用什么检验 | 根据变量类型和研究设计，自动推荐最合适的统计方法 |
| **结果说明什么** | SPSS 输出一堆表格看不懂 | 把每个指标翻译成"这说明了什么"的通俗解释 |
| **怎么写进论文** | 不知道怎么用学术语言表述统计结果 | 自动生成符合中文论文规范的"结果"段落 |

---

## 📦 包含 5 个 Skill

### 1. `/spss-interpreter` — 结果解读 + 分析推荐

**解决的问题**：看不懂 SPSS 输出表格；不知道该用什么统计方法。

**核心功能**：
- **分析方法推荐**：告诉它你有几个变量、变量类型（名义/有序/连续）、研究目的，它会推荐最合适的检验方法，附带前提假设检查提醒
- **结果表格解读**：贴入 SPSS 输出，逐项解释各指标含义（p 值、效应量、置信区间、F 值等）
- **显著性综合判断**：不止看 p 值，同时报告效应量和置信区间，避免"统计显著 ≠ 实际重要"的误判

**支持的分析类型**：
- t 检验（独立样本 / 配对样本）
- 方差分析（单因素 / 双因素 / 重复测量）
- 卡方检验 / Fisher 精确检验
- 相关分析（Pearson / Spearman）
- 线性回归 / 逻辑回归
- 因子分析（探索性）
- 信度分析（Cronbach's α）

**使用示例**：
```
/spss-interpreter 帮我看看这个回归分析结果是什么意思：
[粘贴 SPSS 输出表格]
```
```
/spss-interpreter 我有两组学生（传统教学 vs 翻转课堂），
想比较他们的期末成绩，该用什么检验？
```

---

### 2. `/spss-guide` — 统计流程向导

**解决的问题**：拿到数据不知道从哪开始；在 SPSS 菜单里迷路。

**核心功能**：
- **五步标准流程引导**：数据检查 → 描述统计 → 假设检验 → 建模 → 报告，每一步给出具体操作和 SPSS 菜单路径
- **问卷分析专用模板**：信度分析 → 描述统计 → 交叉表 → t 检验 → ANOVA → 相关 → 回归，按顺序带过整个流程
- **菜单路径 + 语法双轨**：告诉你在菜单里点哪里的同时，提供等效的 SPSS Syntax

**使用示例**：
```
/spss-guide 我做了一份问卷调查，有 300 份有效问卷，
想分析不同性别的学生在学习动机上的差异，应该怎么做？
```
```
/spss-guide 我的数据已经录入好了，下一步该做什么？
```

---

### 3. `/spss-syntax` — 语法生成器

**解决的问题**：想用 Syntax 做可复现分析但语法记不住；要批量跑多个变量的同一套分析。

**核心功能**：
- **智能语法生成**：描述你的分析需求，自动生成完整、带注释、可直接运行的 SPSS Syntax
- **批处理语法**：用 `DO REPEAT` 循环对多个变量、多个分组重复执行同一套分析
- **语法错误排查**：贴入报错信息，帮你定位问题（漏了句号、变量名拼错、子命令顺序不对等）
- **参数解释**：每个子命令和参数都附带中文说明

**支持生成的语法**：
- 变量定义与标签（VARIABLE LABELS / VALUE LABELS）
- 描述统计（FREQUENCIES / DESCRIPTIVES / EXAMINE）
- t 检验 / ANOVA / 相关 / 回归 / 卡方 / 因子分析 / 信度分析
- 数据管理（RECODE / COMPUTE / SELECT IF / SPLIT FILE）
- 输出导出（HTML / Word / 图片）

**使用示例**：
```
/spss-syntax 帮我生成独立样本 t 检验的语法，
自变量是性别（1=男 2=女），因变量是学习动机得分。
```
```
/spss-syntax 我有 5 个因变量（score1 到 score5），
都要按 group 做 t 检验，帮我想办法批量跑。
```

---

### 4. `/spss-cleaning` — 数据清洗检查

**解决的问题**：数据里有缺失值、异常值、编码不一致；不知道该怎么处理。

**核心功能**：
- **缺失值分析**：判断缺失类型（MCAR/MAR/MNAR），根据缺失比例推荐处理方案（删除/均值插补/多重插补）
- **异常值检测**：箱线图法（IQR）、Z-score 法，附 Winsorize 处理语法
- **变量类型检查**：名义/有序/连续的测量层次设置是否正确
- **编码一致性验证**：反向计分题是否已处理、编码是否混用
- **重复样本检查**：自动检测重复个案
- **生成清洗脚本**：一键生成完整的数据清洗 SPSS Syntax

**使用示例**：
```
/spss-cleaning 帮我检查一下数据，看看有没有缺失值和异常值
```
```
/spss-cleaning 我的问卷里有 3 个反向计分题（item3、item5、item7），
帮我生成反向编码的语法
```

---

### 5. `/spss-report` — 论文报告生成

**解决的问题**：分析做完了但不知道怎么写成学术语言；统计表述格式不规范。

**核心功能**：
- **中文论文统计段落生成**：把统计结果直接整理成"结果"段落，符合国内期刊和学位论文规范
- **APA 7 格式**：精确 p 值、斜体统计量、正确的小数位数和空格
- **必报指标提醒**：效应量、置信区间、自由度——一个都不漏
- **图表建议**：告诉你该用柱状图、箱线图、散点图还是直方图，以及为什么
- **表格模板**：描述统计表、t 检验结果表、回归系数表等标准格式

**支持的表述格式**：
- t 检验（独立/配对）
- 方差分析（单因素/双因素/重复测量）
- 相关分析（Pearson/Spearman）
- 回归分析（线性/层次/逻辑）
- 卡方检验 / Fisher 精确检验
- 因子分析 / 信度分析

**使用示例**：
```
/spss-report 帮我把这个 t 检验结果写成论文里的结果段落：
实验组 M=82.35, SD=11.24；对照组 M=74.18, SD=13.56；
t(98)=3.42, p=.001, Cohen's d=0.66
```
```
/spss-report 我做了一个三组的单因素方差分析，结果显著，
事后检验显示 A 组和 B 组有差异，帮我在论文里表述
```

---

## 📚 参考文档（5 份）

插件附带完整的统计参考资料，Claude 会在需要时自动读取：

| 文件 | 内容 | 适用场景 |
|------|------|---------|
| `references/test-selection-guide.md` | 统计检验选择决策树 | 不知道该用什么方法时 |
| `references/interpretation-templates.md` | 各类分析结果解读模板 | 看不懂输出时 |
| `references/paper-expressions.md` | 中文论文统计表述模板 | 写论文结果段落时 |
| `references/questionnaire-template.md` | 问卷分析标准流程 | 做问卷研究时 |
| `references/syntax-reference.md` | 常用 SPSS Syntax 速查 | 需要语法参考时 |

---

## 🚀 安装

### 方式一：一行命令（推荐）

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### 方式二：克隆到本地

```bash
git clone https://github.com/chengamki-tech/ibm-spss-assistant.git

# Windows
xcopy /E /I ibm-spss-assistant %USERPROFILE%\.claude\plugins\ibm-spss-assistant

# macOS / Linux
cp -r ibm-spss-assistant ~/.claude/plugins/
```

### 方式三：作为项目级 Skill

如果你只想在某个项目中使用：

```bash
cd your-project
mkdir -p .claude/plugins
cp -r /path/to/ibm-spss-assistant .claude/plugins/
```

---

## 📖 使用流程建议

### 场景一：课程作业 / 毕业论文

```
1. /spss-guide          → 从数据导入开始，一步步引导你走完整个流程
2. /spss-cleaning       → 数据录入完后，跑一遍清洗检查
3. /spss-interpreter    → 分析完成后，贴入输出看懂每个指标
4. /spss-report         → 最后把结果整理成论文格式
```

### 场景二：拿到一堆 SPSS 输出不知道怎么看

```
1. /spss-interpreter    → 直接贴入输出表格，逐项解读
```

### 场景三：需要批量跑分析

```
1. /spss-syntax         → 描述需求，生成批处理语法
2. /spss-interpreter    → 看结果，理解输出
```

### 场景四：写论文卡在"结果"部分

```
1. /spss-report         → 给出关键数字，生成符合规范的段落
```

---

## 💡 适合谁用

| 用户类型 | 典型需求 | 推荐 Skill |
|---------|---------|-----------|
| **本科生** | 课程作业、期末论文 | `spss-guide` + `spss-interpreter` + `spss-report` |
| **研究生** | 学位论文、课题研究 | 全部 5 个 Skill |
| **教师** | 批改作业、教学示例 | `spss-interpreter` + `spss-report` |
| **研究人员** | 论文写作、数据分析 | `spss-syntax` + `spss-interpreter` + `spss-cleaning` |
| **初学者** | 第一次用 SPSS | `spss-guide`（从头带你走） |

---

## 📁 项目结构

```
ibm-spss-assistant/
├── .claude-plugin/
│   └── plugin.json                    # 插件清单
├── skills/
│   ├── spss-interpreter/SKILL.md      # 结果解读 + 分析推荐
│   ├── spss-guide/SKILL.md            # 统计流程向导
│   ├── spss-syntax/SKILL.md           # 语法生成器
│   ├── spss-cleaning/SKILL.md         # 数据清洗检查
│   └── spss-report/SKILL.md           # 论文报告生成
├── references/
│   ├── test-selection-guide.md        # 统计检验选择决策树
│   ├── interpretation-templates.md    # 各类分析结果解读模板
│   ├── paper-expressions.md           # 中文论文统计表述模板
│   ├── questionnaire-template.md      # 问卷分析标准流程
│   └── syntax-reference.md            # 常用 SPSS Syntax 速查
├── README.md
└── LICENSE
```

---

## 📋 支持的统计方法一览

### 比较差异
| 方法 | 适用条件 |
|------|---------|
| 独立样本 t 检验 | 两组独立样本，连续因变量 |
| 配对样本 t 检验 | 同一批被试前后测比较 |
| 单因素 ANOVA | 三组及以上独立样本 |
| 双因素 ANOVA | 两个自变量对一个因变量的影响 |
| 重复测量 ANOVA | 同一批被试多个时间点测量 |
| Mann-Whitney U | 两组，非正态数据 |
| Kruskal-Wallis | 多组，非正态数据 |

### 探索关联
| 方法 | 适用条件 |
|------|---------|
| Pearson 相关 | 两个连续变量，双变量正态 |
| Spearman 相关 | 非正态或有序变量 |
| 卡方检验 | 两个分类变量的关联 |
| Fisher 精确检验 | 期望频数 < 5 时替代卡方 |

### 预测建模
| 方法 | 适用条件 |
|------|---------|
| 线性回归 | 预测连续因变量 |
| 逻辑回归 | 预测二分类因变量 |
| 层次回归 | 控制变量后检验核心变量效应 |

### 量表开发
| 方法 | 适用条件 |
|------|---------|
| 探索性因子分析 | 量表结构探索 |
| Cronbach's α 信度 | 量表内部一致性检验 |

---

## ⚙️ 技术规格

- **基于**：[Agent Skills 开放标准](https://agentskills.io)
- **兼容**：Claude Code（CLI、桌面版、VS Code / JetBrains 扩展）
- **运行要求**：无需额外依赖，无需网络请求
- **语言**：简体中文为主，术语保留英文原名
- **License**：MIT

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

如果你想添加新的统计方法支持、改进解读模板、或增加其他语言版本，请参考现有 Skill 的格式提交。

---

## 📄 License

[MIT License](LICENSE)
