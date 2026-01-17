"""
Chat API Routes
Handles chat message endpoints for AI assistant interaction
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict, List
from datetime import datetime, timezone
import uuid
import logging

from app.database import get_session
from app.models import Conversation, Message
from app.schemas.message import MessageCreate, ChatResponse, MessageResponse
from app.schemas.conversation import ConversationResponse
from app.middleware.auth import get_current_user
from app.middleware.rate_limit import rate_limit_check
from app.mcp_server.agent import set_tool_context, clear_tool_context, create_todo_agent

# Configure logger
logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def send_chat_message(
    user_id: str,
    message_data: MessageCreate,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Send a chat message and get AI assistant response.

    This endpoint processes user messages with the AI assistant, which can
    invoke MCP tools to manage tasks. The conversation is stateful and
    persisted in the database.

    Args:
        user_id: User ID from path (must match authenticated user)
        message_data: Message content with optional conversation_id
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        ChatResponse: Contains AI response, conversation_id, and tool_calls

    Raises:
        HTTPException 401: Invalid or missing authentication
        HTTPException 403: User ID mismatch (not authorized)
        HTTPException 404: Conversation not found
        HTTPException 500: Internal server error (AI processing failure)

    Example:
        POST /api/user123/chat
        {
            "message": "Add a task to buy groceries"
        }

        Response:
        {
            "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
            "response": "I've added 'Buy groceries' to your tasks.",
            "tool_calls": [
                {
                    "tool": "add_task",
                    "arguments": {"title": "Buy groceries"},
                    "result": {"success": true, "task_id": 42}
                }
            ],
            "created_at": "2026-01-04T10:30:00Z"
        }
    """
    try:
        # Security: Validate user_id matches JWT token
        if current_user["user_id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. User ID does not match authenticated user"
            )

        # Rate limiting: Check if user has exceeded rate limit (30 req/min)
        rate_limit_check(user_id)

        # Get or create conversation
        conversation = None
        if message_data.conversation_id:
            # Load existing conversation
            conversation = session.get(Conversation, message_data.conversation_id)

            # Error: Conversation not found
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conversation with id {message_data.conversation_id} not found"
                )

            # Security: Verify conversation belongs to user
            if conversation.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied. This conversation belongs to another user"
                )
        else:
            # Create new conversation
            conversation = Conversation(
                user_id=user_id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            session.add(conversation)
            session.flush()  # Get conversation.id without committing

        # Load conversation history (all previous messages)
        history_query = (
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.asc())  # Chronological order
        )
        history = session.exec(history_query).all()

        # Save user message to database
        user_message = Message(
            user_id=user_id,
            conversation_id=conversation.id,
            role="user",
            content=message_data.message,
            created_at=datetime.now(timezone.utc)
        )
        session.add(user_message)
        session.flush()  # Save message before processing with AI

        # Set tool context for secure MCP tool execution
        set_tool_context(user_id=user_id, session=session)

        try:
            # Process message with AI agent (Gemini)
            from app.routes.chat_gemini import process_message_with_gemini_agent
            agent_response = await process_message_with_gemini_agent(
                message=message_data.message,
                history=history,
                user_id=user_id,
                session=session
            )

            # Save assistant response to database
            assistant_message = Message(
                user_id=user_id,
                conversation_id=conversation.id,
                role="assistant",
                content=agent_response["response"],
                created_at=datetime.now(timezone.utc)
            )
            session.add(assistant_message)

            # Update conversation timestamp
            conversation.updated_at = datetime.now(timezone.utc)
            session.add(conversation)

            # Commit all changes
            session.commit()

            # Return chat response
            return ChatResponse(
                conversation_id=conversation.id,
                response=agent_response["response"],
                tool_calls=agent_response.get("tool_calls", []),
                created_at=assistant_message.created_at
            )

        finally:
            # Security: Always clear tool context after processing
            clear_tool_context()

    except HTTPException:
        # Re-raise HTTP exceptions (401, 403, 404, 429)
        raise

    except Exception as e:
        # Log detailed error server-side (includes stack trace)
        logger.error(
            f"Error processing chat message for user {user_id}: {str(e)}",
            exc_info=True,
            extra={
                "user_id": user_id,
                "conversation_id": message_data.conversation_id,
                "message_length": len(message_data.message)
            }
        )

        # Rollback database transaction on error
        session.rollback()

        # Return generic error to user (no sensitive info)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="I'm temporarily unavailable. Please try again in a moment."
        )


