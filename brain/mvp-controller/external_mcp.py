#!/usr/bin/env python3
"""Public-source-only upstream MCP Fetch adapter, invoked by mcp_tool_router.py.

This subprocess is not a general purpose web browser or MCP tool proxy.
"""
import asyncio
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = Path("/var/lib/generic-linux-automator-exec/matrix-external-mcp/venv/bin/mcp-server-fetch")
DOC_HOSTS = frozenset({
    "docs.python.org", "docs.github.com", "developer.mozilla.org",
    "modelcontextprotocol.io", "packaging.python.org",
    "docs.pytest.org", "docs.langchain.com",
})
SOURCE_PREFIX = "/aarondash5-star/business-house-matrix/"
MAX_CHARS = 10000

def validate_url(value: str) -> str:
    if not isinstance(value, str) or not 15 <= len(value) <= 500:
        raise ValueError("URL length out of bounds")
    if any(ord(char) < 33 or ord(char) > 126 for char in value):
        raise ValueError("Unsafe character in URL")
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or parsed.username or parsed.password
            or parsed.query or parsed.fragment):
        raise ValueError("Public HTTPS URL required, without credentials/query/fragment")
    if parsed.port not in (None, 443):
        raise ValueError("Unexpected network port")
    host = (parsed.hostname or "").lower()
    if host not in DOC_HOSTS and host not in {"github.com", "raw.githubusercontent.com"}:
        raise ValueError("Host not allowlisted")
    if host == "github.com" and not parsed.path.startswith(SOURCE_PREFIX):
        raise ValueError("Only Matrix GitHub repo permitted")
    if (host == "raw.githubusercontent.com"
            and not parsed.path.startswith(SOURCE_PREFIX + "main/")):
        raise ValueError("Only canonical Matrix source permitted")
    if any(part in parsed.path for part in ("%", "\\", "..", "//")):
        raise ValueError("Noncanonical URL path")
    return value

async def fetch(url: str) -> dict:
    url = validate_url(url)
    params = StdioServerParameters(command=str(SERVER), args=[])
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            handshake = await asyncio.wait_for(session.initialize(), timeout=12)
            inventory = await asyncio.wait_for(session.list_tools(), timeout=12)
            if "fetch" not in {tool.name for tool in inventory.tools}:
                raise RuntimeError("Upstream MCP fetch not advertised")
            result = await asyncio.wait_for(session.call_tool("fetch", {
                "url": url, "max_length": MAX_CHARS, "start_index": 0
            }), timeout=42)
            if result.is_error:
                raise RuntimeError("Upstream MCP returned failure")
            content = "\n".join(getattr(item, "text", "") for item in result.content).strip()
            if not content:
                raise RuntimeError("External MCP returned no text")
            return {
                "provider": "external-mcp", "server": "mcp-server-fetch",
                "transport": "stdio", "protocol": str(handshake.protocol_version),
                "tool": "fetch", "url": url, "text": content[:MAX_CHARS],
                "content_chars": len(content[:MAX_CHARS]),
                "trust": "untrusted_external_source",
                "qa": "retrieval_only", "writes_performed": False,
            }

def selftest():
    good = [
        "https://docs.python.org/3/library/asyncio-task.html",
        "https://raw.githubusercontent.com/aarondash5-star/business-house-matrix/main/README.md",
    ]
    bad = [
        "http://docs.python.org/3/library/asyncio-task.html",
        "https://127.0.0.1/private", "https://localhost/",
        "https://raw.githubusercontent.com/other-owner/other/main/a",
        "https://github.com/other/other/blob/main/a",
        "https://docs.python.org:4443/",
        "https://docs.python.org/../secrets",
        "https://docs.python.org/a?token=oops",
        "https://docs.python.org/a%2fb",
        "https://docs.python.org/a#frag",
    ]
    for link in good:
        assert validate_url(link) == link
    for link in bad:
        try: validate_url(link)
        except ValueError: pass
        else: raise AssertionError("Unsafe URL accepted")
    return {"passed": True, "allowed": len(good), "blocked": len(bad)}

def main():
    try:
        if len(sys.argv) == 2 and sys.argv[1] == "selftest":
            print(json.dumps(selftest())); return
        if len(sys.argv) == 3 and sys.argv[1] == "validate":
            print(json.dumps({"valid": True, "url": validate_url(sys.argv[2])})); return
        if len(sys.argv) == 3 and sys.argv[1] == "fetch":
            print(json.dumps(asyncio.run(fetch(sys.argv[2])), ensure_ascii=False)); return
        raise ValueError("Usage: external_mcp.py selftest|validate URL|fetch URL")
    except Exception as exc:
        print(json.dumps({"error": type(exc).__name__, "detail": str(exc)[:180]}),
              file=sys.stderr)
        raise SystemExit(2)

if __name__ == "__main__":
    main()
