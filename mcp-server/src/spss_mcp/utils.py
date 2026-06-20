"""Utility helpers for SPSS MCP Server."""

from __future__ import annotations


def clean_output(text: str) -> str:
    """Clean up SPSS output text for better readability."""
    if not text:
        return ""

    # Remove excessive blank lines
    lines = text.split("\n")
    cleaned = []
    blank_count = 0
    for line in lines:
        if not line.strip():
            blank_count += 1
            if blank_count <= 2:
                cleaned.append("")
        else:
            blank_count = 0
            cleaned.append(line)

    return "\n".join(cleaned).strip()


def format_table(rows: list[list[str]], headers: list[str] | None = None) -> str:
    """Format a list of rows as a simple aligned text table."""
    if not rows:
        return ""

    all_rows = ([headers] if headers else []) + rows
    if not all_rows:
        return ""

    # Calculate column widths
    n_cols = max(len(r) for r in all_rows)
    widths = [0] * n_cols
    for row in all_rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    # Format
    lines = []
    for i, row in enumerate(all_rows):
        cells = [str(c).ljust(widths[j]) for j, c in enumerate(row)]
        lines.append("  ".join(cells))
        if i == 0 and headers:
            lines.append("  ".join("-" * w for w in widths))

    return "\n".join(lines)


def parse_variables(var_string: str) -> list[str]:
    """Parse a comma-separated variable string into a clean list."""
    return [v.strip() for v in var_string.split(",") if v.strip()]
