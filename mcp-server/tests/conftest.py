from unittest.mock import Mock
import pytest

@pytest.fixture
def engine():
    engine = Mock()
    engine.is_connected.return_value = True
    engine.execute.return_value = "分析結果"
    engine.get_variable_info.return_value = [{"name": "score", "measurement": "scale", "label": "分數", "type_width": 0}]
    engine.get_case_count.return_value = 42
    return engine

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
def fake_runtime(tmp_path, monkeypatch):
    import sys
    module = tmp_path / "spss.py"
    module.write_text('''import os, re, time
_output = None
def Submit(syntax):
    global _output
    os.write(1, b"native SPSS noise\\n")
    if syntax.startswith("OMS "):
        _output = re.search("OUTFILE='(.*)'", syntax).group(1).replace("''", "'")
        with open(_output, "w", encoding="utf-8") as stream:
            stream.write("<p>分析 &amp; results</p>")
    if syntax == "FAIL.":
        raise RuntimeError("mock SPSS failure")
    if syntax == "HANG.":
        time.sleep(30)
def GetCaseCount(): return 42
def GetVariableCount(): return 1
def GetVariableName(i): return "score"
def GetVariableLabel(i): return "分數"
def GetVariableType(i): return 0
def GetVariableMeasurementLevel(i): return "scale"
def GetVariableFormat(i): return "F8.2"
''', encoding="utf-8")
    monkeypatch.setenv("SPSS_PYTHON", sys.executable)
    monkeypatch.setenv("PYTHONPATH", str(tmp_path))
    monkeypatch.setenv("SPSS_TIMEOUT", "5")
    return tmp_path
