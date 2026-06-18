# IBM SPSS Assistant

**IBM SPSS Statistics 智能助手** — 一套 6 个 Claude Code Skill，覆盖从数据清洗到论文投稿的全流程。

> 不是代替 SPSS 做分析，而是帮你在最关键的地方少走弯路：**该做什么分析、结果说明什么、怎么写进论文**。

---

## 功能一览

### 6 个 Skill

| Skill | 定位 | 核心功能 |
|-------|------|---------|
| `/spss-interpreter` | **结果解读** | 贴入 SPSS 输出 → 逐项解释指标含义 + 显著性综合判断 |
| `/spss-what-test` | **检验推荐** | 描述变量和研究问题 → 交互式推荐最合适的统计方法 |
| `/spss-guide` | **流程向导** | 从数据导入到报告，五步流程引导新手走完整个分析 |
| `/spss-syntax` | **语法生成** | 描述分析需求 → 生成带注释、可复现的 SPSS Syntax |
| `/spss-cleaning` | **数据清洗** | 缺失值/异常值/编码/重复检查 → 生成清洗脚本 |
| `/spss-report` | **论文报告** | 统计结果 → 中文论文"结果"段落 + 讨论草稿 |

### 8 份参考文档

| 文档 | 内容 |
|------|------|
| `test-selection-guide.md` | 统计检验选择决策树（5 大分支） |
| `interpretation-templates.md` | 12 种分析的结果解读模板 |
| `paper-expressions.md` | 中文论文统计表述模板（含讨论段落） |
| `questionnaire-template.md` | 问卷分析标准流程（含多选题、中介/调节） |
| `syntax-reference.md` | SPSS Syntax 精简速查卡 |
| `advanced-analysis-guide.md` | 中介/调节/MANOVA/功效分析/回归诊断 |
| `error-troubleshooting.md` | SPSS 常见错误排查手册 |
| `power-analysis-sample-size.md` | 统计功效与样本量计算指南 |

---

## 覆盖的统计方法

### 基础分析
- 描述统计（频率、均值、标准差、偏度/峰度）
- 正态性检验（Shapiro-Wilk、K-S）
- t 检验（独立/配对/单样本）
- 方差分析（单因素/双因素/重复测量/Welch）
- 相关分析（Pearson/Spearman/Kendall/偏相关）
- 卡方检验 / Fisher 精确检验
- 非参数检验（Mann-Whitney / Kruskal-Wallis / Wilcoxon / Friedman）

### 回归建模
- 线性回归（简单/多元/层次/逐步）
- 逻辑回归（二元/有序/多项）
- 曲线估计

### 量表开发
- 探索性因子分析（EFA）
- 信度分析（Cronbach's α）

### 高级分析
- 多元方差分析（MANOVA）
- 中介效应（Baron-Kenny + Bootstrap）
- 调节效应（交互项 + 简单斜率）
- 统计功效与样本量计算

---

## 安装

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

```bash
cd your-project
mkdir -p .claude/plugins
cp -r /path/to/ibm-spss-assistant .claude/plugins/
```

---

## 使用示例

### 场景一：课程作业 / 毕业论文

```
1. /spss-guide            → 一步步引导整个分析流程
2. /spss-cleaning         → 数据清洗检查
3. /spss-interpreter      → 解读 SPSS 输出
4. /spss-report           → 生成论文"结果"段落
```

### 场景二：不知道该用什么方法

```
/spss-what-test 我有两组学生（翻转课堂 vs 传统教学），
想比较他们的期末成绩和学习满意度，该用什么统计方法？
```

### 场景三：看不懂 SPSS 输出

```
/spss-interpreter 帮我看看这个回归分析结果：
[粘贴 SPSS 输出表格]
```

### 场景四：需要批量跑分析

```
/spss-syntax 我有 5 个因变量（score1 到 score5），
都要按 group 做独立样本 t 检验，帮我想办法批量跑。
```

### 场景五：写论文卡在"结果"部分

```
/spss-report 帮我把这个 t 检验结果写成论文里的结果段落：
实验组 M=82.35, SD=11.24；对照组 M=74.18, SD=13.56；
t(98)=3.42, p=.001, Cohen's d=0.66
```

### 场景六：分析结果不显著，不知道怎么办

```
/spss-report 结果不显著，p = .089，效应量 d = 0.35，
样本量每组 40 人，帮我写进论文并讨论功效问题。
```

---

## 适合谁用

