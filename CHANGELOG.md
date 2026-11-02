# Changelog

## 1.1.0 — Unreleased

- Local stdio tool discovery works independently of SPSS installation.
- Isolate SPSS in a persistent worker with bounded waits, cleanup and no automatic
  execution retries; remove in-process native imports and COM fallback.
- Validate tool schemas, variables/methods, quoted labels and absolute paths;
  optional environment-based file root and raw syntax disable switch.
- Surface failures through MCP isError, preserve UTF-8 and serialize dataset calls.
- Require explicit binary/ordinal logistic choice. Delimited imports now require
  explicit schema via raw syntax; reject overwrites in structured save/export.
- Add pytest engine mocks, real stdio SDK tests, portable packaging/dev extras,
  Ubuntu/Windows Python 3.10–3.12 CI, client setup and contribution guidance.
- Preserve MIT license with chengamki-tech contributors copyright.

## 1.0.0

- Initial SPSS skills, statistical reference guides and MCP tool catalog.
