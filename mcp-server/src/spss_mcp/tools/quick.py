"""Quick analysis tools — simplified interfaces for common analyses."""

from __future__ import annotations


def descriptives(engine, variables: str = "ALL") -> str:
    """Run descriptive statistics."""
    syntax = (
        f"DESCRIPTIVES VARIABLES={variables}\n"
        f"  /STATISTICS=MEAN STDDEV MIN MAX SKEWNESS KURTOSIS."
    )
    return engine.execute(syntax)


def frequency(engine, variables: str) -> str:
    """Run frequency analysis with bar charts."""
    syntax = (
        f"FREQUENCIES VARIABLES={variables}\n"
        f"  /BARCHART FREQ\n"
        f"  /ORDER=ANALYSIS."
    )
    return engine.execute(syntax)


def ttest(engine, dv: str, group: str, groups: str = "1 2") -> str:
    """Run independent samples t-test."""
    syntax = (
        f"T-TEST GROUPS={group}({groups})\n"
        f"  /VARIABLES={dv}\n"
        f"  /ES DISPLAY(TRUE)\n"
        f"  /CRITERIA=CI(.95)."
    )
    return engine.execute(syntax)


def ttest_paired(engine, var1: str, var2: str) -> str:
    """Run paired samples t-test."""
    syntax = (
        f"T-TEST PAIRS={var1} WITH {var2} (PAIRED)\n"
        f"  /ES DISPLAY(TRUE)\n"
        f"  /CRITERIA=CI(.95)."
    )
    return engine.execute(syntax)


def anova(engine, dv: str, factor: str, posthoc: str = "TUKEY BONFERRONI") -> str:
    """Run one-way ANOVA with post-hoc tests."""
    syntax = (
        f"ONEWAY {dv} BY {factor}\n"
        f"  /STATISTICS DESCRIPTIVES HOMOGENEITY WELCH\n"
        f"  /PLOT MEANS\n"
        f"  /POSTHOC={posthoc} ALPHA(0.05)."
    )
    return engine.execute(syntax)


def correlation(engine, variables: str, method: str = "PEARSON") -> str:
    """Run bivariate correlation analysis."""
    if method.upper() == "SPEARMAN":
        syntax = (
            f"NONPAR CORR\n"
            f"  /VARIABLES={variables}\n"
            f"  /PRINT=SPEARMAN TWOTAIL NOSIG FULL\n"
            f"  /MISSING=PAIRWISE."
        )
    else:
        syntax = (
            f"CORRELATIONS\n"
            f"  /VARIABLES={variables}\n"
            f"  /PRINT=TWOTAIL NOSIG FULL\n"
            f"  /MISSING=PAIRWISE."
        )
    return engine.execute(syntax)


def regression(engine, dv: str, ivs: str, method: str = "ENTER") -> str:
    """Run linear regression with full diagnostics."""
    syntax = (
        f"REGRESSION\n"
        f"  /DESCRIPTIVES MEAN STDDEV CORR SIG N\n"
        f"  /MISSING LISTWISE\n"
        f"  /STATISTICS COEFF OUTS CI(95) R ANOVA COLLIN TOL CHANGE\n"
        f"  /CRITERIA=PIN(.05) POUT(.10)\n"
        f"  /DEPENDENT {dv}\n"
        f"  /METHOD={method}({ivs})\n"
        f"  /SCATTERPLOT=(*ZRESID ,*ZPRED)\n"
        f"  /RESIDUALS DURBIN HISTOGRAM NORMPROB."
    )
    return engine.execute(syntax)


def crosstab(engine, row_var: str, col_var: str) -> str:
    """Run cross-tabulation with chi-square test."""
    syntax = (
        f"CROSSTABS\n"
        f"  /TABLES={row_var} BY {col_var}\n"
        f"  /FORMAT=AVALUE TABLES\n"
        f"  /STATISTICS=CHISQ CC PHI\n"
        f"  /CELLS=COUNT ROW COLUMN TOTAL EXPECTED\n"
        f"  /COUNT ROUND CELL\n"
        f"  /BARCHART."
    )
    return engine.execute(syntax)


def reliability(engine, items: str, scale_name: str = "Scale") -> str:
    """Run Cronbach's alpha reliability analysis."""
    syntax = (
        f"RELIABILITY\n"
        f"  /VARIABLES={items}\n"
        f"  /SCALE('{scale_name}') ALL\n"
        f"  /MODEL=ALPHA\n"
        f"  /STATISTICS=DESCRIPTIVE SCALE CORR\n"
        f"  /SUMMARY=TOTAL."
    )
    return engine.execute(syntax)


def factor(engine, variables: str, rotation: str = "VARIMAX") -> str:
    """Run exploratory factor analysis."""
    syntax = (
        f"FACTOR\n"
        f"  /VARIABLES {variables}\n"
        f"  /MISSING LISTWISE\n"
        f"  /PRINT INITIAL KMO AIC EXTRACTION ROTATION\n"
        f"  /FORMAT SORT BLANK(.40)\n"
        f"  /PLOT EIGEN\n"
        f"  /CRITERIA MINEIGEN(1) ITERATE(25)\n"
        f"  /EXTRACTION PC\n"
        f"  /CRITERIA ITERATE(25)\n"
        f"  /ROTATION {rotation}\n"
        f"  /METHOD=CORRELATION."
    )
    return engine.execute(syntax)


def logistic(engine, dv: str, ivs: str) -> str:
    """Run binary logistic regression."""
    syntax = (
        f"LOGISTIC REGRESSION VARIABLES {dv}\n"
        f"  /METHOD=ENTER {ivs}\n"
        f"  /PRINT=GOODFIT CI(95)\n"
        f"  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5)\n"
        f"  /SAVE=PRED PGROUP."
    )
    return engine.execute(syntax)


def explore(engine, variables: str, group: str | None = None) -> str:
    """Run Explore (descriptives + normality tests + boxplots)."""
    group_part = f" BY {group}" if group else ""
    syntax = (
        f"EXAMINE VARIABLES={variables}{group_part}\n"
        f"  /PLOT BOXPLOT HISTOGRAM NPPLOT\n"
        f"  /COMPARE GROUPS\n"
        f"  /STATISTICS DESCRIPTIVES EXTREME\n"
        f"  /CINTERVAL 95\n"
        f"  /MISSING LISTWISE\n"
        f"  /NOTOTAL."
    )
    return engine.execute(syntax)


def means_compare(engine, dv: str, group: str) -> str:
    """Run Means procedure — group-level descriptive stats with ANOVA table."""
    syntax = (
        f"MEANS TABLES={dv} BY {group}\n"
        f"  /CELLS=MEAN STDDEV COUNT."
    )
    return engine.execute(syntax)


def normality_test(engine, variables: str) -> str:
    """Run normality tests (Shapiro-Wilk + K-S) via Explore."""
    syntax = (
        f"EXAMINE VARIABLES={variables}\n"
        f"  /PLOT NPPLOT\n"
        f"  /STATISTICS DESCRIPTIVES\n"
        f"  /MISSING LISTWISE."
    )
    return engine.execute(syntax)


def levenes_test(engine, dv: str, group: str) -> str:
    """Run Levene's test for equality of variances (via ONEWAY)."""
    syntax = (
        f"ONEWAY {dv} BY {group}\n"
        f"  /STATISTICS HOMOGENEITY WELCH."
    )
    return engine.execute(syntax)
