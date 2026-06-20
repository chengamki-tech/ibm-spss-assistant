"""
IBM SPSS Statistics Engine

Connects to the local IBM SPSS installation and executes syntax.
Supports three backends (tried in order):
  1. spss Python module (SPSS Integration Plug-in — same Python as MCP server)
  2. Persistent worker subprocess (SPSS's bundled Python 3.8)
  3. COM automation (Windows only, requires SPSS GUI running)
"""

import os
import sys
import re
import json
import tempfile
import platform
import subprocess
import threading
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
        self._worker_proc = None      # Persistent subprocess (if backend=cli)
        self._worker_lock = threading.Lock()  # Serialise worker commands
        self._connected = False

    # ── public ────────────────────────────────────────────────────────────
    def connect(self, spss_home: str | None = None) -> dict:
        """Connect to IBM SPSS Statistics.

        Parameters
        ----------
        spss_home : str | None
            Explicit SPSS installation directory.  When *None* the engine
            auto-detects the installation by checking the registry,
            SPSS_HOME environment variable, and common install paths.

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

        # ── try backend 1: spss Python module (same Python process) ──
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

        # ── try backend 2: persistent worker subprocess ──
        if self._start_worker():
            self._backend = "cli"
            self._connected = True
            return self._status_dict("connected")

        # ── try backend 3: COM (Windows only) — requires SPSS GUI running ──
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
        if self._backend == "cli" and self._worker_proc:
            self._stop_worker()
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

        if self._backend == "cli" and self._worker_proc:
            resp = self._worker_cmd({"cmd": "get_variables"})
            if resp.get("ok"):
                return resp.get("variables", [])
            # Fallback to DISPLAY DICTIONARY
            pass

        # Fallback for COM or worker failure
        out = self.execute("DISPLAY DICTIONARY.")
        return [{"raw": out}]

    def get_case_count(self) -> int:
        if not self._connected:
            raise SPSSError("Not connected to SPSS.")
        if self._backend == "spss_module":
            return self._module.GetCaseCount()
        if self._backend == "cli" and self._worker_proc:
            resp = self._worker_cmd({"cmd": "get_case_count"})
            if resp.get("ok"):
                return resp.get("count", -1)
        return -1  # unknown

    def is_connected(self) -> bool:
        return self._connected

    # ── private: persistent worker subprocess ─────────────────────────────
    def _start_worker(self) -> bool:
        """Launch the persistent SPSS worker subprocess. Returns True on success."""
        worker_script = os.path.join(
            os.path.dirname(__file__), "spss_worker.py"
        )
        if not os.path.isfile(worker_script):
            return False

        # Find SPSS's Python interpreter
        py_exe = self._find_spss_python()
        if not py_exe:
            # Try statisticspython3.bat
            bat = os.path.join(self._spss_home, "statisticspython3.bat")
            if os.path.isfile(bat):
                cmd = [bat, worker_script]
            else:
                return False
        else:
            cmd = [py_exe, worker_script]

        try:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                errors="replace",
                bufsize=1,  # line-buffered
            )
        except Exception:
            return False

        # Read the "ready" response
        try:
            line = proc.stdout.readline()
            resp = json.loads(line)
            if resp.get("ok") and resp.get("status") == "ready":
                self._worker_proc = proc
                return True
        except Exception:
            pass

        # Worker failed to start — clean up
        try:
            proc.kill()
        except Exception:
            pass
        return False

    def _stop_worker(self):
        """Gracefully stop the worker subprocess."""
        proc = self._worker_proc
        self._worker_proc = None
        if proc:
            try:
                proc.stdin.write(json.dumps({"cmd": "quit"}) + "\n")
                proc.stdin.flush()
                proc.wait(timeout=5)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass

    def _worker_cmd(self, cmd: dict) -> dict:
        """Send a command to the worker and return the response dict."""
        if not self._worker_proc:
            return {"ok": False, "error": "Worker not running"}

        with self._worker_lock:
            proc = self._worker_proc
            try:
                line = json.dumps(cmd, ensure_ascii=False) + "\n"
                proc.stdin.write(line)
                proc.stdin.flush()
                resp_line = proc.stdout.readline()
                if not resp_line:
                    # Worker died — try to restart once
                    self._worker_proc = None
                    raise SPSSError("SPSS worker subprocess died unexpectedly.")
                return json.loads(resp_line)
            except (BrokenPipeError, OSError) as exc:
                self._worker_proc = None
                raise SPSSError(f"SPSS worker communication error: {exc}") from exc

    def _find_spss_python(self) -> str | None:
        """Find the SPSS Python interpreter."""
        patterns = [
            os.path.join(self._spss_home, "Python3", "python.exe"),
            os.path.join(self._spss_home, "Python", "python.exe"),
            os.path.join(self._spss_home, "Python3", "python"),
            os.path.join(self._spss_home, "Python", "python"),
        ]
        for p in patterns:
            if os.path.isfile(p):
                return p
        return None

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
        """Execute syntax via the persistent worker subprocess."""
        resp = self._worker_cmd({
            "cmd": "execute",
            "syntax": syntax,
            "capture": capture,
        })
        if resp.get("ok"):
            return resp.get("output", "[executed]")
        raise SPSSError(f"SPSS error: {resp.get('error', 'unknown error')}")

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
    """Return (home_dir, executable, version) or (None, None, None).

    Searches (in order):
      1. Windows Registry (HKLM / HKCU / WOW6432Node)
      2. Environment variable SPSS_HOME
      3. Common install directories on all platforms
      4. `which stats` on macOS / Linux
    """
    system = platform.system()
    candidates: list[tuple[str, str]] = []  # (home, version)

    # ── 1. Windows Registry ─────────────────────────────────────────────
    if system == "Windows":
        try:
            import winreg  # type: ignore
            registry_roots = [
                winreg.HKEY_LOCAL_MACHINE,
                winreg.HKEY_CURRENT_USER,
            ]
            registry_prefixes = [
                "SOFTWARE\\IBM\\SPSS Statistics",
                "SOFTWARE\\WOW6432Node\\IBM\\SPSS Statistics",
                "SOFTWARE\\IBM\\SPSS",
                "SOFTWARE\\WOW6432Node\\IBM\\SPSS",
            ]
            for v in range(40, 23, -1):
                for suffix in (f"{v}.0", f"{v}", str(v)):
                    for prefix in registry_prefixes:
                        for root in registry_roots:
                            try:
                                key = winreg.OpenKey(root, f"{prefix}\\{suffix}")
                                home, _ = winreg.QueryValueEx(key, "InstallDir")
                                winreg.CloseKey(key)
                                candidates.append((home.rstrip("\\/"), str(v)))
                            except FileNotFoundError:
                                pass
        except ImportError:
            pass

    # ── 2. Environment variable ──────────────────────────────────────────
    env_home = os.environ.get("SPSS_HOME") or os.environ.get("SPSSTATHOME")
    if env_home and os.path.isdir(env_home):
        # Try to guess version from path
        version = "unknown"
        for v in range(40, 23, -1):
            if str(v) in env_home:
                version = str(v)
                break
        candidates.append((env_home.rstrip("\\/"), version))

    # ── 3. Common install directories ────────────────────────────────────
    if system == "Windows":
        roots = [
            os.environ.get("ProgramFiles", r"C:\Program Files"),
            os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
            "C:\\Program Files",
            "C:\\Program Files (x86)",
            "D:\\Program Files",
            "D:\\Program Files (x86)",
            "C:\\",
            "D:\\",
        ]
        subpatterns = []
        for v in range(40, 23, -1):
            subpatterns += [
                ("IBM", "SPSS", "Statistics", str(v)),
                ("IBM", "SPSS", "Statistics", f"{v}.0"),
                ("IBM", "SPSS", str(v)),
                ("IBM", "SPSS", f"{v}.0"),
                ("IBM", "SPSS Statistics", str(v)),
                ("SPSS Inc", f"SPSS {v}"),
                ("SPSS", f"Statistics {v}"),
                (f"SPSS {v}",),
                (f"SPSS{v}",),
                ("SPSS",),
                ("IBM", "SPSS"),
            ]

        for root in roots:
            if not root or not os.path.isdir(root):
                continue
            for sub in subpatterns:
                path = os.path.join(root, *sub)
                if os.path.isdir(path):
                    version = "unknown"
                    for v in range(40, 23, -1):
                        if str(v) in path:
                            version = str(v)
                            break
                    candidates.append((path, version))

    elif system == "Darwin":
        for v in range(40, 23, -1):
            for base in ["/Applications", os.path.expanduser("~/Applications")]:
                candidates.append((f"{base}/IBM/SPSS/Statistics/{v}", str(v)))
                candidates.append((f"{base}/IBM/SPSS/Statistics/{v}.0", str(v)))
                candidates.append((f"{base}/IBM/SPSS/{v}", str(v)))
                candidates.append((f"{base}/SPSS Inc/SPSS {v}", str(v)))

    else:  # Linux
        for v in range(40, 23, -1):
            for base in ["/opt", "/usr/local", "/opt/ibm"]:
                candidates.append((f"{base}/ibm/SPSS/Statistics/{v}", str(v)))
                candidates.append((f"{base}/ibm/SPSS/Statistics/{v}.0", str(v)))
                candidates.append((f"{base}/ibm/SPSS/{v}", str(v)))

    # ── 4. Check all candidates ──────────────────────────────────────────
    seen: set[str] = set()
    for home, ver in candidates:
        home_norm = os.path.normpath(home)
        if home_norm in seen or not os.path.isdir(home_norm):
            continue
        seen.add(home_norm)
        exe = _find_exe(home_norm)
        if exe:
            return home_norm, exe, ver

    # ── 5. Fallback: search PATH on Unix ─────────────────────────────────
    if system != "Windows":
        try:
            result = subprocess.run(["which", "stats"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                stats_path = result.stdout.strip()
                if stats_path and os.path.isfile(stats_path):
                    return os.path.dirname(os.path.dirname(stats_path)), stats_path, "unknown"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    return None, None, None


def _find_exe(home: str) -> str | None:
    """Find the stats executable inside *home*."""
    system = platform.system()
    exe_names = ("stats.com", "stats.exe", "spss.com", "spss.exe") if system == "Windows" else ("stats", "spss")
    sub_dirs = ("", "bin", "Stats", "Bin")

    for sub in sub_dirs:
        for name in exe_names:
            p = os.path.join(home, sub, name) if sub else os.path.join(home, name)
            if os.path.isfile(p):
                return p

    # Windows: also look one level deeper for known folder names
    if system == "Windows":
        for deeper in ("Statistics", "SPSS"):
            inner = os.path.join(home, deeper)
            if os.path.isdir(inner):
                for name in exe_names:
                    p = os.path.join(inner, name)
                    if os.path.isfile(p):
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
        import html as html_mod
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
        text = "\n\n".join(parts)
        # Decode any remaining HTML entities
        text = html_mod.unescape(text)
        # Strip temp file names that leak from <title> tags
        text = re.sub(r"^tmp\w+\.html\s*", "", text)
        return text.strip()
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


def _is_spss_running() -> bool:
    """Check if IBM SPSS Statistics is already running."""
    system = platform.system()
    try:
        if system == "Windows":
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq stats.exe", "/NH"],
                capture_output=True, text=True, timeout=5,
            )
            return "stats.exe" in result.stdout
        elif system == "Darwin":
            result = subprocess.run(
                ["pgrep", "-f", "SPSSStatistics"],
                capture_output=True, text=True, timeout=5,
            )
            return result.returncode == 0
        else:
            result = subprocess.run(
                ["pgrep", "-f", "stats"],
                capture_output=True, text=True, timeout=5,
            )
            return result.returncode == 0
    except Exception:
        return False
