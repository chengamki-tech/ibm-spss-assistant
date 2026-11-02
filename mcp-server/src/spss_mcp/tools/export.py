"""Output export tools."""

from __future__ import annotations

from ..validation import data_path
from ..spss_engine import SPSSError


def export_output(engine, format: str, file_path: str) -> str:
    """Export the current SPSS output to a file.

    Parameters
    ----------
    format    : str  'html', 'docx', 'pdf', 'png', 'emf'
    file_path : str  Absolute destination path.
    """
    file_path = data_path(file_path, output=True)
    fmt = format.lower().strip()

    if fmt == "html":
        syntax = (
            f"OUTPUT EXPORT\n"
            f"  /CONTENTS EXPORT=VISIBLE\n"
            f"  /HTML DOCUMENTFILE='{file_path}'\n"
            f"  IMAGES=EMBEDDED."
        )
    elif fmt == "docx":
        syntax = (
            f"OUTPUT EXPORT\n"
            f"  /CONTENTS EXPORT=VISIBLE\n"
            f"  /DOCX DOCUMENTFILE='{file_path}'."
        )
    elif fmt == "pdf":
        syntax = (
            f"OUTPUT EXPORT\n"
            f"  /CONTENTS EXPORT=VISIBLE\n"
            f"  /PDF DOCUMENTFILE='{file_path}'."
        )
    elif fmt == "png":
        syntax = (
            f"OUTPUT EXPORT\n"
            f"  /CONTENTS EXPORT=ALL\n"
            f"  /PNG IMAGFILE='{file_path}' WIDTH=1200 HEIGHT=800."
        )
    elif fmt == "emf":
        syntax = (
            f"OUTPUT EXPORT\n"
            f"  /CONTENTS EXPORT=ALL\n"
            f"  /EMF IMAGFILE='{file_path}'."
        )
    else:
        raise SPSSError("Unsupported format. Use html, docx, pdf, png, emf.")

    engine.execute(syntax, capture=False)
    return f"Output exported to: {file_path} ({fmt})"


def export_chart(engine, format: str, file_path: str) -> str:
    """Export only charts from the current output."""
    file_path = data_path(file_path, output=True)
    fmt = format.lower().strip()

    if fmt == "png":
        syntax = (
            f"OUTPUT EXPORT\n"
            f"  /CONTENTS EXPORT=ALL\n"
            f"  /PNG IMAGFILE='{file_path}' WIDTH=1200 HEIGHT=800."
        )
    elif fmt == "emf":
        syntax = (
            f"OUTPUT EXPORT\n"
            f"  /CONTENTS EXPORT=ALL\n"
            f"  /EMF IMAGFILE='{file_path}'."
        )
    else:
        raise SPSSError("Chart export supports png and emf only.")

    engine.execute(syntax, capture=False)
    return f"Chart exported to: {file_path}"


def clear_output(engine) -> str:
    """Clear all output in the SPSS output viewer."""
    engine.execute("OUTPUT CLOSE ALL.", capture=False)
    return "Output viewer cleared."
