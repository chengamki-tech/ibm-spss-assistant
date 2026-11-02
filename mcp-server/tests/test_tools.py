import pytest
from spss_mcp.spss_engine import SPSSError
from spss_mcp.tools import quick
from spss_mcp.tools.analysis import run_analysis, execute_syntax, REQUIRED
from spss_mcp.tools.data import open_data, save_data, get_variable_info
from spss_mcp.tools.export import export_output
from spss_mcp.validation import data_path
from spss_mcp.server import _dispatch, TOOLS

@pytest.mark.parametrize("call", [
    lambda e: quick.descriptives(e, "score. ERASE FILE='x'"),
    lambda e: quick.ttest(e, "score", "group", "1 2). FINISH."),
    lambda e: quick.regression(e, "score", "age", "ENTER. FINISH"),
    lambda e: quick.anova(e, "score", "group", "TUKEY /MISSING=ANALYSIS"),
    lambda e: quick.factor(e, "a,b", "BAD"),
    lambda e: quick.logistic(e, "y", "x", "auto"),
    lambda e: run_analysis(e, "regression", {"dv": "score", "ivs": "age. FINISH"}),
    lambda e: run_analysis(e, "cluster", {"variables": "a,b", "n_clusters": True}),
    lambda e: run_analysis(e, "ttest", {}),
    lambda e: run_analysis(e, "descriptives", {"surprise": "x"}),
    lambda e: run_analysis(e, "bad", {}),
])
def test_invalid_input_never_executes(engine, call):
    with pytest.raises(SPSSError):
        call(engine)
    engine.execute.assert_not_called()


def test_lists_labels_and_unicode(engine):
    quick.descriptives(engine, "age, 分數")
    assert "age 分數" in engine.execute.call_args.args[0]
    quick.reliability(engine, "a,b", "O'Brien")
    assert "O''Brien" in engine.execute.call_args.args[0]
    assert "分數" in get_variable_info(engine)


def test_paths_escaped_and_overwrites_rejected(engine, tmp_path):
    path = tmp_path / "O'Brien 資料.sav"
    path.touch()
    assert "42" in open_data(engine, str(path))
    assert "O''Brien" in engine.execute.call_args.args[0]
    with pytest.raises(SPSSError, match="already exists"):
        save_data(engine, str(path))
    with pytest.raises(SPSSError, match="absolute"):
        save_data(engine, "relative.sav")
    with pytest.raises(SPSSError):
        export_output(engine, "bad", str(tmp_path / "out.bad"))


def test_root_traversal_and_symlink(tmp_path, monkeypatch):
    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside.sav"
    outside.touch()
    monkeypatch.setenv("SPSS_DATA_ROOT", str(root))
    with pytest.raises(SPSSError, match="outside"):
        data_path(str(root / ".." / "outside.sav"))
    try:
        (root / "link.sav").symlink_to(outside)
    except OSError:
        return  # Windows runners may lack symlink privilege.
    with pytest.raises(SPSSError, match="outside"):
        data_path(str(root / "link.sav"))


def test_raw_syntax_disabled(engine, monkeypatch):
    monkeypatch.setenv("SPSS_ALLOW_SYNTAX", "0")
    with pytest.raises(SPSSError, match="disabled"):
        execute_syntax(engine, "FINISH.")
    engine.execute.assert_not_called()


@pytest.mark.parametrize("name,args", [("missing", {}), ("spss_ttest", {}), ("spss_status", {"unexpected": 1}), ("spss_descriptives", {"variables": []})])
def test_dispatch_schema(engine, name, args):
    with pytest.raises(SPSSError):
        _dispatch(name, args, engine)


def test_all_tools_have_handlers(engine):
    assert len({tool.name for tool in TOOLS}) == len(TOOLS)
    from spss_mcp.server import HANDLERS
    assert {t.name for t in TOOLS} == set(HANDLERS) | {"spss_connect", "spss_status", "spss_disconnect"}


CASES = {
    "descriptives": {}, "frequency": {}, "ttest": {"dv": "y", "group": "g"},
    "anova": {"dv": "y", "factor": "g"}, "correlation": {"variables": "a,b"},
    "regression": {"dv": "y", "ivs": "a,b"}, "crosstab": {"row_var": "a", "col_var": "b"},
    "reliability": {"items": "a,b"}, "factor": {"variables": "a,b"},
    "logistic": {"dv": "y", "ivs": "a,b", "dv_type": "binary"},
    "nonparametric": {"test": "wilcoxon", "variables": "a,b"},
    "glm": {"dv": "y", "factors": "g"}, "mixed": {"dv": "y", "fixed": "g", "random_subject": "id"},
    "survival": {"time": "t", "status": "s", "group": "g"},
    "roc": {"test_var": "x", "state_var": "y"}, "cluster": {"variables": "a,b"},
    "discriminant": {"group": "g", "variables": "a,b"}, "curve": {"y": "y", "x": "x"},
    "tree": {"target": "y", "predictors": "a,b"},
}
@pytest.mark.parametrize("kind,params", CASES.items())
def test_analysis_builders(engine, kind, params):
    assert run_analysis(engine, kind, params) == "分析結果"
    syntax = engine.execute.call_args.args[0]
    assert syntax.endswith(".")
    assert "a,b" not in syntax


def test_engine_error_propagates(engine):
    engine.execute.side_effect = SPSSError("license expired")
    with pytest.raises(SPSSError, match="license expired"):
        run_analysis(engine, "descriptives", {})


@pytest.mark.parametrize("key,value", [("dv_type", []), ("test", {}), ("chart", [])])
def test_nested_invalid_types_are_validation_errors(key, value):
    from spss_mcp.validation import parameters
    with pytest.raises(SPSSError):
        parameters("logistic", {key: value})
