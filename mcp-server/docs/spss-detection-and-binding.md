# SPSS 本地程序查找与 MCP 绑定原理

> 本文档解释 MCP Server 如何自动发现用户电脑上的 IBM SPSS Statistics，并建立通信。适用于所有支持 MCP 的 AI Agent（Claude Code、Codex、Gemini CLI、Cursor 等）。

---

## 一、整体架构

```
AI Agent
   │
   ├─ 读取 .mcp.json → 发现 spss 服务
   │
   ├─ 启动 MCP Server 进程 (python -m spss_mcp)
   │      │
   │      ├─ spss_connect 被调用
   │      │      │
   │      │      ├─ 第1步: 扫描 Windows 注册表
   │      │      ├─ 第2步: 检查 SPSS_HOME 环境变量
   │      │      ├─ 第3步: 遍历常见安装路径
   │      │      ├─ 第4步: macOS/Linux 用 which stats
   │      │      │
   │      │      └─ 找到 stats.exe → 定位 Python 模块路径
   │      │
   │      ├─ 第5步: 加载 SPSS Python 模块 (import spss)
   │      │      ├─ 成功 → 使用 spss_module 后端
   │      │      └─ 失败 → 回退到命令行执行
   │      │
   │      └─ 连接成功 → 开始接受工具调用
   │
   └─ AI Agent 调用工具 (spss_ttest, spss_regression, ...)
          → MCP Server 生成 SPSS Syntax
          → 通过连接发送给 SPSS 执行
          → OMS 捕获输出 → 返回给 AI Agent
```

---

## 二、第一步：查找 SPSS 程序 (stats.exe)

### 2.1 Windows 注册表查找

IBM SPSS 安装时会写入注册表。这是最可靠的检测方式。

```
注册表路径:
  HKEY_LOCAL_MACHINE\SOFTWARE\IBM\SPSS Statistics\28.0
    InstallDir → C:\Program Files\IBM\SPSS\Statistics\28

  HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\IBM\SPSS Statistics\28.0
    InstallDir → C:\Program Files (x86)\IBM\SPSS\Statistics\28

  HKEY_CURRENT_USER\SOFTWARE\IBM\SPSS Statistics\28.0
    InstallDir → C:\Users\xxx\AppData\Local\IBM\SPSS\Statistics\28
```

搜索策略：从最新版本（v40）向下遍历到 v24，确保找到最新安装。

代码实现（Windows Registry）：

```python
import winreg

def find_spss_via_registry():
    """扫描注册表查找 SPSS 安装路径"""
    registry_roots = [
        winreg.HKEY_LOCAL_MACHINE,
        winreg.HKEY_CURRENT_USER,
    ]
    registry_prefixes = [
        "SOFTWARE\\IBM\\SPSS Statistics",
        "SOFTWARE\\WOW6432Node\\IBM\\SPSS Statistics",
        "SOFTWARE\\IBM\\SPSS",
        "SOFTWARE\\WOW6432Node\\IBM\\SPSS",
    ]
    
    for version in range(40, 23, -1):       # 从新到旧
        for suffix in (f"{version}.0", str(version)):
            for prefix in registry_prefixes:
                for root in registry_roots:
                    try:
                        key = winreg.OpenKey(root, f"{prefix}\\{suffix}")
                        install_dir, _ = winreg.QueryValueEx(key, "InstallDir")
                        winreg.CloseKey(key)
                        return install_dir
                    except FileNotFoundError:
                        continue
    return None
```

### 2.2 环境变量查找

用户可以手动设置 `SPSS_HOME` 环境变量指向安装目录。

```python
def find_spss_via_env():
    home = os.environ.get("SPSS_HOME") or os.environ.get("SPSSTATHOME")
    if home and os.path.isdir(home):
        return home
    return None
```

### 2.3 常见路径遍历

很多用户直接默认安装，路径相对固定。遍历以下模式：

**Windows 常见路径**：
```
C:\Program Files\IBM\SPSS\Statistics\28\
C:\Program Files\IBM\SPSS\Statistics\29\
C:\Program Files\IBM\SPSS\28\
C:\Program Files\IBM\SPSS Statistics\
C:\Program Files\SPSS Inc\SPSS 28\
C:\SPSS\                              ← 用户自定义
D:\Program Files\IBM\SPSS\Statistics\28\
```

**macOS 常见路径**：
```
/Applications/IBM/SPSS/Statistics/28/
~/Applications/IBM/SPSS/Statistics/28/
```

**Linux 常见路径**：
```
/opt/ibm/SPSS/Statistics/28/
/usr/local/ibm/SPSS/Statistics/28/
```

### 2.4 定位可执行文件 (stats.exe)

找到安装目录后，在目录及子目录中查找可执行文件：

```
安装目录/
├── stats.exe         ← 主程序（命令行执行入口）
├── stats.com         ← 备选（部分版本）
├── spss.exe          ← 旧版本名称
├── spss.com
└── bin/
    └── stats         ← macOS / Linux 子目录
```

搜索逻辑：
```python
def find_executable(install_dir):
    exe_names = ["stats.exe", "stats.com", "spss.exe", "spss.com"]
    search_dirs = ["", "bin", "Statistics", "Bin"]
    
    for subdir in search_dirs:
        for name in exe_names:
            path = os.path.join(install_dir, subdir, name)
            if os.path.isfile(path):
                return path
    return None
```

