# IBM SPSS Assistant — Claude Code Skill

[English](#english) | [中文](#中文)

---

## 中文

### 这是什么

IBM SPSS Statistics 智能助手 — 一套 Claude Code skills，帮你搞定 SPSS 统计分析的三个核心问题：

1. **该做什么分析** — 根据变量类型和研究问题推荐统计方法
2. **结果说明什么** — 把 SPSS 输出表格翻译成通俗解释
3. **怎么写进论文** — 自动生成符合中文论文规范的统计表述

### 适用场景

| 场景 | 推荐 Skill |
|------|-----------|
| 看不懂 SPSS 输出 | `/spss-interpreter` |
| 不知道从哪开始分析 | `/spss-guide` |
| 需要生成 SPSS 语法 | `/spss-syntax` |
| 做数据清洗检查 | `/spss-cleaning` |
| 要写论文结果段落 | `/spss-report` |

### 安装

**方式一：直接从 GitHub 使用**

```bash
claude --plugin-dir https://github.com/user/ibm-spss-assistant
```

**方式二：手动安装**

```bash
# 克隆仓库
git clone https://github.com/user/ibm-spss-assistant.git

# 复制到 Claude Code 插件目录
cp -r ibm-spss-assistant ~/.claude/plugins/
```

**方式三：作为项目 skill**

```bash
# 在项目目录下
mkdir -p .claude/plugins/ibm-spss-assistant
cp -r ibm-spss-assistant/* .claude/plugins/ibm-spss-assistant/
```

### 使用示例

**结果解读** — 粘贴 SPSS 输出表格
```
/spss-interpreter 帮我看看这个回归分析的结果：
[粘贴 SPSS 输出]
```

**分析推荐** — 描述研究设计
```
/spss-interpreter 我有两组学生（传统教学 vs 翻转课堂），
想比较他们的期末成绩，该用什么检验？
```

**流程向导** — 不知道从哪开始
```
/spss-guide 我做了一份问卷调查，有 300 份有效问卷，
想分析不同性别的学生在学习动机上的差异。
```

**语法生成** — 需要可复现的语法
```
/spss-syntax 帮我生成独立样本 t 检验的语法，
自变量是性别（1=男 2=女），因变量是学习动机得分。
```

**数据清洗** — 检查数据质量
```
/spss-cleaning 帮我检查数据有没有缺失值和异常值。
```

**论文报告** — 生成统计段落
```
/spss-report 帮我把这个 t 检验结果写成论文里的结果段落：
t(98) = 3.42, p = .001, Cohen's d = 0.66
```

### Skills 一览

| Skill | 功能 | 触发词 |
|-------|------|--------|
| `spss-interpreter` | 结果解读 + 分析推荐 | SPSS结果、该用什么检验、p值 |
| `spss-guide` | 统计流程向导 | 统计分析步骤、问卷分析 |
| `spss-syntax` | 语法生成器 | SPSS语法、Syntax、批处理 |
| `spss-cleaning` | 数据清洗检查 | 缺失值、异常值、数据清洗 |
| `spss-report` | 论文报告生成 | 论文结果、写结果段落、APA格式 |

### 参考文档

- `references/test-selection-guide.md` — 统计检验选择决策树
- `references/interpretation-templates.md` — 各类分析结果解读模板
- `references/paper-expressions.md` — 中文论文统计表述模板
- `references/questionnaire-template.md` — 问卷分析标准流程
- `references/syntax-reference.md` — 常用 SPSS Syntax 速查

---

## English

### What is this

A Claude Code skill plugin for IBM SPSS Statistics — helps you answer three core questions:

1. **What analysis to run** — recommends statistical methods based on variable types and research questions
2. **What the results mean** — translates SPSS output tables into plain language explanations
3. **How to write it up** — generates APA-formatted result sections for papers

### Installation

```bash
claude --plugin-dir https://github.com/user/ibm-spss-assistant
```

### Usage

```
/spss-interpreter What test should I use to compare two groups?
/spss-guide Walk me through analyzing my survey data
/spss-syntax Generate syntax for independent samples t-test
/spss-cleaning Check my data for missing values and outliers
/spss-report Write up these t-test results for my paper
```

### License

MIT
