"""
IBM SPSS Statistics Engine

Connects to the local IBM SPSS installation and executes syntax.
Supports three backends (tried in order):
  1. spss Python module (SPSS Integration Plug-in)
  2. Command-line stats executable
  3. COM automation (Windows only)
"""

import os
import sys
import re
import glob
import json
import tempfile
import platform
import subprocess
from pathlib import Path


class SPSSError(Exception):
    """Raised when SPSS execution fails."""


class SPSSEngine:
    """Manages connection to a local IBM SPSS Statistics installation."""

    def __init__(self):
        self._backend = None          # 'spss_module' | 'cli' | 'com'
        self._spss_home = None        # SPSS installation directory
        self._spss_exe = None         # Path to stats executable
        self._spss_version = None     # e.g. '30'
        self._module = None           # The imported spss module (if backend=spss_module)
        self._com_app = None          # COM Application object (if backend=com)
        self._connected = False

    # ── public ────────────────────────────────────────────────────────────
    def connect(self, spss_home: str | None = None) -> dict:
        """Connect to IBM SPSS Statistics.

        Parameters
        ----------
        spss_home : str | None
            Explicit SPSS installation directory.  When *None* the engine
            auto-detects the installation.

        Returns
        -------
        dict  with keys: status, backend, spss_home, version
        """
        if self._connected:
            return self._status_dict("already connected")

        if spss_home:
            self._spss_home = spss_home
        else:
            self._spss_home, self._spss_exe, self._spss_version = _detect_spss()

        if not self._spss_home:
            return {
                "status": "not_found",
                "message": (
                    "IBM SPSS Statistics not found on this computer.\n"
                    "Please install SPSS or pass the installation path explicitly."
                ),
            }

        # Ensure the SPSS Python package is importable
        _add_spss_to_sys_path(self._spss_home)

        # ── try backend 1: spss Python module ──
        try:
            if "spss" not in sys.modules:
                __import__("spss")
            mod = sys.modules["spss"]
            mod.Submit("")                       # initialise processor
            self._module = mod
            self._backend = "spss_module"
            self._connected = True
            return self._status_dict("connected")
        except Exception:
            self._module = None

        # ── try backend 2: command-line executable ──
        exe = self._spss_exe or _find_exe(self._spss_home)
        if exe and os.path.isfile(exe):
            self._spss_exe = exe
            self._backend = "cli"
            self._connected = True
            return self._status_dict("connected")

        # ── try backend 3: COM (Windows only) ──
        if platform.system() == "Windows":
            try:
                import win32com.client  # type: ignore
                self._com_app = win32com.client.Dispatch("SPSS.Application")
                self._backend = "com"
                self._connected = True
                return self._status_dict("connected")
            except Exception:
                self._com_app = None

        return {
            "status": "connection_failed",
            "message": (
                "SPSS installation found but could not connect.\n"
                "Make sure the SPSS Python Integration Plug-in is installed\n"
                "(IBM SPSS Statistics → Utilities → Install Python Plug-in)."
            ),
            "spss_home": self._spss_home,
        }

    def disconnect(self) -> dict:
        self._connected = False
        self._backend = None
        self._module = None
        self._com_app = None
        return {"status": "disconnected"}

    def status(self) -> dict:
        return self._status_dict("connected" if self._connected else "disconnected")

    def execute(self, syntax: str, *, capture: bool = True) -> str:
        """Execute SPSS syntax and return text output.

        Parameters
        ----------
        syntax : str   SPSS syntax (one or more commands, each ending with ``.``)
        capture : bool  Whether to capture and return output (default True).

        Returns
        -------
        str  Cleaned output text.

        Raises
        ------
        SPSSError  on SPSS execution failure.
        """
        if not self._connected:
            raise SPSSError("Not connected to SPSS — call connect() first.")

        if self._backend == "spss_module":
            return self._exec_module(syntax, capture)
        elif self._backend == "cli":
            return self._exec_cli(syntax, capture)
        elif self._backend == "com":
            return self._exec_com(syntax, capture)
        else:
            raise SPSSError("No backend available.")

    def get_variable_info(self) -> list[dict]:
        """Return a list of dicts describing every variable in the active dataset."""
        if not self._connected:
            raise SPSSError("Not connected to SPSS.")

        if self._backend == "spss_module":
            mod = self._module
            n = mod.GetVariableCount()
            return [
                {
                    "index": i,
                    "name": mod.GetVariableName(i),
                    "label": mod.GetVariableLabel(i),
                    "type_width": mod.GetVariableType(i),
                    "measurement": mod.GetVariableMeasurementLevel(i),
                    "format": mod.GetVariableFormat(i),
                }
                for i in range(n)
            ]
        # For CLI / COM fall back to DISPLAY DICTIONARY
        out = self.execute("DISPLAY DICTIONARY.")
        return [{"raw": out}]

    def get_case_count(self) -> int:
        if not self._connected:
            raise SPSSError("Not connected to SPSS.")
        if self._backend == "spss_module":
            return self._module.GetCaseCount()
        return -1  # unknown

    def is_connected(self) -> bool:
        return self._connected

    # ── private: backends ─────────────────────────────────────────────────
    def _exec_module(self, syntax: str, capture: bool) -> str:
        mod = self._module
        if not capture:
            mod.Submit(syntax)
            return "[executed — output not captured]"

        out_file = tempfile.mktemp(suffix=".html")
        # Normalise path separators for SPSS syntax
        out_path = out_file.replace("\\", "/")
        try:
            mod.Submit(
                f"OMS /SELECT ALL /DESTINATION FORMAT=HTML OUTFILE='{out_path}'."
            )
            mod.Submit(syntax)
            mod.Submit("OMSEND.")
        except Exception as exc:
            # Try to close OMS even on error
            try:
                mod.Submit("OMSEND.")
            except Exception:
                pass
            raise SPSSError(f"SPSS error: {exc}") from exc

        text = _read_and_clean(out_file)
        return text

    def _exec_cli(self, syntax: str, capture: bool) -> str:
        syn_file = tempfile.mktemp(suffix=".sps")
        out_file = tempfile.mktemp(suffix=".html")

        # Build a syntax file that uses OMS to capture output
        with open(syn_file, "w", encoding="utf-8") as f:
            if capture:
                f.write(
                    f"OMS /SELECT ALL /DESTINATION FORMAT=HTML OUTFILE='{out_file.replace(chr(92), '/')}'.\n"
                )
            f.write(syntax)
            f.write("\n")
            if capture:
                f.write("OMSEND.\n")

        try:
            result = subprocess.run(
                [self._spss_exe, "-p", syn_file],
                capture_output=True,
                text=True,
                timeout=300,
                cwd=os.path.dirname(syn_file),
            )
        except subprocess.TimeoutExpired:
            raise SPSSError("SPSS execution timed out (300 s).")
        except FileNotFoundError:
            raise SPSSError(f"SPSS executable not found: {self._spss_exe}")

        _try_remove(syn_file)

        if result.returncode != 0 and result.stderr.strip():
            raise SPSSError(f"SPSS error: {result.stderr.strip()}")

        if capture:
            text = _read_and_clean(out_file)
            return text
        return "[executed]"

    def _exec_com(self, syntax: str, capture: bool) -> str:
        app = self._com_app
        syn_file = tempfile.mktemp(suffix=".sps")
        with open(syn_file, "w", encoding="utf-8") as f:
            f.write(syntax)
        try:
            app.OpenSyntaxFile(syn_file)
            app.ExecuteSyntax()
        except Exception as exc:
            _try_remove(syn_file)
            raise SPSSError(f"COM error: {exc}") from exc

        _try_remove(syn_file)

        if not capture:
            return "[executed]"

        # Try to grab text from the output document
        try:
            doc = app.OutputDocument
            parts = []
            for i in range(doc.Items.Count):
                item = doc.Items.Item(i)
                try:
                    parts.append(item.Text)
                except Exception:
                    pass
            return "\n\n".join(p for p in parts if p).strip() or "[no output]"
        except Exception:
            return "[output capture not available via COM]"

    # ── helpers ───────────────────────────────────────────────────────────
    def _status_dict(self, status: str) -> dict:
        return {
            "status": status,
            "backend": self._backend,
            "spss_home": self._spss_home,
            "version": self._spss_version,
            "platform": platform.system(),
        }


