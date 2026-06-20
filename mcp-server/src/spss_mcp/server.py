"""
IBM SPSS Statistics MCP Server

Enables AI agents to directly execute statistical analyses in a local
IBM SPSS Statistics installation.

Tools provided:
  Data management:  spss_connect, spss_open_data, spss_get_variables, spss_get_summary, spss_save_data
  Quick analysis:   spss_descriptives, spss_frequency, spss_ttest, spss_ttest_paired,
                    spss_anova, spss_correlation, spss_regression, spss_crosstab,
                    spss_reliability, spss_factor, spss_logistic, spss_explore,
                    spss_normality, spss_levenes
  General:          spss_execute_syntax, spss_run_analysis
  Export:           spss_export_output, spss_export_chart, spss_clear_output
  System:           spss_status, spss_disconnect
"""

from __future__ import annotations

import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .spss_engine import SPSSEngine, SPSSError
from .tools.data import open_data, get_variable_info, get_data_summary, save_data
from .tools.analysis import execute_syntax, run_analysis
from .tools.quick import (
    descriptives, frequency, ttest, ttest_paired, anova, correlation,
    regression, crosstab, reliability, factor, logistic, explore,
    normality_test, levenes_test, means_compare,
)
from .tools.export import export_output, export_chart, clear_output
from .utils import clean_output

logger = logging.getLogger("spss-mcp")

engine = SPSSEngine()

# ═══════════════════════════════════════════════════════════════════════════
#  Tool definitions
# ═══════════════════════════════════════════════════════════════════════════