@router.get("/{user_id}/conversations", response_model=Dict)
async def list_conversations(
    user_id: str,
    limit: int = 20,
    offset: int = 0,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    List user's conversations with pagination.

    Retrieves all conversations for the authenticated user, ordered by
    most recently updated first. Supports pagination for large conversation lists.

    Args:
        user_id: User ID from path (must match authenticated user)
        limit: Maximum number of conversations to return (default: 20, max: 100)
        offset: Number of conversations to skip (default: 0)
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        Dict containing:
        - conversations: List of ConversationResponse objects
        - total: Total count of user's conversations
        - limit: Applied limit
        - offset: Applied offset

    Raises:
        HTTPException 401: Invalid or missing authentication
        HTTPException 403: User ID mismatch (not authorized)

    Example:
        GET /api/user123/conversations?limit=10&offset=0

        Response:
        {
            "conversations": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "created_at": "2026-01-05T10:00:00Z",
                    "updated_at": "2026-01-05T10:30:00Z"
                }
            ],
            "total": 1,
            "limit": 10,
            "offset": 0
        }
    """
    # Security: Validate user_id matches JWT token
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. User ID does not match authenticated user"
        )

    # Validate pagination parameters
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100"
        )

    if offset < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offset must be non-negative"
        )

    # Get total count of user's conversations
    count_query = select(Conversation).where(Conversation.user_id == user_id)
    total = len(session.exec(count_query).all())

    # Query conversations with pagination
    query = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())  # Most recent first
        .offset(offset)
        .limit(limit)
    )

    conversations = session.exec(query).all()

    # Convert to response schema
    conversation_responses = [
        ConversationResponse(
            id=conv.id,
            created_at=conv.created_at,
            updated_at=conv.updated_at
        )
        for conv in conversations
    ]

    return {
        "conversations": conversation_responses,
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.get("/{user_id}/conversations/{conversation_id}", response_model=Dict)
async def get_conversation_history(
    user_id: str,
    conversation_id: uuid.UUID,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get conversation history with all messages.

    Retrieves a specific conversation and all its messages in chronological order.
    Useful for loading conversation context in the frontend.

    Args:
        user_id: User ID from path (must match authenticated user)
        conversation_id: UUID of the conversation to retrieve
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        Dict containing:
        - conversation: ConversationResponse object
        - messages: List of MessageResponse objects (chronological order)

    Raises:
        HTTPException 401: Invalid or missing authentication
        HTTPException 403: User ID mismatch or conversation access denied
        HTTPException 404: Conversation not found

    Example:
        GET /api/user123/conversations/550e8400-e29b-41d4-a716-446655440000

        Response:
        {
            "conversation": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "created_at": "2026-01-05T10:00:00Z",
                "updated_at": "2026-01-05T10:30:00Z"
            },
            "messages": [
                {
                    "id": 1,
                    "role": "user",
                    "content": "Add a task to buy milk",
                    "created_at": "2026-01-05T10:00:00Z"
                },
                {
                    "id": 2,
                    "role": "assistant",
                    "content": "I've added 'Buy milk' to your tasks.",
                    "created_at": "2026-01-05T10:00:05Z"
                }
            ]
        }
    """
    # Security: Validate user_id matches JWT token
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. User ID does not match authenticated user"
        )

    # Get conversation
    conversation = session.get(Conversation, conversation_id)

    # Error: Conversation not found
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with id {conversation_id} not found"
        )

    # Security: Verify conversation belongs to user
    if conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This conversation belongs to another user"
        )

    # Get all messages in conversation (chronological order)
    messages_query = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())  # Chronological order
    )
    messages = session.exec(messages_query).all()

    # Convert to response schemas
    conversation_response = ConversationResponse(
        id=conversation.id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )

    message_responses = [
        MessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at
        )
        for msg in messages
    ]

    return {
        "conversation": conversation_response,
        "messages": message_responses
    }


