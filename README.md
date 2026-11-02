# IBM SPSS Assistant

A local **stdio MCP server** for IBM SPSS Statistics, plus six optional
[Agent Skills](skills/) for test selection, data cleaning, syntax, interpretation
and reporting. No API key, cloud backend or network listener is required by the
server. It starts and lists all 27 tools even when SPSS is absent; execution tools
return actionable MCP errors until a licensed local runtime is connected.

## Install

Use Python 3.10+ for the MCP server. IBM SPSS Statistics and its Python Integration
Plug-in are required only for statistical execution and are licensed separately.
The SPSS worker uses SPSS's own compatible Python interpreter, which can differ
from the server's Python version. This project does not bundle SPSS.

From the repository root on macOS/Linux:

```sh
python3 -m venv mcp-server/.venv
cd mcp-server
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest -q
.venv/bin/spss-mcp
```

On Windows PowerShell:

```powershell
py -3 -m venv mcp-server/.venv
cd mcp-server
.venv\Scripts\python.exe -m pip install -e '.[dev]'
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\spss-mcp.exe
```

The final command waits for MCP messages on stdin. A quiet terminal is expected.
`python -m spss_mcp` is an equivalent entry point. For runtime-only installation,
use `pip install -e .` without `[dev]`.

## Configure a client

Replace every example path with an **absolute path on your machine**. Client
processes may have a different PATH and working directory from your terminal.
`SPSS_PYTHON` must point to the executable that can import IBM's `spss` module,
not the server virtual environment's Python. See your SPSS release's Python
Integration documentation for its supported interpreter and runtime setup.
The repository `.mcp.json` is a PATH-based template; use the absolute executable
path below if the client cannot find `spss-mcp`. Restart the client after configuration changes. Set client tool-call timeouts
longer than `SPSS_TIMEOUT` when running lengthy procedures.

### Claude Desktop

