"""Validated local dataset operations."""
from ..validation import data_path, literal, parameters
from ..spss_engine import SPSSError
from pathlib import Path
import codecs


def open_data(engine, file_path, encoding="auto"):
    path = data_path(file_path)
    ext = Path(file_path).suffix.lower()
    if ext == ".sav":
        syntax = f"GET FILE='{path}'."
    elif ext in {".csv", ".txt", ".dat"}:
        # Delimited imports require a schema to avoid guessing types/widths.
        raise SPSSError("Delimited import requires an explicit SPSS /VARIABLES schema. Use spss_execute_syntax with GET DATA, /ENCODING and /VARIABLES, or convert to .sav in SPSS first.")
    elif ext in {".xls", ".xlsx"}:
        kind = "XLS" if ext == ".xls" else "XLSX"
        syntax = f"GET DATA /TYPE={kind} /FILE='{path}' /SHEET=INDEX 1 /CELLRANGE=FULL /READNAMES=ON."
    else:
        raise SPSSError("Unsupported data format. Use .sav, .xls or .xlsx.")
    if encoding != "auto":
        try:
            codecs.lookup(encoding)
        except (LookupError, TypeError) as exc:
            raise SPSSError("Unknown encoding.") from exc
        raise SPSSError("encoding is only applicable to explicit delimited GET DATA syntax.")
    engine.execute(syntax)
    variables = engine.get_variable_info()
    count = engine.get_case_count()
    return f"Data loaded: {file_path}\nCases: {count}\n" + _format_vars(variables)


def get_variable_info(engine):
    variables = engine.get_variable_info()
    return _format_vars(variables) if variables else "No variables in the active dataset."


def get_data_summary(engine, variables=None):
    variables = parameters("descriptives", {"variables": variables or "ALL"})["variables"]
    return engine.execute(f"DESCRIPTIVES VARIABLES={variables} /STATISTICS=MEAN STDDEV MIN MAX SKEWNESS KURTOSIS.")


def save_data(engine, file_path):
    path = data_path(file_path, output=True)
    if Path(file_path).suffix.lower() != ".sav":
        raise SPSSError("Saved datasets must use .sav extension.")
    engine.execute(f"SAVE OUTFILE='{path}'.", capture=False)
    return f"Data saved to: {file_path}"


def _format_vars(variables):
    levels = {0: "Scale", 1: "Ordinal", 2: "Nominal", 3: "Unknown"}
    lines = []
    for v in variables:
        level = v.get("measurement", "Unknown")
        level = levels.get(level, level)
        lines.append(f"{v['name']} ({'String' if v.get('type_width', 0) else 'Numeric'}, {level}) {v.get('label', '')}")
    return "Variables:\n" + "\n".join(lines)
