"""
Tool Context Injection
Securely injects user_id and database session into MCP tool calls
"""

from typing import Dict, Any, Callable
from sqlmodel import Session
from functools import wraps


class ToolContext:
    """
    Context container for MCP tool execution.

    Holds authenticated user information and database session
    that must be injected into every tool call for security and data isolation.

    Attributes:
        user_id: Authenticated user ID from JWT token
        session: Database session for query execution
    """

    def __init__(self, user_id: str, session: Session):
        """
        Initialize tool context with authentication and database access.

        Args:
            user_id: Authenticated user ID (from JWT token)
            session: SQLModel database session

        Raises:
            ValueError: If user_id is None or empty
        """
        if not user_id:
            raise ValueError("user_id is required for tool context")

        self.user_id = user_id
        self.session = session

    def inject_into_tool(self, tool_func: Callable) -> Callable:
        """
        Create a wrapper that injects context into a tool function.

        This ensures user_id and session are automatically provided to every
        tool call, preventing tools from accessing data outside the user's scope.

        Args:
            tool_func: MCP tool function requiring user_id and session

        Returns:
            Wrapped function with context injected

        Security Note:
            user_id is NEVER accepted from tool parameters. It is always
            injected from authenticated request context to prevent privilege
            escalation attacks.
        """
        @wraps(tool_func)
        def wrapper(*args, **kwargs):
            # Inject context parameters
            # These override any user-provided values for security
            kwargs['user_id'] = self.user_id
            kwargs['session'] = self.session

            return tool_func(*args, **kwargs)

        return wrapper


def create_tool_context(user_id: str, session: Session) -> ToolContext:
    """
    Factory function to create a ToolContext instance.

    This is the primary way to create context for tool execution
    in API endpoints.

    Args:
        user_id: Authenticated user ID from request
        session: Database session from dependency injection

    Returns:
        ToolContext instance ready to inject into tools

    Raises:
        ValueError: If user_id is missing

    Example:
        >>> from app.database import get_session
        >>> from app.middleware.auth import get_current_user
        >>>
        >>> @router.post("/chat")
        >>> def chat(
        >>>     current_user: dict = Depends(get_current_user),
        >>>     session: Session = Depends(get_session)
        >>> ):
        >>>     context = create_tool_context(
        >>>         user_id=current_user["user_id"],
        >>>         session=session
        >>>     )
        >>>     # Use context to call tools safely
    """
    return ToolContext(user_id=user_id, session=session)


async def inject_context_into_tool_call(
    tool_func: Callable,
    params: Dict[str, Any],
    user_id: str,
    session: Session
) -> Dict[str, Any]:
    """
    Execute a tool function with injected context.

    This is a convenience function that creates context and executes
    the tool in one step. Use when you need to call individual tools
    rather than wrapping them.

    Args:
        tool_func: MCP tool function to execute
        params: Parameters to pass to the tool (from OpenAI agent)
        user_id: Authenticated user ID
        session: Database session

    Returns:
        Tool execution result dictionary

    Security:
        - user_id is injected, not accepted from params
        - If params contains 'user_id', it will be overridden
        - If params contains 'session', it will be overridden

    Example:
        >>> result = await inject_context_into_tool_call(
        >>>     tool_func=add_task,
        >>>     params={"title": "Buy milk"},
        >>>     user_id="user123",
        >>>     session=session
        >>> )
        >>> print(result)  # {"success": True, "task_id": 42, ...}
    """
    # Create context
    context = ToolContext(user_id=user_id, session=session)

    # Inject context and call tool
    wrapped_tool = context.inject_into_tool(tool_func)

    # Execute tool with parameters
    # Context (user_id, session) will be automatically injected
    result = wrapped_tool(**params)

    return result
