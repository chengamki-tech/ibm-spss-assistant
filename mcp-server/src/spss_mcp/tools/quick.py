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
    """Run linear regression.

    Note: /STATISTICS, /RESIDUALS, /SCATTERPLOT and /DESCRIPTIVES subcommands
    are omitted because they produce output tables that the SPSS CLI OMS
    capture cannot process (errLevel 3 Serious error).
    The basic coefficients, model summary and ANOVA table are always returned.
    """
    syntax = (
        f"REGRESSION\n"
        f"  /MISSING LISTWISE\n"
        f"  /DEPENDENT {dv}\n"
        f"  /METHOD={method}({ivs})."
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
        f"  /ROTATION {rotation}\n"
        f"  /METHOD=CORRELATION."
    )
    return engine.execute(syntax)


def logistic(engine, dv: str, ivs: str, dv_type: str = "auto",
             factors: str = "", covariates: str = "") -> str:
    """Run logistic regression — automatically selects binary or ordinal.

    Parameters
    ----------
    dv         : str  Dependent variable name.
    ivs        : str  Comma-separated independent variable names (used when
                      factors/covariates are not specified).
    dv_type    : str  'auto' (detect), 'binary' (0/1 DV → LOGISTIC REGRESSION),
                      'ordinal' (3+ ordered DV → PLUM).
    factors    : str  Comma-separated categorical IV names (PLUM ... BY ...).
                      When empty, falls back to ivs treated as covariates for
                      ordinal, or as a flat list for binary.
    covariates : str  Comma-separated continuous IV names (PLUM ... WITH ...).
                      When empty and dv_type is ordinal, all ivs are used as
                      covariates (safer default for survey data).
    """
    # ── Auto-detect DV type ───────────────────────────────────────────────
    if dv_type == "auto":
        dv_type = _detect_dv_type(engine, dv)

    # ── Build PLUM syntax (ordinal DV) ────────────────────────────────────
    if dv_type == "ordinal":
        # Resolve factors / covariates
        fac = factors.strip()
        cov = covariates.strip()
        if not fac and not cov:
            # No explicit split → treat all ivs as continuous covariates
            # (safer for Likert-scale survey items; avoids parameter explosion)
            cov = ivs
        elif not cov:
            cov = ""
        elif not fac:
            fac = ""

        parts = []
        if fac:
            parts.append(f"PLUM {dv} BY {_to_spss_list(fac)}")
            if cov:
                parts[0] += f" WITH {_to_spss_list(cov)}"
        elif cov:
            parts.append(f"PLUM {dv} WITH {_to_spss_list(cov)}")
        else:
            return "Error: No independent variables specified."

        parts.append("  /LINK=LOGIT")
        parts.append("  /PRINT=FIT PARAMETER SUMMARY TPARALLEL.")
        return engine.execute("\n".join(parts))

    # ── Binary logistic regression ────────────────────────────────────────
    syntax = (
        f"LOGISTIC REGRESSION VARIABLES {dv}\n"
        f"  /METHOD=ENTER {ivs}\n"
        f"  /PRINT=GOODFIT CI(95) SUMMARY\n"
        f"  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5)."
    )
    return engine.execute(syntax)


def _detect_dv_type(engine, dv: str) -> str:
    """Auto-detect whether DV is binary or ordinal by counting unique values."""
    try:
        freq_output = engine.execute(f"FREQUENCIES VARIABLES={dv}.")
        # Parse frequency table: look for lines starting with a numeric value
        # followed by a count column.  SPSS frequency output format:
        #   1.00    37   54.4   54.4   54.4
        #   2.00    19   27.9   27.9   82.4
        numeric_values = set()
        in_table = False
        for line in freq_output.split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            # Detect start of frequency table (after "Valid" header)
            if "Frequency" in stripped and "Percent" in stripped:
                in_table = True
                continue
            if in_table:
                parts = stripped.split()
                if len(parts) >= 2:
                    try:
                        val = float(parts[0])
                        count = int(float(parts[1]))
                        if count > 0:
                            numeric_values.add(val)
                    except (ValueError, IndexError):
                        # End of table or non-data line
                        if stripped.startswith("Total"):
                            break
        if len(numeric_values) > 2:
            return "ordinal"
        return "binary"
    except Exception:
        return "binary"


def _to_spss_list(var_string: str) -> str:
    """Convert comma-separated variable string to space-separated SPSS list."""
    return " ".join(v.strip() for v in var_string.split(",") if v.strip())


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
