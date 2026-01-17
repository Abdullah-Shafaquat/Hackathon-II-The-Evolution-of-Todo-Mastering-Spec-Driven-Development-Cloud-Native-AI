"""
OpenAI Agent Configuration
Configures OpenAI Agents SDK with MCP tools for todo management
"""

import json
from typing import Any, Dict
from sqlmodel import Session
from agents import Agent, FunctionTool
from app.config import settings
from app.mcp_server.tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
)
from app.mcp_server.context import inject_context_into_tool_call


# Agent system instructions
AGENT_INSTRUCTIONS = """You ARE the Project Agent. Identify tasks by TITLE, never by ID.

**ABSOLUTE RULES:**
1. Identify tasks from TITLE or conversation context - NEVER ask for ID
2. Auto-correct spelling and grammar without changing meaning
3. After ANY edit, show the updated task with: Title, Description, Priority, Category
4. Keep responses clear and concise - no unrelated information
5. If task unclear, ask about TITLE only: "Which task - [name1] or [name2]?"

**EDITING TASKS:**
- Find task by title/name user provides or from context
- Update exactly what user instructs (description, priority, category, status)
- After update, ALWAYS confirm with full task details:
  "Updated: [Title]
   Description: [text]
   Priority: [level]
   Category: [type]"

**TASK IDENTIFICATION:**
- "this task" / "is ko" / "us ko" → last mentioned task in conversation
- "[task name]" → find by that name
- "the one I added" → most recent task
- Context from conversation history

**AUTO-CORRECTIONS:**
- Fix typos: "byu car" → "buy car"
- Fix grammar: "go store" → "go to store"
- Keep original meaning intact

**LANGUAGE (English/Hindi/Urdu):**
- "ban do" = create
- "us ki" / "is ki" = its
- "kar do" = do it
- "badal do" = change
- "dikha do" = show

**RESPONSE FORMAT:**
- Add task → "Added: [name]"
- Edit task → Show updated task details
- Delete → "Deleted: [name]"
- Show tasks → Clean list with all details

**NEVER:**
- Ask for task ID
- Say "I need the ID"
- Add unrelated information
- Skip showing updated details after edit"""


def create_todo_agent() -> Agent:
    """
    Create and configure the OpenAI agent with MCP tools.

    This agent uses the OpenAI Agents SDK with function calling to interact
    with MCP tools for todo management. All tools receive user_id from context
    (injected in Task 4.8).

    Returns:
        Agent: Configured OpenAI agent with all 5 MCP tools

    Raises:
        ValueError: If OPENAI_API_KEY is not configured
    """
    # Validate configuration
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your-openai-api-key-here":
        raise ValueError(
            "OPENAI_API_KEY not configured. "
            "Please set your OpenAI API key in backend/.env"
        )

    # Create function tools from MCP tools
    tools = [
        # Tool 1: add_task
        FunctionTool(
            name="add_task",
            description="Create a new todo task with a title and optional description",
            params_json_schema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title (1-200 characters)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description",
                    },
                },
                "required": ["title"],
            },
            on_invoke_tool=lambda ctx, params_json: _invoke_add_task(params_json),
        ),

        # Tool 2: list_tasks
        FunctionTool(
            name="list_tasks",
            description="Retrieve user's tasks with optional filtering by completion status, category, or task status, and optional sorting",
            params_json_schema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "string",
                        "enum": ["all", "pending", "completed", "today"],
                        "description": "Filter by completion status or date: 'all', 'pending', 'completed', or 'today' (default: 'all')",
                    },
                    "category": {
                        "type": "string",
                        "enum": ["personal", "work", "study", "health", "shopping", "other"],
                        "description": "Filter by category (optional)",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed"],
                        "description": "Filter by task status (optional)",
                    },
                    "sort_by": {
                        "type": "string",
                        "enum": ["date", "priority", "status", "recent"],
                        "description": "Sort order: 'date' (due date), 'priority' (high to low), 'status' (pending first), or 'recent' (most recent first)",
                    },
                },
                "required": [],  # All parameters are optional
            },
            on_invoke_tool=lambda ctx, params_json: _invoke_list_tasks(params_json),
        ),

        # Tool 3: complete_task
        FunctionTool(
            name="complete_task",
            description="Mark a task as complete by its ID",
            params_json_schema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to mark as complete",
                    },
                },
                "required": ["task_id"],
            },
            on_invoke_tool=lambda ctx, params_json: _invoke_complete_task(params_json),
        ),

        # Tool 4: delete_task
        FunctionTool(
            name="delete_task",
            description="Delete a task from the list by its ID",
            params_json_schema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to delete",
                    },
                },
                "required": ["task_id"],
            },
            on_invoke_tool=lambda ctx, params_json: _invoke_delete_task(params_json),
        ),

        # Tool 5: update_task
        FunctionTool(
            name="update_task",
            description="Modify task title, description, or completion status. At least one field (title, description, or completed) must be provided along with task_id.",
            params_json_schema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to update",
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (1-200 characters, optional)",
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description (optional, can be null to clear)",
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "New completion status (true/false, optional)",
                    },
                },
                "required": ["task_id"],  # Only task_id is required; title, description, completed are optional
            },
            on_invoke_tool=lambda ctx, params_json: _invoke_update_task(params_json),
        ),
    ]

    # Create agent with tools and instructions
    agent = Agent(
        name="todo_assistant",
        instructions=AGENT_INSTRUCTIONS,
        tools=tools,
        model=settings.OPENAI_MODEL,
    )

    return agent