# ═══════════════════════════════════════════════════════════════════════════
#  Module-level helpers
# ═══════════════════════════════════════════════════════════════════════════

def _detect_spss():
    """Return (home_dir, executable, version) or (None, None, None)."""
    system = platform.system()

    candidates: list[tuple[str, str]] = []  # (home, version)

    if system == "Windows":
        # Try registry first
        try:
            import winreg  # type: ignore
            for v in range(40, 24, -1):
                for root in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
                    for suffix in (f"{v}.0", str(v)):
                        try:
                            key = winreg.OpenKey(root, f"SOFTWARE\\IBM\\SPSS Statistics\\{suffix}")
                            home = winreg.QueryValueEx(key, "InstallDir")[0]
                            winreg.CloseKey(key)
                            candidates.append((home, str(v)))
                        except FileNotFoundError:
                            pass
        except ImportError:
            pass

        # Common paths
        for v in range(40, 24, -1):
            for base in [
                os.environ.get("ProgramFiles", r"C:\Program Files"),
                os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
            ]:
                candidates.append((os.path.join(base, "IBM", "SPSS", "Statistics", str(v)), str(v)))
                candidates.append((os.path.join(base, "IBM", "SPSS", "Statistics", f"{v}.0"), str(v)))

    elif system == "Darwin":
        for v in range(40, 24, -1):
            candidates.append((f"/Applications/IBM/SPSS/Statistics/{v}", str(v)))
            candidates.append((f"/Applications/IBM/SPSS/Statistics/{v}.0", str(v)))

    else:  # Linux
        for v in range(40, 24, -1):
            candidates.append((f"/opt/ibm/SPSS/Statistics/{v}", str(v)))
            candidates.append((f"/opt/ibm/SPSS/Statistics/{v}.0", str(v)))
        # Also check /usr/local
        for v in range(40, 24, -1):
            candidates.append((f"/usr/local/ibm/SPSS/Statistics/{v}", str(v)))

    for home, ver in candidates:
        if os.path.isdir(home):
            exe = _find_exe(home)
            return home, exe, ver

    return None, None, None


