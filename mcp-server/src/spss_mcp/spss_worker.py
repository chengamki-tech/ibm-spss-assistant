"""
SPSS Persistent Worker

Runs inside IBM SPSS's bundled Python (3.8) as a long-lived subprocess.
Reads JSON commands from stdin, executes SPSS syntax, returns JSON results
via stdout.  Keeps the SPSS processor alive across calls so that data loaded
in one command is available to the next.

Protocol (newline-delimited JSON):
  Input:  {"cmd": "<execute|get_variables|get_case_count|quit>", ...}
  Output: {"ok": true, ...} | {"ok": false, "error": "..."}

This script is NOT meant to be imported — it is launched as a subprocess by
the SPSSEngine CLI backend.

IMPORTANT: SPSS's Submit() writes directly to C-level stdout (fd 1).
We redirect fd 1 to /dev/null before importing spss so that SPSS output
doesn't pollute our JSON channel.  JSON responses go through a saved
copy of the original stdout.
"""

import sys
import os
import re
import json
import tempfile

# ── Step 1: Redirect C-level stdout (fd 1) BEFORE importing spss ──────
# SPSS writes output directly to fd 1.  We save the real stdout as fd 3
# and point fd 1 at the null device so SPSS output is silently discarded.
_orig_stdout_fd = os.dup(1)                    # save real stdout
_devnull_fd = os.open(os.devnull, os.O_WRONLY) # /dev/null
os.dup2(_devnull_fd, 1)                        # fd 1 → /dev/null
os.close(_devnull_fd)

# Create a Python file object for the saved fd (our JSON channel)
_out = os.fdopen(_orig_stdout_fd, "w", encoding="utf-8", errors="replace")

# Force UTF-8 for stdin (Python 3.8 on Windows defaults to GBK)
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Step 2: Import spss AFTER redirecting fd 1 ───────────────────────
import spss  # SPSS Integration Plug-in (only available in SPSS's Python)


def _write_response(obj):
    """Write a JSON response to the saved stdout fd, flush immediately."""
    line = json.dumps(obj, ensure_ascii=False)
    _out.write(line + "\n")
    _out.flush()


def _capture_execute(syntax):
    """Execute syntax with OMS output capture, return cleaned text."""
    out_file = tempfile.mktemp(suffix=".html")
    out_path = out_file.replace("\\", "/")
    try:
        spss.Submit(
            "OMS /SELECT ALL /DESTINATION FORMAT=HTML OUTFILE='{}'.".format(out_path)
        )
        spss.Submit(syntax)
        spss.Submit("OMSEND.")
    except Exception as exc:
        # Try to close OMS even on error
        try:
            spss.Submit("OMSEND.")
        except Exception:
            pass
        raise RuntimeError(str(exc))

    return _read_and_clean(out_file)


def _read_and_clean(path):
    """Read OMS HTML output and convert to plain text."""
    if not os.path.isfile(path):
        return "[no output file produced]"
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
    except Exception as exc:
        return "[could not read output: {}]".format(exc)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass

    return _html_to_text(html)


def _html_to_text(html):
    """Convert SPSS OMS HTML to readable plain text."""
    if not html.strip():
        return ""

    # Try BeautifulSoup first
    try:
        from bs4 import BeautifulSoup
        import html as html_mod
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["style", "script"]):
            tag.decompose()
        parts = []
        for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "table", "div"]):
            if el.name == "table":
                rows = []
                for tr in el.find_all("tr"):
                    cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                    if cells:
                        rows.append("\t".join(cells))
                if rows:
                    parts.append("\n".join(rows))
            else:
                txt = el.get_text(strip=True)
                if txt:
                    parts.append(txt)
        text = "\n\n".join(parts)
        # Decode any remaining HTML entities
        text = html_mod.unescape(text)
        # Strip temp file names that leak from <title> tags
        text = re.sub(r"^tmp\w+\.html\s*", "", text)
        return text.strip()
    except ImportError:
        pass

    # Fallback: naive regex
    import html as html_mod
    text = re.sub(r"(?is)<style.*?</style>", "", html)
    text = re.sub(r"(?is)<script.*?</script>", "", text)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)<tr[^>]*>", "\n", text)
    text = re.sub(r"(?i)<t[hd][^>]*>", "\t", text)
    text = re.sub(r"(?s)<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = html_mod.unescape(text)
    text = re.sub(r"^tmp\w+\.html\s*", "", text)
    return text.strip()


def _get_variables():
    """Return list of variable info dicts."""
    n = spss.GetVariableCount()
    result = []
    for i in range(n):
        result.append({
            "index": i,
            "name": spss.GetVariableName(i),
            "label": spss.GetVariableLabel(i),
            "type_width": spss.GetVariableType(i),
            "measurement": spss.GetVariableMeasurementLevel(i),
            "format": spss.GetVariableFormat(i),
        })
    return result


def _get_case_count():
    """Return number of cases in active dataset."""
    return spss.GetCaseCount()


def main():
    # Initialise the SPSS processor
    try:
        spss.Submit("")
    except Exception as exc:
        _write_response({"ok": False, "error": "Failed to initialise SPSS: {}".format(exc)})
        sys.exit(1)

    # Signal that we're ready
    _write_response({"ok": True, "status": "ready"})

    # Command loop
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except json.JSONDecodeError as exc:
            _write_response({"ok": False, "error": "Invalid JSON: {}".format(exc)})
            continue

        cmd = req.get("cmd", "")

        try:
            if cmd == "execute":
                syntax = req.get("syntax", "")
                capture = req.get("capture", True)
                if not syntax:
                    _write_response({"ok": False, "error": "No syntax provided"})
                    continue
                if capture:
                    output = _capture_execute(syntax)
                    _write_response({"ok": True, "output": output})
                else:
                    spss.Submit(syntax)
                    _write_response({"ok": True, "output": "[executed]"})

            elif cmd == "get_variables":
                vars_info = _get_variables()
                _write_response({"ok": True, "variables": vars_info})

            elif cmd == "get_case_count":
                count = _get_case_count()
                _write_response({"ok": True, "count": count})

            elif cmd == "quit":
                _write_response({"ok": True, "status": "bye"})
                break

            else:
                _write_response({"ok": False, "error": "Unknown command: {}".format(cmd)})

        except Exception as exc:
            _write_response({"ok": False, "error": str(exc)})


if __name__ == "__main__":
    main()
