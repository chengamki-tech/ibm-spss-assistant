"""Persistent local SPSS worker, isolated from MCP's stdout and Python ABI."""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import queue
import subprocess
import threading


class SPSSError(Exception):
    """Actionable local SPSS failure."""


class SPSSEngine:
    def __init__(self):
        self._proc = None
        self._responses = queue.Queue()
        self._lock = threading.RLock()
        self._reader = None

    def connect(self, spss_home=None):
        with self._lock:
            if self.is_connected():
                return self.status()
            self.disconnect()
            home = spss_home or os.environ.get("SPSS_HOME")
            configured = os.environ.get("SPSS_PYTHON")
            candidates = [Path(configured).expanduser()] if configured else []
            if home and not configured:
                base = Path(home).expanduser()
                candidates = [base / folder / name for folder in ("Python3", "Python", "bin", "")
                              for name in ("python.exe", "python3", "python")]
            interpreter = next((p.resolve() for p in candidates if p.is_absolute() and p.is_file()), None)
            if interpreter is None:
                raise SPSSError("IBM SPSS runtime not found. Install licensed IBM SPSS Statistics with Python Integration and set SPSS_PYTHON to its absolute Python executable path (or set SPSS_HOME).")
            try:
                self._timeout = float(os.environ.get("SPSS_TIMEOUT", "120"))
                if not math.isfinite(self._timeout) or not 0 < self._timeout <= 3600:
                    raise ValueError()
            except ValueError as exc:
                raise SPSSError("SPSS_TIMEOUT must be a number greater than 0 and at most 3600 seconds.") from exc
            try:
                self._proc = subprocess.Popen(
                    [str(interpreter), "-u", str(Path(__file__).with_name("spss_worker.py"))],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None,
                    text=True, encoding="utf-8", errors="strict", bufsize=1,
                    env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                )
                self._responses = queue.Queue()
                self._reader = threading.Thread(target=self._read, args=(self._proc, self._responses), daemon=True)
                self._reader.start()
                reply = self._receive()
                if reply.get("status") != "ready":
                    raise SPSSError("SPSS worker did not become ready.")
            except (OSError, SPSSError) as exc:
                self.disconnect()
                raise SPSSError(f"Could not start SPSS Python Integration: {exc}") from exc
            return self.status()

    @staticmethod
    def _read(proc, responses):
        try:
            for line in proc.stdout:
                responses.put(line)
        except (OSError, UnicodeError):
            pass
        finally:
            responses.put(None)

    def _receive(self):
        try:
            line = self._responses.get(timeout=self._timeout)
            if line is None:
                raise SPSSError("SPSS worker exited; check the runtime and license. Reconnect before retrying.")
            reply = json.loads(line)
            if not isinstance(reply, dict) or not isinstance(reply.get("ok"), bool):
                raise ValueError("invalid response envelope")
            if not reply["ok"]:
                raise SPSSError(str(reply.get("error", "SPSS execution failed")))
            return reply
        except queue.Empty as exc:
            raise SPSSError("SPSS worker timed out. Command outcome is unknown; inspect saved data before retrying.") from exc
        except (ValueError, TypeError) as exc:
            raise SPSSError("Invalid SPSS worker response; reconnect before retrying.") from exc

    def _command(self, request):
        with self._lock:
            if not self.is_connected():
                raise SPSSError("Not connected to IBM SPSS. Call spss_connect; install SPSS and configure SPSS_PYTHON if necessary.")
            try:
                self._proc.stdin.write(json.dumps(request, ensure_ascii=False) + "\n")
                self._proc.stdin.flush()
                reply = self._receive()
                key, expected = {
                    "execute": ("output", str),
                    "get_variables": ("variables", list),
                    "get_case_count": ("count", int),
                }[request["cmd"]]
                if key not in reply or type(reply[key]) is not expected:
                    raise SPSSError("Invalid SPSS worker response payload; reconnect before retrying.")
                return reply
            except (OSError, SPSSError) as exc:
                self.disconnect()
                raise SPSSError(str(exc)) from exc

    def execute(self, syntax, *, capture=True):
        if not isinstance(syntax, str) or not syntax.strip() or len(syntax) > 1_000_000 or "\x00" in syntax:
            raise SPSSError("Syntax must contain 1–1,000,000 characters without NUL bytes.")
        return self._command({"cmd": "execute", "syntax": syntax, "capture": capture})["output"]

    def get_variable_info(self):
        return self._command({"cmd": "get_variables"})["variables"]

    def get_case_count(self):
        return self._command({"cmd": "get_case_count"})["count"]

    def is_connected(self):
        return self._proc is not None and self._proc.poll() is None

    def status(self):
        return {"status": "connected" if self.is_connected() else "disconnected", "backend": "local_worker"}

    def disconnect(self):
        with self._lock:
            proc, self._proc = self._proc, None
            if proc:
                if proc.poll() is None:
                    proc.kill()
                proc.wait()
                for stream in (proc.stdin, proc.stdout):
                    if stream:
                        stream.close()
                if self._reader:
                    self._reader.join(timeout=2)
            return {"status": "disconnected"}
