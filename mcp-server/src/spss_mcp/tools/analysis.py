"""Validated structured analyses and explicitly trusted raw syntax."""
from ..spss_engine import SPSSError
from ..validation import parameters
import os

REQUIRED = {
    "descriptives": set(), "frequency": set(), "ttest": {"dv", "group"},
    "anova": {"dv", "factor"}, "correlation": {"variables"},
    "regression": {"dv", "ivs"}, "crosstab": {"row_var", "col_var"},
    "reliability": {"items"}, "factor": {"variables"}, "logistic": {"dv", "ivs", "dv_type"},
    "nonparametric": {"test"}, "glm": {"dv", "factors"},
    "mixed": {"dv", "fixed", "random_subject"}, "survival": {"time", "status"},
    "roc": {"test_var", "state_var"}, "cluster": {"variables"},
    "discriminant": {"group", "variables"}, "curve": {"y", "x"},
    "tree": {"target", "predictors"},
}

def execute_syntax(engine, syntax):
    if os.environ.get("SPSS_ALLOW_SYNTAX", "1") != "1":
        raise SPSSError("Raw syntax is disabled by SPSS_ALLOW_SYNTAX.")
    if not isinstance(syntax, str) or not syntax.strip() or len(syntax) > 1_000_000 or "\x00" in syntax:
        raise SPSSError("Provide nonempty syntax up to 1,000,000 characters without NUL bytes.")
    return engine.execute(syntax)


def run_analysis(engine, analysis_type, params):
    if not isinstance(analysis_type, str) or not isinstance(params, dict):
        raise SPSSError("Expected analysis_type string and params object.")
    at = analysis_type.lower().strip()
    if at not in REQUIRED:
        raise SPSSError("Unknown analysis type: " + at)
    required = REQUIRED[at].copy()
    if at == "ttest" and params.get("paired") is True:
        required = {"dv"}
    if at == "nonparametric":
        required |= {"variables"} if params.get("test") in ("wilcoxon", "friedman") else {"dv", "group"}
    if at == "survival":
        required |= {"covariates"} if not params.get("group") else {"group"}
    if required - params.keys():
        raise SPSSError("Missing parameters: " + ", ".join(sorted(required - params.keys())))
    if at not in ANALYSIS_PARAMS or params.keys() - ANALYSIS_PARAMS[at]:
        raise SPSSError("Unknown parameter for " + at)
    validation_params = dict(params)
    paired_dv = validation_params.pop("dv", None) if at == "ttest" and params.get("paired") else None
    values = parameters(at, validation_params)
    if paired_dv is not None:
        words = parameters(at, {"variables": paired_dv})["variables"].split()
        if len(words) != 2:
            raise SPSSError("Paired t-test requires exactly two dv variables.")
        values["dv"] = ",".join(words)
    syntax = _build_syntax(at, values)
    if syntax.startswith("Error"):
        raise SPSSError(syntax)
    return engine.execute(syntax)


ANALYSIS_PARAMS = {'anova': {'posthoc', 'factor', 'dv'},
 'cluster': {'n_clusters', 'variables', 'method'},
 'correlation': {'variables', 'method'},
 'crosstab': {'statistics', 'col_var', 'row_var'},
 'curve': {'x', 'models', 'y'},
 'descriptives': {'variables'},
 'discriminant': {'group', 'variables', 'groups'},
 'factor': {'extraction', 'rotation', 'variables'},
 'frequency': {'variables', 'chart'},
 'glm': {'factors', 'dv'},
 'logistic': {'factors', 'ivs', 'dv_type', 'covariates', 'dv'},
 'mixed': {'random_subject', 'fixed', 'dv'},
 'nonparametric': {'group', 'variables', 'test', 'dv'},
 'regression': {'method', 'ivs', 'dv'},
 'reliability': {'items', 'scale_name'},
 'roc': {'state_value', 'test_var', 'state_var'},
 'survival': {'status_value', 'status', 'covariates', 'group', 'time'},
 'tree': {'predictors', 'target', 'method'},
 'ttest': {'paired', 'group', 'groups', 'dv'}}