@router.delete("/{user_id}/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    user_id: str,
    conversation_id: uuid.UUID,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a conversation and all its messages.

    Permanently removes a conversation and all associated messages from the database.
    This action cannot be undone. Messages are automatically deleted via CASCADE.

    Args:
        user_id: User ID from path (must match authenticated user)
        conversation_id: UUID of the conversation to delete
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        204 No Content on successful deletion

    Raises:
        HTTPException 401: Invalid or missing authentication
        HTTPException 403: User ID mismatch or conversation access denied
        HTTPException 404: Conversation not found

    Example:
        DELETE /api/user123/conversations/550e8400-e29b-41d4-a716-446655440000

        Response: 204 No Content
    """
    # Security: Validate user_id matches JWT token
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. User ID does not match authenticated user"
        )

    # Get conversation
    conversation = session.get(Conversation, conversation_id)

    # Error: Conversation not found
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with id {conversation_id} not found"
        )

    # Security: Verify conversation belongs to user
    if conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This conversation belongs to another user"
        )

    # Delete conversation (messages deleted automatically via CASCADE)
    session.delete(conversation)
    session.commit()

    # Return 204 No Content (no response body)
    return None


async def process_message_with_agent(
    message: str,
    history: list,
    user_id: str,
    session: Session
) -> Dict:
    """
    Process user message with OpenAI agent.

    This function formats the conversation history, calls the OpenAI agent
    with tools enabled, and returns the agent's response with tool call results.

    Implements exponential backoff retry logic for transient OpenAI API errors.

    Args:
        message: User's current message
        history: List of previous Message objects in conversation
        user_id: Authenticated user ID
        session: Database session

    Returns:
        Dict containing:
        - response (str): AI-generated natural language response
        - tool_calls (list): List of tool invocations with results

    Raises:
        HTTPException 503: OpenAI service unavailable (rate limit or API error)
        HTTPException 500: Other processing errors
    """
    from app.config import settings
    from openai import OpenAI, RateLimitError, APIError, APIConnectionError, APITimeoutError
    from app.utils.retry import retry_with_exponential_backoff
    import json

    # Initialize OpenAI client
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Format conversation history for OpenAI
    messages = []

    # Add system instructions
    from app.mcp_server.agent import AGENT_INSTRUCTIONS
    messages.append({
        "role": "system",
        "content": AGENT_INSTRUCTIONS
    })

    # Add conversation history (windowed to MAX_CONVERSATION_MESSAGES)
    max_messages = settings.MAX_CONVERSATION_MESSAGES
    recent_history = history[-max_messages:] if len(history) > max_messages else history

    for msg in recent_history:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    # Add current user message
    messages.append({
        "role": "user",
        "content": message
    })

    # Create tool definitions for OpenAI
    from app.mcp_server.agent import create_todo_agent
    agent = create_todo_agent()

    # Define retry-enabled OpenAI call
    @retry_with_exponential_backoff(
        max_retries=3,
        initial_delay=1.0,
        exponential_base=2.0,
        max_delay=10.0,
        exceptions=(RateLimitError, APIConnectionError, APITimeoutError)
    )
    def call_openai_with_retry():
        """Call OpenAI API with automatic retry on transient errors."""
        return client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            tools=[
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new todo task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Task title (1-200 characters)"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional task description"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve user's tasks with optional filtering",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filter": {
                                "type": "string",
                                "enum": ["all", "pending", "completed"],
                                "description": "Filter by status"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "ID of task to complete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "ID of task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update task details",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "ID of task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "New completion status"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ],
            tool_choice="auto"  # Let AI decide when to use tools
        )

    # Call OpenAI with error handling
    try:
        response = call_openai_with_retry()

    except RateLimitError as e:
        logger.error(f"OpenAI rate limit exceeded for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is currently busy. Please try again in a few seconds.",
            headers={"Retry-After": "5"}
        )

    except (APIConnectionError, APITimeoutError) as e:
        logger.error(f"OpenAI connection error for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to reach AI service. Please try again in a moment.",
            headers={"Retry-After": "3"}
        )

    except APIError as e:
        logger.error(f"OpenAI API error for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="I'm experiencing technical difficulties. Please try again later."
        )

    except Exception as e:
        logger.error(f"Unexpected error calling OpenAI for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="I'm temporarily unavailable. Please try again in a moment."
        )

    # Extract response
    assistant_message = response.choices[0].message
    response_text = assistant_message.content or ""

    # Process tool calls if any
    tool_calls_results = []
    if assistant_message.tool_calls:
        # Import tool functions
        from app.mcp_server.tools import (
            add_task,
            list_tasks,
            complete_task,
            delete_task,
            update_task
        )

        tool_map = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "complete_task": complete_task,
            "delete_task": delete_task,
            "update_task": update_task
        }

        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name

            try:
                arguments = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in tool call arguments: {str(e)}")
                tool_calls_results.append({
                    "tool": tool_name,
                    "arguments": {},
                    "result": {"success": False, "error": "Invalid tool arguments"}
                })
                continue

            # Execute tool with context injection
            if tool_name in tool_map:
                try:
                    tool_func = tool_map[tool_name]
                    result = tool_func(
                        **arguments,
                        user_id=user_id,
                        session=session
                    )

                    tool_calls_results.append({
                        "tool": tool_name,
                        "arguments": arguments,
                        "result": result
                    })

                    # If tool call succeeded, append confirmation to response
                    # This helps if the AI didn't generate a text response
                    if not response_text and result.get("success"):
                        response_text = f"Tool {tool_name} executed successfully."

                except Exception as e:
                    logger.error(f"Error executing tool {tool_name}: {str(e)}", exc_info=True)
                    tool_calls_results.append({
                        "tool": tool_name,
                        "arguments": arguments,
                        "result": {"success": False, "error": "Tool execution failed"}
                    })
            else:
                logger.warning(f"Unknown tool requested: {tool_name}")
                tool_calls_results.append({
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": {"success": False, "error": f"Unknown tool: {tool_name}"}
                })

    # Ensure we always have a response
    if not response_text:
        response_text = "I've processed your request."

    return {
        "response": response_text,
        "tool_calls": tool_calls_results
    }