TOOLS: list[Tool] = [
    # ── System ──
    Tool(
        name="spss_connect",
        description=(
            "Connect to the local IBM SPSS Statistics installation. "
            "Automatically detects SPSS on Windows, macOS, and Linux. "
            "Must be called before any analysis tool. "
            "Optionally pass spss_home to specify the installation path."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "spss_home": {
                    "type": "string",
                    "description": "Optional. Explicit path to SPSS installation directory.",
                },
            },
        },
    ),
    Tool(
        name="spss_status",
        description="Check the current connection status to IBM SPSS.",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="spss_disconnect",
        description="Disconnect from IBM SPSS.",
        inputSchema={"type": "object", "properties": {}},
    ),

    # ── Data management ──
    Tool(
        name="spss_open_data",
        description=(
            "Open a data file in IBM SPSS. Supports .sav, .csv, .xlsx, .xls, .txt, .dat. "
            "Returns case count, variable count, and variable list."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Absolute path to the data file."},
                "encoding": {"type": "string", "description": "File encoding (default: auto-detect)."},
            },
            "required": ["file_path"],
        },
    ),
    Tool(
        name="spss_get_variables",
        description="Get all variable names, types, labels, and measurement levels from the active dataset.",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="spss_get_summary",
        description="Get descriptive statistics (mean, SD, min, max, skewness, kurtosis) for specified variables.",
        inputSchema={
            "type": "object",
            "properties": {
                "variables": {
                    "type": "string",
                    "description": "Comma-separated variable names, or 'ALL' for all numeric variables.",
                },
            },
        },
    ),
    Tool(
        name="spss_save_data",
        description="Save the active dataset to a .sav file.",
        inputSchema={
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Absolute path for the output .sav file."},
            },
            "required": ["file_path"],
        },
    ),

    # ── Quick analysis ──
    Tool(
        name="spss_descriptives",
        description="Run descriptive statistics on specified variables (mean, SD, min, max, skewness, kurtosis).",
        inputSchema={
            "type": "object",
            "properties": {
                "variables": {"type": "string", "description": "Comma-separated variable names or 'ALL'."},
            },
        },
    ),
    Tool(
        name="spss_frequency",
        description="Run frequency analysis with frequency tables and bar charts for categorical variables.",
        inputSchema={
            "type": "object",
            "properties": {
                "variables": {"type": "string", "description": "Comma-separated variable names."},
            },
            "required": ["variables"],
        },
    ),
    Tool(
        name="spss_explore",
        description=(
            "Run Explore analysis — comprehensive descriptive statistics with normality tests "
            "(Shapiro-Wilk, Q-Q plots), boxplots, histograms, and extreme values. "
            "Optionally split by a grouping variable."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "variables": {"type": "string", "description": "Comma-separated continuous variable names."},
                "group": {"type": "string", "description": "Optional. Grouping variable for split analysis."},
            },
            "required": ["variables"],
        },
    ),
    Tool(
        name="spss_normality",
        description="Run normality tests (Shapiro-Wilk, Kolmogorov-Smirnov) with Q-Q plots.",
        inputSchema={
            "type": "object",
            "properties": {
                "variables": {"type": "string", "description": "Comma-separated variable names to test."},
            },
            "required": ["variables"],
        },
    ),
    Tool(
        name="spss_levenes",
        description="Run Levene's test for equality of variances between groups.",
        inputSchema={
            "type": "object",
            "properties": {
                "dv": {"type": "string", "description": "Dependent variable (continuous)."},
                "group": {"type": "string", "description": "Grouping variable (categorical)."},
            },
            "required": ["dv", "group"],
        },
    ),
    Tool(
        name="spss_ttest",
        description="Run independent samples t-test comparing two groups on a continuous variable.",
        inputSchema={
            "type": "object",
            "properties": {
                "dv": {"type": "string", "description": "Dependent variable name."},
                "group": {"type": "string", "description": "Grouping variable name (must have exactly 2 values)."},
                "groups": {"type": "string", "description": "Group values, e.g. '1 2' (default: '1 2')."},
            },
            "required": ["dv", "group"],
        },
    ),
    Tool(
        name="spss_ttest_paired",
        description="Run paired samples t-test comparing two related measurements.",
        inputSchema={
            "type": "object",
            "properties": {
                "var1": {"type": "string", "description": "First variable (e.g., pre-test)."},
                "var2": {"type": "string", "description": "Second variable (e.g., post-test)."},
            },
            "required": ["var1", "var2"],
        },
    ),
    Tool(
        name="spss_anova",
        description="Run one-way ANOVA with descriptive statistics, homogeneity test, and post-hoc comparisons.",
        inputSchema={
            "type": "object",
            "properties": {
                "dv": {"type": "string", "description": "Dependent variable (continuous)."},
                "factor": {"type": "string", "description": "Factor/grouping variable (categorical, 3+ groups)."},
                "posthoc": {
                    "type": "string",
                    "description": "Post-hoc method: 'TUKEY BONFERRONI' (default), 'GAMESHOWELL', 'DUNNETT'.",
                },
            },
            "required": ["dv", "factor"],
        },
    ),
    Tool(
        name="spss_correlation",
        description="Run bivariate correlation analysis (Pearson or Spearman).",
        inputSchema={
            "type": "object",
            "properties": {
                "variables": {"type": "string", "description": "Comma-separated variable names (at least 2)."},
                "method": {"type": "string", "description": "'PEARSON' (default) or 'SPEARMAN'."},
            },
            "required": ["variables"],
        },
    ),
    Tool(
        name="spss_regression",
        description="Run linear regression with full diagnostics (R², F-test, coefficients, VIF, Durbin-Watson, residual plots).",
        inputSchema={
            "type": "object",
            "properties": {
                "dv": {"type": "string", "description": "Dependent variable name."},
                "ivs": {"type": "string", "description": "Comma-separated independent variable names."},
                "method": {
                    "type": "string",
                    "description": "Variable entry method: 'ENTER' (default), 'STEPWISE', 'FORWARD', 'BACKWARD'.",
                },
            },
            "required": ["dv", "ivs"],
        },
    ),
    Tool(
        name="spss_crosstab",
        description="Run cross-tabulation with chi-square test, expected frequencies, and bar chart.",
        inputSchema={
            "type": "object",
            "properties": {
                "row_var": {"type": "string", "description": "Row variable (categorical)."},
                "col_var": {"type": "string", "description": "Column variable (categorical)."},
            },
            "required": ["row_var", "col_var"],
        },
    ),
    Tool(
        name="spss_reliability",
        description="Run Cronbach's alpha reliability analysis with item-total statistics.",
        inputSchema={
            "type": "object",
            "properties": {
                "items": {"type": "string", "description": "Comma-separated item/variable names."},
                "scale_name": {"type": "string", "description": "Name of the scale (default: 'Scale')."},
            },
            "required": ["items"],
        },
    ),
    Tool(
        name="spss_factor",
        description="Run exploratory factor analysis (EFA) with KMO, Bartlett test, scree plot, and rotated loadings.",
        inputSchema={
            "type": "object",
            "properties": {
                "variables": {"type": "string", "description": "Comma-separated item/variable names."},
                "rotation": {
                    "type": "string",
                    "description": "Rotation method: 'VARIMAX' (default, orthogonal) or 'PROMAX' (oblique).",
                },
            },
            "required": ["variables"],
        },
    ),
    Tool(
        name="spss_logistic",
        description="Run binary logistic regression with model fit statistics, classification table, and OR confidence intervals.",
        inputSchema={
            "type": "object",
            "properties": {
                "dv": {"type": "string", "description": "Dependent variable (binary, 0/1 coded)."},
                "ivs": {"type": "string", "description": "Comma-separated independent variable names."},
            },
            "required": ["dv", "ivs"],
        },
    ),
    Tool(
        name="spss_means_compare",
        description="Compare means across groups — shows group-level means, SD, and counts with ANOVA table.",
        inputSchema={
            "type": "object",
            "properties": {
                "dv": {"type": "string", "description": "Dependent variable."},
                "group": {"type": "string", "description": "Grouping variable."},
            },
            "required": ["dv", "group"],
        },
    ),

    # ── General ──
    Tool(
        name="spss_execute_syntax",
        description=(
            "Execute arbitrary SPSS Syntax and return the text output. "
            "Use this for any analysis not covered by the quick tools, "
            "or for multi-step analyses, data transformations, and custom procedures."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "syntax": {
                    "type": "string",
                    "description": "Complete SPSS syntax text. Each command must end with a period (.).",
                },
            },
            "required": ["syntax"],
        },
    ),
    Tool(
        name="spss_run_analysis",
        description=(
            "Run a structured analysis by type and parameters. "
            "Available types: descriptives, frequency, ttest, anova, correlation, regression, "
            "crosstab, reliability, factor, logistic, nonparametric, glm, mixed, survival, "
            "roc, cluster, discriminant, curve, tree."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "analysis_type": {"type": "string", "description": "Type of analysis to run."},
                "params": {
                    "type": "object",
                    "description": "Analysis-specific parameters (e.g., dv, ivs, group, variables).",
                },
            },
            "required": ["analysis_type", "params"],
        },
    ),

    # ── Export ──
    Tool(
        name="spss_export_output",
        description="Export the current SPSS output to a file. Supported formats: html, docx, pdf, png, emf.",
        inputSchema={
            "type": "object",
            "properties": {
                "format": {"type": "string", "description": "Export format: 'html', 'docx', 'pdf', 'png', 'emf'."},
                "file_path": {"type": "string", "description": "Absolute path for the output file."},
            },
            "required": ["format", "file_path"],
        },
    ),
    Tool(
        name="spss_export_chart",
        description="Export only charts from the current SPSS output. Supported formats: png, emf.",
        inputSchema={
            "type": "object",
            "properties": {
                "format": {"type": "string", "description": "'png' or 'emf'."},
                "file_path": {"type": "string", "description": "Absolute path for the chart file."},
            },
            "required": ["format", "file_path"],
        },
    ),
    Tool(
        name="spss_clear_output",
        description="Clear all output from the SPSS output viewer.",
        inputSchema={"type": "object", "properties": {}},
    ),
]


