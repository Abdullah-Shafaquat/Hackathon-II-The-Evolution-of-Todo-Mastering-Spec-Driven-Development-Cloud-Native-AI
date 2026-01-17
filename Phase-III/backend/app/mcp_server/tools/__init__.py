"""
MCP Tools Package
Individual tool implementations for task management operations

Tools:
- add_task: Create a new todo task
- list_tasks: Retrieve user's tasks with filtering
- complete_task: Mark a task as complete
- delete_task: Delete a task
- update_task: Modify task title or description

All tools are registered with the MCP server using decorators.
"""

# Import tool implementations to register them with MCP server
from app.mcp_server.tools.add_task import add_task
from app.mcp_server.tools.list_tasks import list_tasks
from app.mcp_server.tools.complete_task import complete_task
from app.mcp_server.tools.delete_task import delete_task
from app.mcp_server.tools.update_task import update_task

__all__ = [
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "update_task",
]