# Global context storage for current request
# This will be set by the chat endpoint before calling the agent
_current_context: Dict[str, Any] = {}


def set_tool_context(user_id: str, session: Session) -> None:
    """
    Set the context for tool execution.

    This must be called before invoking the agent to ensure tools
    have access to the authenticated user and database session.

    Args:
        user_id: Authenticated user ID from JWT token
        session: Database session from FastAPI dependency

    Security Note:
        This context is request-scoped and must be set for each
        chat request to ensure proper user isolation.
    """
    global _current_context
    _current_context = {
        "user_id": user_id,
        "session": session
    }


def clear_tool_context() -> None:
    """
    Clear the tool execution context.

    Should be called after agent execution completes to prevent
    context leakage between requests.
    """
    global _current_context
    _current_context = {}


# Tool invocation wrapper functions
# These inject user_id and session from the request context

async def _invoke_add_task(params_json: str) -> Dict[str, Any]:
    """
    Invoke add_task tool with context injection.

    Args:
        params_json: JSON string with tool parameters from OpenAI

    Returns:
        Tool execution result
    """
    params = json.loads(params_json)

    # Inject context from current request
    result = await inject_context_into_tool_call(
        tool_func=add_task,
        params={
            "title": params.get("title"),
            "description": params.get("description")
        },
        user_id=_current_context.get("user_id"),
        session=_current_context.get("session")
    )
    return result


async def _invoke_list_tasks(params_json: str) -> Dict[str, Any]:
    """
    Invoke list_tasks tool with context injection.

    Args:
        params_json: JSON string with tool parameters from OpenAI

    Returns:
        Tool execution result
    """
    params = json.loads(params_json)

    result = await inject_context_into_tool_call(
        tool_func=list_tasks,
        params={
            "filter": params.get("filter", "all"),
            "category": params.get("category"),
            "status": params.get("status"),
            "sort_by": params.get("sort_by")
        },
        user_id=_current_context.get("user_id"),
        session=_current_context.get("session")
    )
    return result


async def _invoke_complete_task(params_json: str) -> Dict[str, Any]:
    """
    Invoke complete_task tool with context injection.

    Args:
        params_json: JSON string with tool parameters from OpenAI

    Returns:
        Tool execution result
    """
    params = json.loads(params_json)

    result = await inject_context_into_tool_call(
        tool_func=complete_task,
        params={"task_id": params.get("task_id")},
        user_id=_current_context.get("user_id"),
        session=_current_context.get("session")
    )
    return result


async def _invoke_delete_task(params_json: str) -> Dict[str, Any]:
    """
    Invoke delete_task tool with context injection.

    Args:
        params_json: JSON string with tool parameters from OpenAI

    Returns:
        Tool execution result
    """
    params = json.loads(params_json)

    result = await inject_context_into_tool_call(
        tool_func=delete_task,
        params={"task_id": params.get("task_id")},
        user_id=_current_context.get("user_id"),
        session=_current_context.get("session")
    )
    return result


async def _invoke_update_task(params_json: str) -> Dict[str, Any]:
    """
    Invoke update_task tool with context injection.

    Args:
        params_json: JSON string with tool parameters from OpenAI

    Returns:
        Tool execution result
    """
    params = json.loads(params_json)

    result = await inject_context_into_tool_call(
        tool_func=update_task,
        params={
            "task_id": params.get("task_id"),
            "title": params.get("title"),
            "description": params.get("description"),
            "completed": params.get("completed")
        },
        user_id=_current_context.get("user_id"),
        session=_current_context.get("session")
    )
    return result