---

## 三、第二步：建立与 SPSS 的通信

找到程序后，有三种方式与 SPSS 通信。按优先级依次尝试。

### 3.1 方式一：SPSS Python 模块（首选）

IBM SPSS 提供了 Python 扩展模块 `spss`，可以在 SPSS 进程内执行任意语法并访问数据。

**前提**：SPSS 安装时需要勾选 Python Integration Plug-in，或在 SPSS 菜单中手动安装。

**查找 Python 模块路径**：
```
安装目录/Python3/Lib/site-packages/    ← 包含 spss.pyd, spssaux.py 等
安装目录/Python/lib/python3.8/site-packages/
安装目录/Python3/lib/python3.10/site-packages/
```

**连接过程**：
```python
import sys
sys.path.insert(0, python_site_packages_path)  # 把 SPSS Python 路径加入搜索
import spss                                     # 导入 SPSS 模块

spss.Submit("")  # 初始化 SPSS 后端处理器（关键！）
```

**执行语法**：
```python
spss.Submit("GET FILE='C:/data/mydata.sav'.")
spss.Submit("DESCRIPTIVES VARIABLES=age income.")
```

**获取变量信息**：
```python
count = spss.GetVariableCount()
for i in range(count):
    name  = spss.GetVariableName(i)      # 如 "age"
    label = spss.GetVariableLabel(i)     # 如 "被试年龄"
    type_ = spss.GetVariableType(i)      # 0=数值, >0=字符串宽度
    level = spss.GetVariableMeasurementLevel(i)  # 0=Scale, 1=Ordinal, 2=Nominal
```

### 3.2 方式二：命令行执行（回退）

如果 Python 模块不可用，可以用命令行直接执行语法文件：

```bash
stats.exe -p syntax_file.sps
```

执行过程：
1. 将 SPSS Syntax 写入临时 `.sps` 文件
2. 调用 `stats.exe -p 临时文件.sps`
3. 在语法中使用 OMS 命令捕获输出
4. 读取 OMS 生成的输出文件

### 3.3 方式三：COM 自动化（Windows 专用）

Windows 下可用 COM 接口控制 SPSS：

```python
import win32com.client
app = win32com.client.Dispatch("SPSS.Application")
app.OpenSyntaxFile("temp.sps")
app.ExecuteSyntax()
output = app.OutputDocument  # 可访问输出文档
```

### 通信方式对比

| 方式 | 平台 | 优点 | 缺点 |
|------|------|------|------|
| Python 模块 | 全平台 | 最快、可直接访问数据 | 需要 SPSS Python 插件 |
| 命令行 | 全平台 | 不需要额外插件 | 无法访问数据，只能执行语法 |
| COM 自动化 | Windows | 可访问输出文档 | 仅 Windows，依赖 pywin32 |

---

## 四、第三步：输出捕获 (OMS)

SPSS 执行语法后，输出默认进入 Viewer。MCP Server 通过 OMS（Output Management System）捕获输出。

### OMS 工作原理

```
OMS 开始捕获 → SPSS 执行语法 → 输出被重定向到文件 → OMS 停止捕获
```

### 捕获为 HTML（推荐）

```spss
OMS /SELECT ALL /DESTINATION FORMAT=HTML OUTFILE='C:\temp\spss_output.html'.
DESCRIPTIVES VARIABLES=age income.
OMSEND.
```

输出文件是标准 HTML，包含格式化表格。

### HTML 转纯文本

MCP Server 将 OMS 输出的 HTML 转换为可读的纯文本返回给 AI：

```python
# 优先用 BeautifulSoup
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
# 提取表格行 → 用制表符分隔
# 提取段落文本
# 拼接为可读文本
```

如果没有 BeautifulSoup，用正则表达式回退处理。

---

## 五、绑定流程总结

```
用户安装:
  pip install -e mcp-server/
  claude --plugin-dir .

自动绑定:
  AI Agent 读取 .mcp.json
    → 启动 python -m spss_mcp 进程
    → AI 调用 spss_connect
    → 注册表扫描 → 找到 stats.exe 路径
    → 定位 Python 模块目录 → sys.path 加入
    → import spss → spss.Submit("") 初始化
    → 连接成功，26 个工具可用

用户使用:
  "帮我分析 data.sav 中男女成绩差异"
    → AI 调用 spss_open_data("data.sav")
    → AI 调用 spss_ttest(dv="score", group="gender")
    → MCP Server 生成 Syntax → 发送给 SPSS → OMS 捕获输出
    → AI 解读结果并写论文段落
```

---

## 六、扩展到其他本地程序

这个模式（自动查找 → 绑定 → 执行）可复用到任何有命令行或 Python 接口的桌面程序：

| 程序 | 查找方式 | 通信方式 |
|------|---------|---------|
| IBM SPSS | 注册表 + 常见路径 | Python 模块 / CLI |
| SAS | 注册表 + PATH | `sas` 命令行 |
| Stata | PATH | `stata-mp -b do file.do` |
| R | PATH / R_HOME | `Rscript` 命令行 |
| MATLAB | PATH / MATLAB_ROOT | `matlab -batch "code"` |
| Excel | COM | `win32com.client.Dispatch("Excel.Application")` |

核心逻辑一致：注册表/路径扫描 → 可执行文件定位 → 建立通信 → 执行 → 捕获输出。
