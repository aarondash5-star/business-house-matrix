"""FastMCP read-only discovery endpoint. No production side effects."""
from fastmcp import FastMCP
from .config import DEPARTMENTS, DEPARTMENT_TOOL_SCOPES

mcp = FastMCP("Business House AI Matrix")


@mcp.tool
def list_departments() -> list[str]:
    """List the nine independent Business House Matrix departments."""
    return list(DEPARTMENTS)


@mcp.tool
def describe_department(name: str) -> dict:
    """Return intended tool scopes (not authorization credentials) for a department."""
    if name not in DEPARTMENTS:
        raise ValueError("Unknown department")
    return {"department": name, "tool_scopes": DEPARTMENT_TOOL_SCOPES[name],
            "structure": "brain -> execute -> qa_qc -> evolution"}


if __name__ == "__main__":
    mcp.run()
