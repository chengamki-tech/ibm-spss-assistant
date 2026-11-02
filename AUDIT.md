# Open-source readiness audit

Baseline: branch `oss-mcp`, before remediation. References below refer to that baseline;
this document intentionally preserves findings after fixes. Scope: tracked source,
configuration, packaging, skills, references and documentation. No hard-coded API
keys or cloud service dependency were found. These are the concrete weaknesses
identified by source review; real licensed SPSS execution was not available.

## Architecture
- `mcp-server/src/spss_mcp/server.py:41,406` uses process-global engine state; synchronous dispatch blocks the async MCP loop and server shutdown does not disconnect.
- `mcp-server/src/spss_mcp/spss_engine.py:75-130` mixes in-process native imports, COM and worker fallbacks. Native stdout can corrupt MCP stdio; COM can attach to unrelated GUI data, and undeclared pywin32 is needed.
- `mcp-server/src/spss_mcp/spss_engine.py:164-176` retries failed captured commands, potentially applying mutations twice.
- `mcp-server/src/spss_mcp/tools/quick.py:80-96` regression promises diagnostics absent from generated syntax; logistic auto detection is heuristic rather than reliable metadata.

## Security
- **Command injection:** `mcp-server/src/spss_mcp/tools/quick.py:9-121` and `tools/analysis.py:90-430` interpolate variables, methods, group values and labels into executable syntax without validation.
- **Paths/traversal:** `mcp-server/src/spss_mcp/tools/data.py:34-59,135-139` and `tools/export.py:18-86` interpolate unescaped paths, accept relative paths and unrestricted writes; quote/newline injection and symlink escapes are possible. No configurable data root exists.
- **Temporary files:** `mcp-server/src/spss_mcp/spss_engine.py:343,376` and `spss_worker.py:67` use race-prone mktemp; capture exceptions can leave sensitive files behind.
- **Hard-coded paths:** `mcp-server/src/spss_mcp/spss_engine.py:491-520` guesses C:/D: installs, scans versions and mutates import search paths (`:580`); explicit configuration has lower precedence than registry discovery (`:440-487`).
- **Trust boundary:** `mcp-server/src/spss_mcp/server.py:323-337` exposes unrestricted syntax (including local code/file operations) without a documented trust boundary or disable switch. No hard-coded secrets found.

## Error handling
- `mcp-server/src/spss_mcp/spss_engine.py:272,313` blocking readline has no timeout; stderr PIPE is never drained, risking deadlock. Killed workers are not consistently reaped and streams closed.
- `mcp-server/src/spss_mcp/spss_engine.py:215-246` silently converts metadata failures to empty lists/unknown counts.
- `mcp-server/src/spss_mcp/server.py:420-650` mostly catches only SPSSError, does not validate direct dispatch arguments, and returns error text without MCP isError.
- `mcp-server/src/spss_mcp/tools/data.py:28-32,65-105`, `tools/analysis.py:20-49,82-88` swallow exceptions as ordinary successful text; CSV encoding is ignored (`data.py:40-56`), XLS is sent as XLSX (`:58`).
- `mcp-server/src/spss_mcp/spss_worker.py:91-107` missing/unreadable output is silently reported as success; HTML fallback conversion differs between worker and engine.

## Tests
- `mcp-server/pyproject.toml:9-21`: no dev dependencies, pytest configuration or tests directory. No engine mocks, injection regressions, lifecycle tests or real MCP client stdio discovery test.

## Docs
- `.claude-plugin/plugin.json:3` advertises 26 tools despite the 27-entry catalog and implies SPSS is required for discovery.
- `README.md:38-61` focuses on skills without complete local MCP install/client configuration; lacks Claude Desktop, Cursor and Codex examples together.
- `mcp-server/README.md:272-277` claims CLI/COM fallbacks and that data never leaves the machine, overlooking client forwarding of tool results.
- `mcp-server/docs/spss-detection-and-binding.md:203-235` documents a CLI fallback different from the actual persistent worker; duplicate architecture narrative can drift.
- Root lacks CONTRIBUTING.md and CHANGELOG.md; configuration, overwrite behavior and SPSS licensing/runtime compatibility need documentation.

## Packaging
- `mcp-server/pyproject.toml:7,10` advertises Python 3.9 although the MCP SDK requires newer Python, and has no SDK major-version ceiling.
- `mcp-server/pyproject.toml:6,8,16-21` lacks distributed license file, project URLs and dev extras. `.gitignore:1-6` fails to ignore venvs, pytest cache and local statistical data.

## License
- `LICENSE:3` copyright holder is “SPSS Assistant”; change to “chengamki-tech contributors”. SPSS itself is proprietary and not included.

## CI
- No `.github/workflows/ci.yml` exists: no automated Ubuntu/Windows Python 3.10–3.12 installation or tests.

## i18n
- `README.md:88-475` contains useful language notes but duplicated install snippets drift; claims of 20+ languages describe agent behavior, not localized server messages.
- `mcp-server/src/spss_mcp/tools/data.py:144-146` assumes numeric measurement codes, losing string levels supplied by SPSS. UTF-8 and non-ASCII paths/labels have no regression coverage.