Edit `claude_desktop_config.json` through Desktop's developer settings
(macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`;
Windows: `%APPDATA%\Claude\claude_desktop_config.json`). Merge this entry with
any existing `mcpServers`:

```json
{
  "mcpServers": {
    "spss": {
      "command": "/absolute/path/ibm-spss-assistant/mcp-server/.venv/bin/spss-mcp",
      "env": {
        "SPSS_PYTHON": "/absolute/path/to/SPSS/Python3/bin/python3"
      }
    }
  }
}
```

On Windows, use the command
`C:\\absolute\\path\\ibm-spss-assistant\\mcp-server\\.venv\\Scripts\\spss-mcp.exe`
and an SPSS Python executable such as
`C:\\absolute\\path\\SPSS\\Python3\\python.exe` (JSON backslashes must be escaped).
See [Claude Desktop local MCP setup](https://modelcontextprotocol.io/docs/develop/connect-local-servers).

### Cursor

Place the same JSON object in project `.cursor/mcp.json` or user
`~/.cursor/mcp.json`. Enable `spss` in Cursor's MCP settings and review tool
permissions. See [Cursor MCP documentation](https://cursor.com/docs/context/mcp).

### Codex

Add this to `~/.codex/config.toml`:

```toml
[mcp_servers.spss]
command = "/absolute/path/ibm-spss-assistant/mcp-server/.venv/bin/spss-mcp"
tool_timeout_sec = 180

[mcp_servers.spss.env]
SPSS_PYTHON = "/absolute/path/to/SPSS/Python3/bin/python3"
```

For Windows, use a TOML literal string such as
`command = 'C:\absolute\path\ibm-spss-assistant\mcp-server\.venv\Scripts\spss-mcp.exe'`
and set `SPSS_PYTHON` similarly. Check discovery with `codex mcp list`.
See [official OpenAI MCP configuration](https://developers.openai.com/codex/mcp).

## Configuration

| Environment variable | Behavior |
| --- | --- |
| `SPSS_PYTHON` | Absolute SPSS-compatible Python executable; takes precedence over home-directory discovery. |
| `SPSS_HOME` | Optional installation directory; checks `Python3`, `Python`, `bin` and the directory itself for `python.exe`, `python3` or `python`. Use `SPSS_PYTHON` for other layouts. `spss_connect(spss_home=...)` overrides this directory. |
| `SPSS_TIMEOUT` | Worker startup and command timeout in seconds; default 120, greater than 0 and at most 3600. |
| `SPSS_DATA_ROOT` | Optional existing absolute directory restricting structured file tools; resolved paths, including symlinks, must stay inside it. |
| `SPSS_ALLOW_SYNTAX` | Default `1`; set `0` to disable unrestricted `spss_execute_syntax`. |

The server executes only local operations, but the **MCP client can send returned
results to its model provider**. Use a client and model appropriate for your data.
Raw SPSS syntax can read/write files and invoke local code under your account;
only enable it for trusted users and clients. `SPSS_DATA_ROOT` constrains the
structured file tools, not arbitrary syntax or code. It is not a sandbox.
No secrets belong in the repository. There are no required server credentials.

Paths must be absolute. Structured save/export tools reject existing destinations;
choose a new path. This check is not protection against another local process
racing file creation. SPSS itself may produce sidecar files when exporting images.
Calls are serialized against one persistent worker and dataset. The worker does
not attach to an existing GUI session. On timeout/error it is stopped, so reconnect
and reopen data; a timed-out command may already have changed files. Commands are
never retried automatically. Save important work explicitly.

## Usage

Ask your client to call these tools (arguments shown as JSON):

```text
spss_status {}
spss_connect {}
spss_open_data {"file_path": "/absolute/path/study.sav"}
spss_get_variables {}
spss_descriptives {"variables": "age,score"}
spss_ttest {"dv": "score", "group": "condition", "groups": "1 2"}
spss_logistic {"dv": "outcome", "ivs": "age,score", "dv_type": "binary"}
spss_run_analysis {"analysis_type": "correlation", "params": {"variables": "age,score", "method": "SPEARMAN"}}
spss_save_data {"file_path": "/absolute/path/study-clean.sav"}
spss_disconnect {}
```

Tools cover connection/status, open/save and metadata, descriptives, frequencies,
explore/normality/Levene, independent/paired t-tests, ANOVA, correlations,
regression, crosstabs, reliability, factors, binary/ordinal logistic regression,
means comparison, structured advanced analyses, raw syntax, output/chart export
and output clearing. Methods are validated; variables accept commas or spaces,
Unicode names and `ALL` where applicable. Use numeric group values for t-tests.
Logistic `dv_type` must be chosen explicitly; automatic inference was unreliable.
Regression returns basic model output; additional diagnostics require raw syntax.
Advanced procedures depend on your SPSS edition and licensed modules.

`.sav`, `.xls` and `.xlsx` can be opened directly. CSV/TXT/DAT imports require an
explicit SPSS `GET DATA` schema (variable names/types/widths and encoding), so use
raw syntax or first convert the file to `.sav` in SPSS. For example:

```text
spss_execute_syntax {"syntax": "GET DATA /TYPE=TXT /FILE='/absolute/path/study.csv' /ENCODING='UTF8' /ARRANGEMENT=DELIMITED /DELCASE=LINE /DELIMITERS=',' /FIRSTCASE=2 /VARIABLES=age F8.0 score F8.2.\nDESCRIPTIVES VARIABLES=age score."}
```

Tool failures carry MCP `isError=true`. If connection fails, verify that
`SPSS_PYTHON` exists, can import `spss`, and has a working SPSS license. Runtime
stderr is inherited by the server for client logs; stdout is reserved for MCP.

## Skills and internationalization

Optional guidance remains in [skills/](skills/) and statistical references in
[references/](references/). Install those according to your agent's skills support;
they are not needed to start the MCP server. Ask your agent for explanations in
English, 简体中文, 繁體中文, 日本語, 한국어, Español, Français, Deutsch, Português,
Русский, العربية, ไทย, Tiếng Việt, हिन्दी, Türkçe, Italiano, Bahasa Indonesia,
Bahasa Melayu, Polski or Nederlands. These are language guidance notes, not a
claim of localized server messages: tool names/errors use English, while UTF-8
paths, variable names, labels and SPSS output are preserved. SPSS output language
is controlled by your SPSS installation. Translation contributions are welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md), and the baseline
[AUDIT.md](AUDIT.md). MIT licensed; copyright chengamki-tech contributors. IBM SPSS
Statistics is an IBM product; this community project is not affiliated with IBM.
