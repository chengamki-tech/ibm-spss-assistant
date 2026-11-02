# Local SPSS binding / 本地 SPSS 連接

The MCP client launches `spss-mcp` over stdio. Initialization and tool discovery
need no SPSS installation. Only `spss_connect` starts a local persistent worker.

1. `SPSS_PYTHON` selects an absolute SPSS-compatible Python executable.
2. Otherwise, explicit `spss_home` or `SPSS_HOME` is checked for Python in
   `Python3`, `Python`, `bin` or the home directory. There is no registry scan,
   COM attachment, shell command or network fallback.
3. That Python runs `spss_worker.py`, imports IBM's `spss` integration module and
   initializes the processor. The interpreter must match the SPSS integration ABI.
4. Newline-delimited UTF-8 JSON carries commands/results. Native SPSS stdout is
   discarded in the worker, keeping the MCP protocol clean; errors go to stderr.
5. A persistent worker retains the dataset. Calls are serialized; startup and
   commands time out via `SPSS_TIMEOUT`. Failures stop the worker without retries.
6. OMS HTML is captured in a private temporary directory and converted to text.
   Files are cleaned after success/failure; disconnect and server exit reap the
   worker. Abrupt OS termination cannot guarantee cleanup.

SPSS's GUI dataset is not shared. Open a data file explicitly. Only structured
file tools honor `SPSS_DATA_ROOT`; raw syntax is trusted code, not sandboxed.
See the root README for authoritative installation and client examples.

中文說明：MCP 伺服器可在未安裝 SPSS 時啟動與列出工具。統計執行需另行安裝及授權
IBM SPSS 與 Python Integration，並設定 `SPSS_PYTHON`。工作程序保留資料集，但不連接
既有 GUI 工作階段。工具錯誤會明確回報；逾時不會自動重試。UTF-8 保留中文路徑、
變數及標籤；AI 客戶端可能將回傳結果傳送給模型供應商。