| 用户类型 | 典型需求 | 推荐 Skill |
|---------|---------|-----------|
| **本科生** | 课程作业、期末论文 | guide → cleaning → interpreter → report |
| **研究生** | 学位论文、课题研究 | what-test → guide → cleaning → syntax → interpreter → report |
| **初学者** | 第一次用 SPSS | guide（从头带你走） |
| **教师** | 批改作业、教学示例 | interpreter + report |
| **研究人员** | 论文写作、数据分析 | syntax + interpreter + cleaning + report |

---

## 常见问题 (FAQ)

### Q: 这个插件需要安装 SPSS 吗？
A: 不需要。这个插件是 Claude Code 的 Skill，帮你理解、生成语法和撰写报告。实际的 SPSS 操作需要你自己的 SPSS 软件。

### Q: 生成的语法能直接在 SPSS 里运行吗？
A: 是的，生成的语法可以直接复制到 SPSS Syntax Editor 中运行。但请检查变量名是否与你的数据文件一致。

### Q: 支持中文版 SPSS 吗？
A: 支持。生成的语法和解读适用于中英文版 SPSS。如果你运行中文版 SPSS，输出表格的标题可能是中文的，skill 能够识别。

### Q: 结果解读准确吗？
A: 插件基于统计学标准方法进行解读，但不能替代你对数据和研究设计的理解。建议将解读结果作为参考，结合你的专业知识做出最终判断。

### Q: 能处理多大的数据集？
A: 这个插件不直接处理数据——它帮你生成语法和解读结果。SPSS 本身可以处理数十万行数据。

### Q: 和 G*Power 是什么关系？
A: G*Power 是统计功效计算的独立软件。插件中的 `power-analysis-sample-size.md` 参考文档教你如何使用 G*Power 进行样本量计算和功效分析。

---

## 技术规格

- **基于**：[Agent Skills 开放标准](https://agentskills.io)
- **兼容**：Claude Code（CLI、桌面版、VS Code / JetBrains 扩展）
- **运行要求**：无需额外依赖，无需网络请求
- **语言**：简体中文为主，统计术语保留英文原名
- **版本**：2.0.0
- **License**：MIT

---

## 更新日志

### v2.0.0 (2026-06-18)

**新增 Skill**：
- `/spss-what-test` — 交互式统计检验推荐向导

**新增参考文档**：
- `advanced-analysis-guide.md` — 中介/调节/MANOVA/功效/回归诊断/重复测量
- `error-troubleshooting.md` — SPSS 常见错误排查手册
- `power-analysis-sample-size.md` — 统计功效与样本量计算指南

**增强功能**：
- spss-interpreter：增加高级分析支持（MANOVA、中介/调节）、诊断问题表、术语速查表
- spss-guide：增加问卷分析模板、毕业论文提醒、常见新手误区
- spss-syntax：增加完整数据管理、批处理、中介回归、输出管理、错误排查
- spss-cleaning：增加正态性转换、标准化、哑变量编码、数据合并/重塑
- spss-report：增加全分析类型模板、非显著结果表述、讨论段落、功效报告、6 种表格模板

**改进**：
- 统一版本号至 2.0.0
- 更新 plugin.json 中文描述和关键词
- 语法参考文档去重精简

### v1.0.0 (2026-06-18)

- 初始发布：5 个 Skill + 5 份参考文档

---

## 项目结构

```
ibm-spss-assistant/
├── .claude-plugin/
│   └── plugin.json                          # 插件清单
├── skills/
│   ├── spss-interpreter/SKILL.md            # 结果解读 + 分析推荐
│   ├── spss-what-test/SKILL.md              # 检验推荐向导 (新增)
│   ├── spss-guide/SKILL.md                  # 统计流程向导
│   ├── spss-syntax/SKILL.md                 # 语法生成器
│   ├── spss-cleaning/SKILL.md               # 数据清洗检查
│   └── spss-report/SKILL.md                 # 论文报告生成
├── references/
│   ├── test-selection-guide.md              # 检验选择决策树
│   ├── interpretation-templates.md          # 结果解读模板
│   ├── paper-expressions.md                 # 中文论文表述模板
│   ├── questionnaire-template.md            # 问卷分析标准流程
│   ├── syntax-reference.md                  # Syntax 精简速查卡
│   ├── advanced-analysis-guide.md           # 高级分析指南 (新增)
│   ├── error-troubleshooting.md             # 错误排查手册 (新增)
│   └── power-analysis-sample-size.md        # 功效与样本量指南 (新增)
├── README.md
└── LICENSE
```

---

## 贡献

欢迎提交 Issue 和 Pull Request！

如果你想添加新的统计方法支持、改进解读模板、或增加其他语言版本，请参考现有 Skill 的格式提交。

---

## License

[MIT License](LICENSE)
