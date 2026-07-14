"""Connect to the local server over stdio, discover tools, and call one tool."""

from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run() -> dict[str, Any]:
    """Run the protocol demo and return the structured tool result."""

    server = StdioServerParameters(command=sys.executable, args=["-m", "harborlight_mcp"])
    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("Initialized MCP session.")

            discovered = await session.list_tools()
            tool_names = sorted(tool.name for tool in discovered.tools)
            print(f"Tools: {', '.join(tool_names)}")

            called = await session.call_tool(
                "calculate_premium_change",
                arguments={"current_cents": 120_000, "renewal_cents": 126_000},
            )
            if called.structuredContent is None:
                raise RuntimeError("Server did not return structured content.")
            print("calculate_premium_change result:")
            print(json.dumps(called.structuredContent, indent=2, sort_keys=True))
            return called.structuredContent


def main() -> None:
    """Run the asynchronous client from a normal Python process."""

    asyncio.run(run())


if __name__ == "__main__":
    main()
