# IBM SPSS Statistics MCP Server

**让 AI Agent 直接调用你电脑上的 IBM SPSS** — 自动执行分析、返回结果、解读输出。

## 工作原理

```
你的对话 → AI Agent → MCP Server → 本地 IBM SPSS → 结果返回 → AI 解读
```

安装后，AI 可以：
- 打开你的 SPSS 数据文件（.sav / .csv / .xlsx）
- 自动执行任何统计分析（t 检验、ANOVA、回归、因子分析……）
- 直接获取分析结果并解读
- 导出报告为 Word / HTML / PDF

**所有计算都在你的本地 SPSS 中完成，数据不会离开你的电脑。**

---

## 系统要求

| 要求 | 说明 |
|------|------|
| **IBM SPSS Statistics** | v24 或更高版本，已安装在本地 |
| **Python** | 3.9 或更高版本 |
| **SPSS Python 插件** | SPSS 菜单 → Utilities → Install Python Plug-in |

---

## 安装

### 方式一：pip 安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/chengamki-tech/ibm-spss-assistant.git

# 安装 MCP Server
cd ibm-spss-assistant/mcp-server
pip install -e .
```

### 方式二：直接安装依赖

```bash
pip install mcp
```

然后手动配置（见下方"配置"）。

---

## 配置

### Claude Code

在你的项目根目录或 `~/.claude/` 下创建 `.mcp.json`：

```json
{
  "mcpServers": {
    "spss": {
      "command": "python",
      "args": ["-m", "spss_mcp"],
      "env": {}
    }
  }
}
```

如果你安装了 `spss-mcp-server` 包：

```json
{
  "mcpServers": {
    "spss": {
      "command": "spss-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

### 指定 SPSS 安装路径（如果自动检测失败）

```json
{
  "mcpServers": {
    "spss": {
      "command": "python",
      "args": ["-m", "spss_mcp"],
      "env": {
        "SPSS_HOME": "C:\\Program Files\\IBM\\SPSS\\Statistics\\28"
      }
    }
  }
}
```

---

## 可用工具

安装后，AI Agent 获得以下 26 个工具：

### 系统管理
| 工具 | 功能 |
|------|------|
| `spss_connect` | 连接本地 SPSS（自动检测安装路径） |
| `spss_status` | 查看连接状态和 SPSS 版本 |
| `spss_disconnect` | 断开连接 |

### 数据管理
| 工具 | 功能 |
|------|------|
| `spss_open_data` | 打开数据文件（.sav / .csv / .xlsx） |
| `spss_get_variables` | 列出所有变量（名称、类型、标签、测量层次） |
| `spss_get_summary` | 获取描述统计摘要 |
| `spss_save_data` | 保存数据文件 |

### 快捷分析
| 工具 | 功能 |
|------|------|
| `spss_descriptives` | 描述统计 |
| `spss_frequency` | 频率分析 + 条形图 |
| `spss_explore` | 探索性分析（含正态性检验 + 箱线图） |
| `spss_normality` | 正态性检验（Shapiro-Wilk / K-S） |
| `spss_levenes` | Levene 方差齐性检验 |
| `spss_ttest` | 独立样本 t 检验 |
| `spss_ttest_paired` | 配对样本 t 检验 |
| `spss_anova` | 单因素 ANOVA + 事后检验 |
| `spss_correlation` | 相关分析（Pearson / Spearman） |
| `spss_regression` | 线性回归（含 VIF、残差诊断） |
| `spss_crosstab` | 交叉表 + 卡方检验 |
| `spss_reliability` | 信度分析（Cronbach's α） |
| `spss_factor` | 探索性因子分析（EFA） |
| `spss_logistic` | 逻辑回归 |
| `spss_means_compare` | 均值比较（ANOVA 表） |

### 通用执行
| 工具 | 功能 |
|------|------|
| `spss_execute_syntax` | 执行任意 SPSS Syntax |
| `spss_run_analysis` | 按类型执行分析（支持 19 种分析类型） |

### 输出导出
| 工具 | 功能 |
|------|------|
| `spss_export_output` | 导出输出（HTML / Word / PDF / PNG） |
| `spss_export_chart` | 导出图表 |
| `spss_clear_output` | 清空输出窗口 |

---

## 使用示例

### 基本流程

```
你: 帮我分析 data.sav 里的数据，比较男女在成绩上的差异

AI: [调用 spss_connect → 连接 SPSS]
    [调用 spss_open_data → 打开 data.sav]
    [调用 spss_get_variables → 查看变量]
    [调用 spss_ttest → 执行独立样本 t 检验]
    → 输出结果并解读：
    "独立样本 t 检验结果表明，女生 (M=82.3, SD=11.2) 的成绩
     显著高于男生 (M=74.2, SD=13.6)，t(198)=3.42, p=.001,
     Cohen's d=0.66。"
```

### 复杂分析

```
你: 对问卷数据做因子分析和信度检验

AI: [调用 spss_factor → 探索性因子分析]
    [调用 spss_reliability → 各维度信度分析]
    → 输出结果并解读：
    "KMO=.85，Bartlett 检验显著 (p<.001)，适合做因子分析。
     提取 3 个因子，累计方差解释率 62.3%。
     各维度 Cronbach's α 分别为 .87, .82, .79，信度良好。"
```

### 直接执行语法

```
你: 帮我做一个中介效应分析

AI: [调用 spss_execute_syntax → 执行 PROCESS 宏语法]
    → 输出结果并解读
```

---

## `spss_run_analysis` 支持的分析类型

| 类型 | 参数 | 说明 |
|------|------|------|
| `descriptives` | variables | 描述统计 |
| `frequency` | variables, chart | 频率分析 |
| `ttest` | dv, group, groups, paired | t 检验 |
| `anova` | dv, factor, posthoc | 方差分析 |
| `correlation` | variables, method | 相关分析 |
| `regression` | dv, ivs, method | 回归分析 |
| `crosstab` | row_var, col_var | 交叉表 |
| `reliability` | items, scale_name | 信度分析 |
| `factor` | variables, extraction, rotation | 因子分析 |
| `logistic` | dv, ivs | 逻辑回归 |
| `nonparametric` | test, dv, group, variables | 非参数检验 |
| `glm` | dv, factors | 一般线性模型 |
| `mixed` | dv, fixed, random_subject | 混合线性模型 |
| `survival` | time, status, group, covariates | 生存分析 |
| `roc` | test_var, state_var, state_value | ROC 曲线 |
| `cluster` | method, variables, n_clusters | 聚类分析 |
| `discriminant` | group, variables | 判别分析 |
| `curve` | y, x, models | 曲线估计 |
| `tree` | target, predictors, method | 决策树 |

---

## 故障排除

### "IBM SPSS Statistics not found"

确保 SPSS 已安装。如果安装在非标准路径，在 `.mcp.json` 中设置 `SPSS_HOME`：

```json
"env": {
  "SPSS_HOME": "你的 SPSS 安装路径"
}
```

### "Could not connect to SPSS"

确保 SPSS Python 插件已安装：
1. 打开 SPSS
2. 菜单 → Utilities → Install Python Plug-in
3. 重启 SPSS 和 AI Agent

### "ModuleNotFoundError: No module named 'mcp'"

```bash
pip install mcp
```

---

## 技术规格

- **协议**: MCP (Model Context Protocol) over stdio
- **SPSS 连接**: Python spss 模块 → 命令行 → COM 自动化（三级回退）
- **输出捕获**: OMS (Output Management System) → HTML → 解析为纯文本
- **安全**: 所有计算在本地 SPSS 完成，数据不离开本机
- **平台**: Windows / macOS / Linux

---

## License

MIT License
