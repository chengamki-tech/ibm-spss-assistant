# Contributing

Open an issue describing a bug, expected behavior and sanitized reproduction.
Do not include private datasets, license files, credentials or identifiable output.
Use small synthetic datasets when a licensed SPSS reproduction is necessary.

Create a branch, then from `mcp-server/`:

```sh
python -m venv .venv
# Activate the environment for your platform.
python -m pip install -e '.[dev]'
python -m pytest -q
```

Use Python 3.10-compatible source for the server. The standalone worker must remain
compatible with SPSS-bundled Python 3.8+ and must not import the MCP SDK. Keep stdout
reserved for transport. Add regression tests for behavioral changes, particularly
validation, failures, lifecycle and MCP client interoperability. Mock SPSS so the
standard tests never require IBM software. CI runs Ubuntu/Windows on 3.10–3.12.
A real-SPSS manual check is helpful when available; report SPSS edition, OS, Python
Integration version, syntax, and observed output, and distinguish it from mock tests.

Document changed tools/configuration and add a changelog entry. Prefer focused
commits. English server diagnostics are the current convention; preserve UTF-8
labels and paths. Translations and corrections to statistical guidance are welcome.
Code contributions are distributed under the repository's MIT license. SPSS is not
redistributed. Report security issues privately through GitHub private vulnerability
reporting if enabled; otherwise ask the maintainers for a private contact without
posting exploit details or sensitive data in a public issue.
