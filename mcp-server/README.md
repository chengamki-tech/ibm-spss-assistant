# spss-mcp-server

Local stdio MCP tools for licensed IBM SPSS Statistics. Python 3.10+ runs the MCP
server; a separately configured SPSS-compatible interpreter runs the persistent
worker. No cloud backend or API key is required. Tool discovery works without SPSS.

From this directory:

```sh
python -m venv .venv
# macOS/Linux; on Windows use .venv\Scripts\python.exe
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest -q
.venv/bin/spss-mcp
```

Set `SPSS_PYTHON` to an absolute Python executable that can import IBM's `spss`
module. `SPSS_HOME` provides limited discovery when that is unset. Optional
`SPSS_TIMEOUT` (default 120 seconds), `SPSS_DATA_ROOT` and `SPSS_ALLOW_SYNTAX=0`
control execution limits and structured file access. Save/export reject existing
paths. Raw syntax is trusted local code and bypasses structured path restrictions.

See the [repository README](https://github.com/chengamki-tech/ibm-spss-assistant#readme)
for Claude Desktop, Cursor and Codex configuration, usage, security boundaries
and internationalization notes. The MCP client may forward results to a model
provider. IBM SPSS is proprietary, separately licensed and not bundled.