# ═══════════════════════════════════════════════════════════════════════════
#  Tool dispatch
# ═══════════════════════════════════════════════════════════════════════════

def _ok(text: str) -> list[TextContent]:
    return [TextContent(type="text", text=clean_output(text))]


def _err(msg: str) -> list[TextContent]:
    return [TextContent(type="text", text=f"Error: {msg}")]


async def dispatch_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Route a tool call to the appropriate handler."""

    # ── System ──
    if name == "spss_connect":
        spss_home = arguments.get("spss_home")
        result = engine.connect(spss_home)
        return _ok(json.dumps(result, indent=2, ensure_ascii=False))

    if name == "spss_status":
        result = engine.status()
        return _ok(json.dumps(result, indent=2, ensure_ascii=False))

    if name == "spss_disconnect":
        result = engine.disconnect()
        return _ok(json.dumps(result, indent=2, ensure_ascii=False))

    # All remaining tools require connection
    if not engine.is_connected():
        return _err(
            "Not connected to IBM SPSS. Call spss_connect first.\n"
            "If SPSS is not installed, you need IBM SPSS Statistics on your computer."
        )

    # ── Data ──
    if name == "spss_open_data":
        try:
            result = open_data(engine, arguments["file_path"], arguments.get("encoding", "auto"))
            return _ok(result)
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_get_variables":
        try:
            result = get_variable_info(engine)
            return _ok(result)
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_get_summary":
        try:
            result = get_data_summary(engine, arguments.get("variables"))
            return _ok(result)
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_save_data":
        try:
            result = save_data(engine, arguments["file_path"])
            return _ok(result)
        except SPSSError as e:
            return _err(str(e))

    # ── Quick analysis ──
    if name == "spss_descriptives":
        try:
            return _ok(descriptives(engine, arguments.get("variables", "ALL")))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_frequency":
        try:
            return _ok(frequency(engine, arguments["variables"]))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_explore":
        try:
            return _ok(explore(engine, arguments["variables"], arguments.get("group")))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_normality":
        try:
            return _ok(normality_test(engine, arguments["variables"]))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_levenes":
        try:
            return _ok(levenes_test(engine, arguments["dv"], arguments["group"]))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_ttest":
        try:
            return _ok(ttest(engine, arguments["dv"], arguments["group"], arguments.get("groups", "1 2")))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_ttest_paired":
        try:
            return _ok(ttest_paired(engine, arguments["var1"], arguments["var2"]))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_anova":
        try:
            return _ok(anova(engine, arguments["dv"], arguments["factor"], arguments.get("posthoc", "TUKEY BONFERRONI")))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_correlation":
        try:
            return _ok(correlation(engine, arguments["variables"], arguments.get("method", "PEARSON")))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_regression":
        try:
            return _ok(regression(engine, arguments["dv"], arguments["ivs"], arguments.get("method", "ENTER")))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_crosstab":
        try:
            return _ok(crosstab(engine, arguments["row_var"], arguments["col_var"]))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_reliability":
        try:
            return _ok(reliability(engine, arguments["items"], arguments.get("scale_name", "Scale")))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_factor":
        try:
            return _ok(factor(engine, arguments["variables"], arguments.get("rotation", "VARIMAX")))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_logistic":
        try:
            return _ok(logistic(engine, arguments["dv"], arguments["ivs"]))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_means_compare":
        try:
            return _ok(means_compare(engine, arguments["dv"], arguments["group"]))
        except SPSSError as e:
            return _err(str(e))

    # ── General ──
    if name == "spss_execute_syntax":
        try:
            return _ok(execute_syntax(engine, arguments["syntax"]))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_run_analysis":
        try:
            result = run_analysis(engine, arguments["analysis_type"], arguments.get("params", {}))
            return _ok(result)
        except SPSSError as e:
            return _err(str(e))

    # ── Export ──
    if name == "spss_export_output":
        try:
            return _ok(export_output(engine, arguments["format"], arguments["file_path"]))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_export_chart":
        try:
            return _ok(export_chart(engine, arguments["format"], arguments["file_path"]))
        except SPSSError as e:
            return _err(str(e))

    if name == "spss_clear_output":
        try:
            return _ok(clear_output(engine))
        except SPSSError as e:
            return _err(str(e))

    return _err(f"Unknown tool: {name}")


# ═══════════════════════════════════════════════════════════════════════════
#  MCP Server entry point
# ═══════════════════════════════════════════════════════════════════════════

def create_server() -> Server:
    """Create and configure the MCP Server."""
    server = Server("spss-mcp")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        logger.info(f"Tool call: {name}({list(arguments.keys())})")
        try:
            result = await dispatch_tool(name, arguments)
            return result
        except Exception as e:
            logger.exception(f"Error in tool {name}")
            return _err(f"Unexpected error: {e}")

    return server


async def run():
    """Run the MCP Server on stdio."""
    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    """Entry point for `spss-mcp` console script."""
    import asyncio
    import sys

    # Force UTF-8 for stdio transport — avoids GBK/CP1252 encoding errors
    # on Windows with non-English locales when SPSS output contains \xa0 etc.
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.stdin.encoding and sys.stdin.encoding.lower() != "utf-8":
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())


if __name__ == "__main__":
    main()
