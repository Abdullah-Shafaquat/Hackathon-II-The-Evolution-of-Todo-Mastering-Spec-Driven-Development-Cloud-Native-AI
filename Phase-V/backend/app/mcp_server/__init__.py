"""
MCP Server Package
Model Context Protocol server for todo task management tools
"""

from app.mcp_server.server import mcp_server, get_mcp_server
from app.mcp_server.agent import create_todo_agent, AGENT_INSTRUCTIONS

# Import tools to register them with the server
# This ensures the @mcp_server.tool() decorators are executed
from app.mcp_server import tools  # noqa: F401

__all__ = [
    "mcp_server",
    "get_mcp_server",
    "create_todo_agent",
    "AGENT_INSTRUCTIONS",
]