def _find_exe(home: str) -> str | None:
    system = platform.system()
    if system == "Windows":
        for name in ("stats.exe", "stats.com", "spss.com"):
            p = os.path.join(home, name)
            if os.path.isfile(p):
                return p
    else:
        for name in ("stats", "spss"):
            for sub in ("", "bin"):
                p = os.path.join(home, sub, name) if sub else os.path.join(home, name)
                if os.path.isfile(p) and os.access(p, os.X_OK):
                    return p
    return None


def _add_spss_to_sys_path(home: str) -> None:
    """Add the SPSS Python packages to sys.path if not already there."""
    patterns = [
        os.path.join(home, "Python3", "Lib", "site-packages"),
        os.path.join(home, "Python", "Lib", "site-packages"),
        os.path.join(home, "Python3", "lib", "site-packages"),
        os.path.join(home, "Python", "lib", "site-packages"),
    ]
    # Also try versioned Python dirs
    for minor in range(8, 15):
        patterns.append(
            os.path.join(home, "Python3", "lib", f"python3.{minor}", "site-packages")
        )
        patterns.append(
            os.path.join(home, "Python", "lib", f"python3.{minor}", "site-packages")
        )

    for p in patterns:
        if os.path.isdir(p) and p not in sys.path:
            sys.path.insert(0, p)


def _read_and_clean(path: str) -> str:
    """Read an OMS HTML output file and return cleaned text."""
    if not os.path.isfile(path):
        return "[no output file produced]"
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
    except Exception as exc:
        return f"[could not read output: {exc}]"
    finally:
        _try_remove(path)

    return _html_to_text(html)


def _html_to_text(html: str) -> str:
    """Best-effort conversion of SPSS OMS HTML to readable plain text."""
    if not html.strip():
        return ""

    # Try BeautifulSoup first
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["style", "script"]):
            tag.decompose()
        parts: list[str] = []
        for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "table", "div"]):
            if el.name == "table":
                rows: list[str] = []
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
        return "\n\n".join(parts)
    except ImportError:
        pass

    # Fallback: naive regex
    text = re.sub(r"(?is)<style.*?</style>", "", html)
    text = re.sub(r"(?is)<script.*?</script>", "", text)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)<tr[^>]*>", "\n", text)
    text = re.sub(r"(?i)<t[hd][^>]*>", "\t", text)
    text = re.sub(r"(?s)<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _try_remove(path: str) -> None:
    try:
        os.unlink(path)
    except OSError:
        pass
