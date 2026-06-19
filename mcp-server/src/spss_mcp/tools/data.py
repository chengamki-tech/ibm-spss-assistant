"""Data management tools for SPSS MCP Server."""

from __future__ import annotations

import os


def open_data(engine, file_path: str, encoding: str = "auto") -> str:
    """Open a data file (.sav, .csv, .xlsx, .xls, .dat).

    Parameters
    ----------
    file_path : str  Absolute path to the data file.
    encoding  : str  File encoding ('auto', 'UTF-8', 'GBK', etc.)

    Returns
    -------
    str  Confirmation message with case count and variable count.
    """
    file_path = os.path.abspath(file_path).replace("\\", "/")
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".sav":
        syntax = f"GET FILE='{file_path}'."
    elif ext in (".csv", ".txt", ".dat"):
        if encoding == "auto":
            encoding = "UTF-8"
        syntax = (
            f"GET DATA /TYPE=TXT\n"
            f"  /FILE='{file_path}'\n"
            f"  /DELCASE=LINE\n"
            f"  /DELIMITERS=','\n"
            f"  /QUALIFIER='\"'\n"
            f"  /ARRANGEMENT=DELIMITED\n"
            f"  /FIRSTCASE=2\n"
            f"  /IMPORTCASE=ALL\n"
            f"  /VARIABLES=\n"
            f"  /MAP.\n"
            f"SET UNICODE=ON."
        )
    elif ext in (".xlsx", ".xls"):
        syntax = (
            f"GET DATA /TYPE=XLSX\n"
            f"  /FILE='{file_path}'\n"
            f"  /SHEET=name 'Sheet1'\n"
            f"  /CELLRANGE=FULL\n"
            f"  /READNAMES=ON\n"
            f"  /IMPORTCASE=ALL."
        )
    else:
        return f"Unsupported file format: {ext}. Supported: .sav, .csv, .xlsx, .xls, .txt, .dat"

    output = engine.execute(syntax)
    n_vars = engine.get_variable_info()
    n_cases = engine.get_case_count()

    return (
        f"Data loaded successfully.\n"
        f"File: {file_path}\n"
        f"Cases: {n_cases}\n"
        f"Variables: {len(n_vars)}\n\n"
        f"Variable list:\n" + _format_vars(n_vars)
    )


def get_variable_info(engine) -> str:
    """Return formatted variable information for the active dataset."""
    vars_info = engine.get_variable_info()
    if not vars_info:
        return "No dataset loaded."

    if "raw" in vars_info[0]:
        return vars_info[0]["raw"]

    return f"Variables ({len(vars_info)}):\n" + _format_vars(vars_info)


def get_data_summary(engine, variables: str | None = None) -> str:
    """Run descriptive statistics on specified (or all) variables.

    Parameters
    ----------
    variables : str | None  Comma-separated variable names, or None for all numeric.
    """
    var_part = variables if variables else "ALL"
    syntax = (
        f"DESCRIPTIVES VARIABLES={var_part}\n"
        f"  /STATISTICS=MEAN STDDEV MIN MAX SKEWNESS KURTOSIS."
    )
    return engine.execute(syntax)


def save_data(engine, file_path: str) -> str:
    """Save the active dataset to a .sav file."""
    file_path = os.path.abspath(file_path).replace("\\", "/")
    engine.execute(f"SAVE OUTFILE='{file_path}'.")
    return f"Data saved to: {file_path}"


def _format_vars(vars_info: list[dict]) -> str:
    lines = []
    measurement_map = {0: "Scale", 1: "Ordinal", 2: "Nominal", 3: "Unknown"}
    for v in vars_info:
        m = measurement_map.get(v.get("measurement", 3), "Unknown")
        label = v.get("label", "")
        type_w = v.get("type_width", 0)
        t = "String" if type_w > 0 else "Numeric"
        label_part = f'  "{label}"' if label else ""
        lines.append(f"  {v['name']}{label_part}  ({t}, {m})")
    return "\n".join(lines)
