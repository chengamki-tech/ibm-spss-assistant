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
        description="Run logistic regression with model fit statistics, classification table, and OR confidence intervals. Supports both binary (0/1) and ordinal (3+ levels) dependent variables. Auto-detects DV type.",
        inputSchema={
            "type": "object",
            "properties": {
                "dv": {"type": "string", "description": "Dependent variable (binary or ordinal)."},
                "ivs": {"type": "string", "description": "Comma-separated independent variable names."},
                "dv_type": {"type": "string", "enum": ["auto", "binary", "ordinal"], "default": "auto", "description": "'binary' for 0/1 DV (LOGISTIC REGRESSION), 'ordinal' for 3+ ordered levels (PLUM), 'auto' to detect automatically."},
                "factors": {"type": "string", "default": "", "description": "Comma-separated categorical IV names for ordinal regression (PLUM ... BY ...). Ignored for binary."},
                "covariates": {"type": "string", "default": "", "description": "Comma-separated continuous IV names for ordinal regression (PLUM ... WITH ...). Ignored for binary."},
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

def _ok(text):
    return [TextContent(type="text", text=clean_output(text))]


# Use the public schemas for MCP and direct Python dispatch validation.
for tool in TOOLS:
    tool.inputSchema["additionalProperties"] = False

# Keep help aligned with runtime behavior.
for tool in TOOLS:
    if tool.name == "spss_connect":
        tool.description = "Connect to licensed local SPSS Python Integration. Set SPSS_PYTHON or SPSS_HOME; no cloud service is used."
    if tool.name == "spss_open_data":
        tool.description = "Open an absolute .sav, .xls or .xlsx path. Delimited files require explicit GET DATA syntax with a variable schema."
    if tool.name == "spss_regression":
        tool.description = "Run linear regression with model summary, ANOVA and coefficients. Use raw syntax for additional diagnostics."
    if tool.name == "spss_logistic":
        tool.description = "Run binary or ordinal logistic regression. Specify dv_type explicitly."
        tool.inputSchema["properties"]["dv_type"] = {"type": "string", "enum": ["binary", "ordinal"]}
        tool.inputSchema["required"].append("dv_type")


HANDLERS = {
    "spss_open_data": open_data, "spss_get_variables": get_variable_info,
    "spss_get_summary": get_data_summary, "spss_save_data": save_data,
    "spss_descriptives": descriptives, "spss_frequency": frequency,
    "spss_ttest": ttest, "spss_ttest_paired": ttest_paired,
    "spss_anova": anova, "spss_correlation": correlation,
    "spss_regression": regression, "spss_crosstab": crosstab,
    "spss_reliability": reliability, "spss_factor": factor,
    "spss_logistic": logistic, "spss_explore": explore,
    "spss_normality": normality_test, "spss_levenes": levenes_test,
    "spss_means_compare": means_compare, "spss_execute_syntax": execute_syntax,
    "spss_run_analysis": run_analysis, "spss_export_output": export_output,
    "spss_export_chart": export_chart, "spss_clear_output": clear_output,
}


def _dispatch(name, arguments, local_engine):
    from jsonschema import Draft202012Validator
    tool = next((t for t in TOOLS if t.name == name), None)
    if tool is None:
        raise SPSSError(f"Unknown tool: {name}")
    errors = list(Draft202012Validator(tool.inputSchema).iter_errors(arguments))
    if errors:
        raise SPSSError("Invalid arguments: " + errors[0].message)
    if name == "spss_connect":
        return json.dumps(local_engine.connect(**arguments), ensure_ascii=False)
    if name == "spss_status":
        return json.dumps(local_engine.status(), ensure_ascii=False)
    if name == "spss_disconnect":
        return json.dumps(local_engine.disconnect(), ensure_ascii=False)
    if not local_engine.is_connected():
        raise SPSSError("Not connected to IBM SPSS. Call spss_connect. If SPSS is not installed, install licensed SPSS with Python Integration and set SPSS_PYTHON.")
    return HANDLERS[name](local_engine, **arguments)


async def dispatch_tool(name, arguments, local_engine):
    """Serialize stateful calls in a thread so MCP's event loop stays responsive."""
    import anyio
    return _ok(await anyio.to_thread.run_sync(_dispatch, name, arguments, local_engine))


def create_server(local_engine=None):
    from contextlib import asynccontextmanager
    from mcp.types import CallToolResult
    import anyio
    local_engine = local_engine or SPSSEngine()
    lock = anyio.Lock()

    @asynccontextmanager
    async def lifespan(server):
        try:
            yield {}
        finally:
            await anyio.to_thread.run_sync(local_engine.disconnect)

    server = Server("spss-mcp", lifespan=lifespan)

    @server.list_tools()
    async def list_tools():
        return TOOLS

    @server.call_tool()
    async def call_tool(name, arguments):
        async with lock:
            try:
                content = await dispatch_tool(name, arguments, local_engine)
                return CallToolResult(content=content, isError=False)
            except (SPSSError, ValueError, TypeError, OSError) as exc:
                return CallToolResult(content=_ok(str(exc)), isError=True)
            except Exception:
                logger.exception("Unexpected tool failure: %s", name)
                return CallToolResult(content=_ok("Unexpected local SPSS failure; see server stderr for details."), isError=True)
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
