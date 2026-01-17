"""
MCP Server for Todo Task Management
Exposes task operations as MCP tools for OpenAI Agents SDK integration
"""

from mcp.server import FastMCP

# Initialize MCP server instance
mcp_server = FastMCP(
    name="todo-mcp-server",
    instructions=(
        "MCP server for todo task management. "
        "Provides tools for creating, reading, updating, and deleting tasks. "
        "All operations are scoped to the authenticated user."
    )
)

# Tool registry - tools will be registered using @mcp_server.tool() decorator
# Individual tool implementations are in the tools/ subdirectory

def get_mcp_server():
    """
    Get the MCP server instance.

    Returns:
        FastMCP: The configured MCP server instance
    """
    return mcp_server
