"""Integration test that crosses a real MCP stdio protocol boundary."""

import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def _exercise_protocol() -> None:
    server = StdioServerParameters(command=sys.executable, args=["-m", "harborlight_mcp"])

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            discovered = await session.list_tools()
            assert {tool.name for tool in discovered.tools} == {
                "list_upcoming_renewals",
                "calculate_premium_change",
            }

            premium_result = await session.call_tool(
                "calculate_premium_change",
                arguments={"current_cents": 120_000, "renewal_cents": 126_000},
            )
            assert premium_result.structuredContent == {
                "current_cents": 120_000,
                "renewal_cents": 126_000,
                "change_cents": 6_000,
                "change_percent": 5.0,
                "direction": "increase",
            }

            renewal_result = await session.call_tool(
                "list_upcoming_renewals", arguments={"days": 30}
            )
            assert renewal_result.structuredContent is not None
            assert renewal_result.structuredContent["fictional"] is True
            assert [
                item["policy_id"] for item in renewal_result.structuredContent["renewals"]
            ] == ["FIC-HLA-1001", "FIC-HLA-1002", "FIC-HLA-1003"]


async def _exercise_invalid_argument() -> None:
    server = StdioServerParameters(command=sys.executable, args=["-m", "harborlight_mcp"])

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            invalid_result = await session.call_tool(
                "list_upcoming_renewals", arguments={"days": 400}
            )

    assert invalid_result.isError is True
    assert any(
        "days must be between 0 and 365" in getattr(content, "text", "")
        for content in invalid_result.content
    )


def test_stdio_tool_discovery_and_invocation() -> None:
    asyncio.run(_exercise_protocol())


def test_stdio_invalid_argument_returns_tool_error() -> None:
    asyncio.run(_exercise_invalid_argument())
