"""Exercise the installed server through the actual MCP SDK transport."""
import os
from pathlib import Path
import sys
from datetime import timedelta
import anyio
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from spss_mcp.server import TOOLS

@pytest.mark.anyio
@pytest.mark.parametrize("console", [False, True])
async def test_discovery_without_spss(tmp_path, console):
    executable = str(Path(sys.executable).with_name("spss-mcp.exe" if os.name == "nt" else "spss-mcp")) if console else sys.executable
    env = {"SPSS_HOME": str(tmp_path / "absent"), "SPSS_PYTHON": str(tmp_path / "absent-python"), "PYTHONIOENCODING": "utf-8"}
    params = StdioServerParameters(command=executable, args=[] if console else ["-m", "spss_mcp"], env=env, cwd=str(tmp_path))
    with anyio.fail_after(20):
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=10)) as client:
                await client.initialize()
                tools = await client.list_tools()
                assert {t.name for t in tools.tools} == {t.name for t in TOOLS}
                assert not (await client.call_tool("spss_status", {})).isError
                missing = await client.call_tool("spss_connect", {})
                assert missing.isError
                assert "SPSS_PYTHON" in missing.content[0].text
                result = await client.call_tool("spss_descriptives", {})
                assert result.isError
                assert "Not connected" in result.content[0].text
                assert (await client.call_tool("spss_ttest", {})).isError
                assert (await client.call_tool("unknown", {})).isError
                assert not (await client.call_tool("spss_status", {})).isError


@pytest.mark.anyio
async def test_full_stdio_with_mock_spss(fake_runtime):
    params = StdioServerParameters(command=sys.executable, args=["-m", "spss_mcp"], env={
        "SPSS_PYTHON": sys.executable, "PYTHONPATH": str(fake_runtime), "SPSS_TIMEOUT": "5",
    })
    with anyio.fail_after(20):
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as client:
                await client.initialize()
                assert not (await client.call_tool("spss_connect", {})).isError
                output = await client.call_tool("spss_descriptives", {"variables": "age,score"})
                assert not output.isError
                assert "分析 & results" in output.content[0].text
                failed = await client.call_tool("spss_execute_syntax", {"syntax": "FAIL."})
                assert failed.isError
                assert "mock SPSS failure" in failed.content[0].text
                assert not (await client.call_tool("spss_disconnect", {})).isError
