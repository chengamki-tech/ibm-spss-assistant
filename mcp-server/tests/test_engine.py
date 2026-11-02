import pytest
from spss_mcp.spss_engine import SPSSEngine, SPSSError


def test_absent_runtime(monkeypatch):
    monkeypatch.delenv("SPSS_HOME", raising=False)
    monkeypatch.delenv("SPSS_PYTHON", raising=False)
    engine = SPSSEngine()
    assert engine.status()["status"] == "disconnected"
    with pytest.raises(SPSSError, match="SPSS_PYTHON"):
        engine.connect()
    with pytest.raises(SPSSError, match="Not connected"):
        engine.execute("DESCRIPTIVES ALL.")
    engine.disconnect()


def test_real_worker_with_mock_integration(fake_runtime):
    engine = SPSSEngine()
    try:
        assert engine.connect()["status"] == "connected"
        assert "分析 & results" in engine.execute("DESCRIPTIVES ALL.")
        assert engine.get_case_count() == 42
        assert engine.get_variable_info()[0]["label"] == "分數"
        assert engine.execute("EXECUTE.", capture=False) == "[executed]"
        process = engine._proc
    finally:
        engine.disconnect()
    assert process.poll() is not None
    assert process.stdout.closed
    assert not engine.is_connected()


def test_execution_failure_no_retry(fake_runtime):
    engine = SPSSEngine()
    engine.connect()
    with pytest.raises(SPSSError, match="mock SPSS failure"):
        engine.execute("FAIL.")
    assert not engine.is_connected()


def test_timeout_reaps_worker(fake_runtime):
    engine = SPSSEngine()
    engine.connect()
    process = engine._proc
    engine._timeout = 0.1
    with pytest.raises(SPSSError, match="timed out"):
        engine.execute("HANG.")
    assert process.poll() is not None
    assert not engine.is_connected()


@pytest.mark.parametrize("value", ["nan", "inf", "0", "-1", "bad", "3601"])
def test_invalid_timeout(fake_runtime, monkeypatch, value):
    monkeypatch.setenv("SPSS_TIMEOUT", value)
    with pytest.raises(SPSSError, match="SPSS_TIMEOUT"):
        SPSSEngine().connect()


def test_worker_import_error(tmp_path, monkeypatch):
    import sys
    (tmp_path / "spss.py").write_text("raise ImportError('mock missing runtime')")
    monkeypatch.setenv("SPSS_PYTHON", sys.executable)
    monkeypatch.setenv("PYTHONPATH", str(tmp_path))
    with pytest.raises(SPSSError, match="mock missing runtime"):
        SPSSEngine().connect()


def test_startup_timeout(fake_runtime, monkeypatch):
    (fake_runtime / "spss.py").write_text("import time; time.sleep(30)")
    monkeypatch.setenv("SPSS_TIMEOUT", "0.1")
    engine = SPSSEngine()
    with pytest.raises(SPSSError, match="timed out"):
        engine.connect()
    assert not engine.is_connected()


def test_malformed_worker_response(fake_runtime):
    import queue
    engine = SPSSEngine()
    engine._timeout = 0.1
    for payload in ('not json', '[]', '{"ok": "yes"}'):
        engine._responses = queue.Queue()
        engine._responses.put(payload)
        with pytest.raises(SPSSError, match="Invalid"):
            engine._receive()
