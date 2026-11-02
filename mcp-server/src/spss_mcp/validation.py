"""Validation at tool and syntax-builder boundaries."""
from __future__ import annotations
import functools
import inspect
import os
from pathlib import Path
import re
from .spss_engine import SPSSError

IDENT = re.compile(r"(?:[^\W\d]|[@#$])[\w@#$]*", re.UNICODE)
LISTS = {"variables", "ivs", "items", "factors", "covariates", "fixed", "predictors"}
SINGLES = {"dv", "group", "var1", "var2", "factor", "row_var", "col_var", "random_subject", "time", "status", "test_var", "state_var", "x", "y", "target"}
CHOICES = {
    "posthoc": {"TUKEY", "BONFERRONI", "GAMESHOWELL", "SCHEFFE", "LSD", "SIDAK"},
    "rotation": {"VARIMAX", "PROMAX", "NONE", "OBLIMIN", "QUARTIMAX", "EQUAMAX"},
    "extraction": {"PC", "PAF", "ML", "ULS", "GLS", "ALPHA", "IMAGE"},
    "statistics": {"CHISQ", "CC", "PHI", "LAMBDA", "UC", "ETA", "CORR", "RISK", "MCNEMAR"},
    "models": {"LINEAR", "QUADRATIC", "CUBIC", "EXPONENTIAL", "S", "LOGARITHMIC", "INVERSE", "POWER", "COMPOUND", "GROWTH", "LOGISTIC"},
}
METHODS = {"correlation": {"PEARSON", "SPEARMAN"}, "regression": {"ENTER", "STEPWISE", "FORWARD", "BACKWARD"}, "cluster": {"KMEANS", "HIERARCHICAL", "TWOSTEP"}, "tree": {"CHAID", "EXHAUSTIVECHAID", "CRT", "QUEST"}}

def literal(value):
    if not isinstance(value, str) or any(ord(c) < 32 for c in value):
        raise SPSSError("Text must not contain control characters.")
    return value.replace("'", "''")


def data_path(value, *, output=False):
    literal(value)
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise SPSSError("File paths must be absolute.")
    path = path.resolve()
    root = os.environ.get("SPSS_DATA_ROOT")
    if root:
        base = Path(root).expanduser()
        if not base.is_absolute() or not base.is_dir():
            raise SPSSError("SPSS_DATA_ROOT must be an existing absolute directory.")
        if not path.is_relative_to(base.resolve()):
            raise SPSSError("File path is outside SPSS_DATA_ROOT.")
    if output:
        if not path.parent.is_dir():
            raise SPSSError("Output parent directory does not exist.")
        if path.exists():
            raise SPSSError("Output already exists; choose a new file path.")
    elif not path.is_file():
        raise SPSSError(f"File not found: {path}")
    return literal(path.as_posix())


def parameters(context, values):
    result = dict(values)
    for key, value in values.items():
        if key in LISTS or key in SINGLES:
            if value is None and key == "group" and context == "explore":
                continue
            if value == "" and key in {"factors", "covariates"}:
                continue
            if not isinstance(value, str) or any(ord(c) < 32 for c in value):
                raise SPSSError(f"{key} must contain variable names.")
            words = value.replace(",", " ").split()
            if not words or any(not IDENT.fullmatch(w) or len(w.encode('utf-8')) > 64 for w in words):
                raise SPSSError(f"Invalid variable name in {key}.")
            if key in SINGLES and len(words) != 1:
                raise SPSSError(f"{key} requires one variable name.")
            result[key] = " ".join(words)
        elif key in CHOICES or key == "method":
            choices = METHODS.get(context, set()) if key == "method" else CHOICES[key]
            if not isinstance(value, str) or not value.split() or any(w.upper() not in choices for w in value.split()):
                raise SPSSError(f"Invalid {key} for {context}.")
            if key != "posthoc" and key != "statistics" and key != "models" and len(value.split()) != 1:
                raise SPSSError(f"{key} requires one option.")
            result[key] = value.upper() if key != "method" or context not in {"cluster"} else value.lower()
        elif key == "scale_name":
            result[key] = literal(value)
        elif key in {"groups", "status_value", "state_value"}:
            if not isinstance(value, (str, int, float)) or isinstance(value, bool):
                raise SPSSError(f"Invalid {key}.")
            words = str(value).split()
            if len(words) != (2 if key == "groups" else 1) or any(not re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)", w) for w in words):
                raise SPSSError(f"{key} requires numeric values.")
            result[key] = " ".join(words)
        elif key == "n_clusters":
            if type(value) is not int or not 2 <= value <= 1000:
                raise SPSSError("n_clusters must be an integer from 2 to 1000.")
        elif key == "dv_type":
            if not isinstance(value, str) or value not in {"binary", "ordinal"}:
                raise SPSSError("Specify dv_type='binary' or 'ordinal'; automatic inference is not reliable.")
        elif key == "paired":
            if type(value) is not bool:
                raise SPSSError("paired must be boolean.")
        elif key == "chart":
            if not isinstance(value, (str, bool)) or value not in {"", "bar", True, False}:
                raise SPSSError("chart must be 'bar' or boolean.")
        elif key == "test":
            if not isinstance(value, str) or value not in {"mann_whitney", "kruskal_wallis", "wilcoxon", "friedman"}:
                raise SPSSError("Unsupported nonparametric test.")
        else:
            raise SPSSError(f"Unknown parameter: {key}")
    minimums = {"correlation": ("variables", 2), "reliability": ("items", 2), "factor": ("variables", 2)}
    if context in minimums:
        key, minimum = minimums[context]
        if key in result and len(result[key].split()) < minimum:
            raise SPSSError(f"{context} requires at least {minimum} variables.")
    return result


def validated(function):
    """Protect direct Python helpers as well as MCP dispatch."""
    signature = inspect.signature(function)
    @functools.wraps(function)
    def wrapper(engine, *args, **kwargs):
        bound = signature.bind(engine, *args, **kwargs)
        bound.apply_defaults()
        values = {k: v for k, v in bound.arguments.items() if k != "engine"}
        values = parameters(function.__name__, values)
        return function(engine, **values)
    return wrapper
