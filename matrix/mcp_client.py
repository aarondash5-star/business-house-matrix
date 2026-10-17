"""Optional current LangChain MCP integration. Tool execution is NOT wired in MVP.

Production: authenticate per department using server-side ContextForge policies,
not just the client-side scope names in config.py.
"""
from contextlib import asynccontextmanager


@asynccontextmanager
async def discover_tools(server_url: str):
    from fastmcp import Client
    from langchain.mcp import MCPAdapter

    client = Client(server_url, cache=True)
    async with MCPAdapter(client) as adapter:
        yield await adapter.list_tools(cache_mode="use")
