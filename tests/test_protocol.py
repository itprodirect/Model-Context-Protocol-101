"""Integration tests that cross a real MCP stdio protocol boundary."""

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
            tools = {tool.name: tool for tool in discovered.tools}
            assert set(tools) == {
                "list_upcoming_renewals",
                "calculate_premium_change",
            }

            renewal_days_schema = tools["list_upcoming_renewals"].inputSchema[
                "properties"
            ]["days"]
            assert renewal_days_schema["type"] == "integer"
            assert renewal_days_schema["minimum"] == 0
            assert renewal_days_schema["maximum"] == 365

            premium_properties = tools["calculate_premium_change"].inputSchema[
                "properties"
            ]
            for field_name in ("current_cents", "renewal_cents"):
                field_schema = premium_properties[field_name]
                assert field_schema["type"] == "integer"
                assert field_schema["exclusiveMinimum"] == 0

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
    error_text = " ".join(getattr(content, "text", "") for content in invalid_result.content)
    assert "days" in error_text and "365" in error_text


async def _exercise_strict_integer_validation() -> None:
    server = StdioServerParameters(command=sys.executable, args=["-m", "harborlight_mcp"])

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            invalid_premium_values = [True, False, "120000", 120_000.0, 120_000.5]
            premium_requests = []
            for field_name in ("current_cents", "renewal_cents"):
                for invalid_value in invalid_premium_values:
                    arguments = {
                        "current_cents": 120_000,
                        "renewal_cents": 126_000,
                    }
                    arguments[field_name] = invalid_value
                    premium_requests.append(
                        (
                            "calculate_premium_change",
                            arguments,
                            f"{field_name}={invalid_value!r}",
                        )
                    )

            invalid_days_values = [True, False, "30", 30.0, 30.5]
            days_requests = [
                (
                    "list_upcoming_renewals",
                    {"days": invalid_value},
                    f"days={invalid_value!r}",
                )
                for invalid_value in invalid_days_values
            ]

            for tool_name, arguments, case_label in premium_requests + days_requests:
                result = await session.call_tool(tool_name, arguments=arguments)
                assert result.isError is True, case_label
                assert result.structuredContent is None, case_label
                assert not any(
                    '"change_cents"' in getattr(content, "text", "")
                    or '"renewals"' in getattr(content, "text", "")
                    for content in result.content
                ), case_label


def test_stdio_tool_discovery_and_invocation() -> None:
    asyncio.run(_exercise_protocol())


def test_stdio_invalid_argument_returns_tool_error() -> None:
    asyncio.run(_exercise_invalid_argument())


def test_stdio_strict_integer_validation_rejects_coercible_values() -> None:
    asyncio.run(_exercise_strict_integer_validation())
