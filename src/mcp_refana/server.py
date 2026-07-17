"""MCP server for Mu2e refana analysis."""

from __future__ import annotations

import argparse

from mcp.server.fastmcp import FastMCP
from mcp_refana.mcp_tools.refana_wrappers import register_refana_tools

mcp = FastMCP("mcp-refana", json_response=True)
register_refana_tools(mcp)


def main() -> None:
    """Run the MCP server."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
    )
    args = parser.parse_args()
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