def _build_syntax(analysis_type: str, params: dict) -> str:
    at = analysis_type.lower().strip()

    if at == "descriptives":
        variables = params.get("variables", "ALL")
        return (
            f"DESCRIPTIVES VARIABLES={variables}\n"
            f"  /STATISTICS=MEAN STDDEV MIN MAX SKEWNESS KURTOSIS."
        )

    if at == "frequency":
        variables = params.get("variables", "ALL")
        chart = params.get("chart", "")
        syn = f"FREQUENCIES VARIABLES={variables}"
        if chart:
            syn += f"\n  /BARCHART FREQ"
        syn += "\n  /ORDER=ANALYSIS."
        return syn

    if at == "ttest":
        dv = params.get("dv", "")
        group = params.get("group", "")
        groups = params.get("groups", "1 2")
        paired = params.get("paired", False)
        if paired:
            var1, var2 = (dv.split(",") + [""])[:2]
            return (
                f"T-TEST PAIRS={var1.strip()} WITH {var2.strip()} (PAIRED)\n"
                f"  /ES DISPLAY(TRUE)\n"
                f"  /CRITERIA=CI(.95)."
            )
        return (
            f"T-TEST GROUPS={group}({groups})\n"
            f"  /VARIABLES={dv}\n"
            f"  /ES DISPLAY(TRUE)\n"
            f"  /CRITERIA=CI(.95)."
        )

    if at == "anova":
        dv = params.get("dv", "")
        factor = params.get("factor", "")
        posthoc = params.get("posthoc", "TUKEY BONFERRONI")
        return (
            f"ONEWAY {dv} BY {factor}\n"
            f"  /STATISTICS DESCRIPTIVES HOMOGENEITY WELCH\n"
            f"  /PLOT MEANS\n"
            f"  /POSTHOC={posthoc} ALPHA(0.05)."
        )

    if at == "correlation":
        variables = params.get("variables", "")
        method = params.get("method", "PEARSON")
        if method.upper() == "SPEARMAN":
            return (
                f"NONPAR CORR\n"
                f"  /VARIABLES={variables}\n"
                f"  /PRINT=SPEARMAN TWOTAIL NOSIG FULL\n"
                f"  /MISSING=PAIRWISE."
            )
        return (
            f"CORRELATIONS\n"
            f"  /VARIABLES={variables}\n"
            f"  /PRINT=TWOTAIL NOSIG FULL\n"
            f"  /MISSING=PAIRWISE."
        )

    if at == "regression":
        dv = params.get("dv", "")
        ivs = params.get("ivs", "")
        method = params.get("method", "ENTER")
        return (
            f"REGRESSION\n"
            f"  /MISSING LISTWISE\n"
            f"  /DEPENDENT {dv}\n"
            f"  /METHOD={method} {ivs}."
        )

    if at == "crosstab":
        row = params.get("row_var", "")
        col = params.get("col_var", "")
        stats = params.get("statistics", "CHISQ CC PHI")
        return (
            f"CROSSTABS\n"
            f"  /TABLES={row} BY {col}\n"
            f"  /FORMAT=AVALUE TABLES\n"
            f"  /STATISTICS={stats}\n"
            f"  /CELLS=COUNT ROW COLUMN TOTAL EXPECTED\n"
            f"  /COUNT ROUND CELL\n"
            f"  /BARCHART."
        )

    if at == "reliability":
        items = params.get("items", "")
        name = params.get("scale_name", "Scale")
        return (
            f"RELIABILITY\n"
            f"  /VARIABLES={items}\n"
            f"  /SCALE('{name}') ALL\n"
            f"  /MODEL=ALPHA\n"
            f"  /STATISTICS=DESCRIPTIVE SCALE CORR\n"
            f"  /SUMMARY=TOTAL."
        )

    if at == "factor":
        variables = params.get("variables", "")
        extraction = params.get("extraction", "PC")
        rotation = params.get("rotation", "VARIMAX")
        return (
            f"FACTOR\n"
            f"  /VARIABLES {variables}\n"
            f"  /MISSING LISTWISE\n"
            f"  /PRINT INITIAL KMO AIC EXTRACTION ROTATION\n"
            f"  /FORMAT SORT BLANK(.40)\n"
            f"  /PLOT EIGEN\n"
            f"  /CRITERIA MINEIGEN(1) ITERATE(25)\n"
            f"  /EXTRACTION {extraction}\n"
            f"  /ROTATION {rotation}\n"
            f"  /METHOD=CORRELATION."
        )

    if at == "logistic":
        dv = params.get("dv", "")
        ivs = params.get("ivs", "")
        dv_type = params.get("dv_type", "binary")
        factors = params.get("factors", "").strip()
        covariates = params.get("covariates", "").strip()

        if dv_type == "ordinal":
            if factors and covariates:
                return (
                    f"PLUM {dv} BY {' '.join(factors.split(','))} WITH {' '.join(covariates.split(','))}\n"
                    f"  /LINK=LOGIT\n"
                    f"  /PRINT=FIT PARAMETER SUMMARY."
                )
            if factors:
                return (
                    f"PLUM {dv} BY {' '.join(factors.split(','))}\n"
                    f"  /LINK=LOGIT\n"
                    f"  /PRINT=FIT PARAMETER SUMMARY."
                )
            # Default: treat all ivs as continuous covariates
            return (
                f"PLUM {dv} WITH {' '.join(ivs.split(','))}\n"
                f"  /LINK=LOGIT\n"
                f"  /PRINT=FIT PARAMETER SUMMARY."
            )

        return (
            f"LOGISTIC REGRESSION VARIABLES {dv}\n"
            f"  /METHOD=ENTER {ivs}\n"
            f"  /PRINT=GOODFIT CI(95) SUMMARY\n"
            f"  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5)."
        )

    if at == "nonparametric":
        test = params.get("test", "mann_whitney")
        dv = params.get("dv", "")
        group = params.get("group", "")
        if "mann" in test or "whitney" in test:
            return (
                f"NPTESTS\n"
                f"  /INDEPENDENT TEST ({dv}) GROUP ({group}) MANN_WHITNEY\n"
                f"  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE."
            )
        if "kruskal" in test:
            return (
                f"NPTESTS\n"
                f"  /INDEPENDENT TEST ({dv}) GROUP ({group}) KRUSKAL_WALLIS(COMPARE=PAIRWISE)\n"
                f"  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE."
            )
        if "wilcoxon" in test:
            vars_pair = params.get("variables", "")
            return (
                f"NPTESTS\n"
                f"  /RELATED TEST({vars_pair}) WILCOXON\n"
                f"  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE."
            )
        if "friedman" in test:
            variables = params.get("variables", "")
            return (
                f"NPTESTS\n"
                f"  /RELATED TEST({variables}) FRIEDMAN(COMPARE=PAIRWISE)\n"
                f"  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE."
            )
        return f"Error: Unknown nonparametric test: {test}"

    if at == "glm":
        dv = params.get("dv", "")
        factors = params.get("factors", "")
        return (
            f"UNIANOVA {dv} BY {factors}\n"
            f"  /METHOD=SSTYPE(3)\n"
            f"  /INTERCEPT=INCLUDE\n"
            f"  /PLOT=PROFILE({factors}) TYPE=LINE ERRORBAR=CI MEANREFERENCE=NO\n"
            f"  /PRINT=ETASQ DESCRIPTIVE HOMOGENEITY\n"
            f"  /CRITERIA=ALPHA(.05)."
        )

    if at == "mixed":
        dv = params.get("dv", "")
        fixed = params.get("fixed", "")
        random_subject = params.get("random_subject", "")
        return (
            f"MIXED {dv} BY {fixed}\n"
            f"  /FIXED={fixed} | SSTYPE(3)\n"
            f"  /RANDOM=INTERCEPT | SUBJECT({random_subject}) COVTYPE(VC)\n"
            f"  /METHOD=REML\n"
            f"  /PRINT=SOLUTION TESTCOV."
        )

    if at == "survival":
        time_var = params.get("time", "")
        status_var = params.get("status", "")
        group = params.get("group", "")
        status_val = params.get("status_value", "1")
        if group:
            return (
                f"KM {time_var} BY {group}\n"
                f"  /STATUS={status_var}({status_val})\n"
                f"  /PRINT TABLE MEAN\n"
                f"  /PLOT SURVIVAL\n"
                f"  /TEST LOGRANK BRESLOW TARONE\n"
                f"  /COMPARE OVERALL POOLED."
            )
        covariates = params.get("covariates", "")
        return (
            f"COXREG {time_var}\n"
            f"  /STATUS={status_var}({status_val})\n"
            f"  /METHOD=ENTER {covariates}\n"
            f"  /PRINT=CI(95) BASELINE SURVIVAL TABLE(1,5,10)\n"
            f"  /PLOT SURVIVAL HAZARDS."
        )

    if at == "roc":
        test_var = params.get("test_var", "")
        state_var = params.get("state_var", "")
        state_val = params.get("state_value", "1")
        return (
            f"ROC {test_var} BY {state_var}({state_val})\n"
            f"  /PLOT=CURVE(REFERENCE)\n"
            f"  /PRINT=SE SP COORDINATES\n"
            f"  /CRITERIA=CUTOFF=INCLUDE TESTPOS=LR DISTRIBUTION=FREE\n"
            f"  /CI=TRUE(95)."
        )

    if at == "cluster":
        method = params.get("method", "kmeans")
        variables = params.get("variables", "")
        n_clusters = params.get("n_clusters", 3)
        if "kmeans" in method:
            return (
                f"QUICK CLUSTER {variables}\n"
                f"  /MISSING=LISTWISE\n"
                f"  /CRITERIA=CLUSTER({n_clusters}) MXITER(100) CONVERGE(0)\n"
                f"  /METHOD=KMEANS(NOUPDATE)\n"
                f"  /SAVE CLUSTER DISTANCE\n"
                f"  /PRINT INITIAL ANOVA CLUSTER DISTANCE."
            )
        if "hierarchical" in method:
            return (
                f"CLUSTER {variables}\n"
                f"  /METHOD=WARD\n"
                f"  /MEASURE=SEUCLID\n"
                f"  /PLOT=DENDROGRAM\n"
                f"  /PRINT=CLUSTER(2,{n_clusters}) SCHEDULE\n"
                f"  /SAVE=CLUSTER({n_clusters})."
            )
        if "twostep" in method:
            return (
                f"TWOSTEP CLUSTER\n"
                f"  /CONTINUOUS VARIABLES={variables}\n"
                f"  /DISTANCE LIKELIHOOD\n"
                f"  /NUMCLUSTERS AUTO 15 BIC\n"
                f"  /PRINT INITIAL SUMMARY\n"
                f"  /SAVE VARIABLE=TSC_501."
            )
        return f"Error: Unknown cluster method: {method}"

    if at == "discriminant":
        group = params.get("group", "")
        groups = params.get("groups", "1 2")
        variables = params.get("variables", "")
        return (
            f"DISCRIMINANT\n"
            f"  /GROUPS={group}({groups})\n"
            f"  /VARIABLES={variables}\n"
            f"  /ANALYSIS ALL\n"
            f"  /METHOD=WILKS\n"
            f"  /ROTATE=UNRAW\n"
            f"  /HISTOGRAM\n"
            f"  /STATISTICS=MEAN STDDEV COEFF RAW CORR CROSSVALID\n"
            f"  /PLOT=COMBINED\n"
            f"  /CLASSIFY=NONMISSING POOLED."
        )

    if at == "curve":
        y = params.get("y", "")
        x = params.get("x", "")
        models = params.get("models", "LINEAR QUADRATIC CUBIC EXPONENTIAL S")
        return (
            f"CURVEFIT\n"
            f"  /VARIABLES={y} WITH {x}\n"
            f"  /CONSTANT\n"
            f"  /MODEL={models}\n"
            f"  /PLOT FIT."
        )

    if at == "tree":
        target = params.get("target", "")
        predictors = params.get("predictors", "")
        method = params.get("method", "CHAID")
        return (
            f"TREE {target} BY {predictors}\n"
            f"  /DISPLAY=TOPDOWN NODES=BRANCHES\n"
            f"  /PRINT MODELSUMMARY CLASSIFICATION RISK\n"
            f"  /METHOD TYPE={method} MAXDEPTH=3\n"
            f"  /SAVE PREDVAL NODEID."
        )

    return f"Error: Unknown analysis type: {analysis_type}. Available: descriptives, frequency, ttest, anova, correlation, regression, crosstab, reliability, factor, logistic, nonparametric, glm, mixed, survival, roc, cluster, discriminant, curve, tree"
