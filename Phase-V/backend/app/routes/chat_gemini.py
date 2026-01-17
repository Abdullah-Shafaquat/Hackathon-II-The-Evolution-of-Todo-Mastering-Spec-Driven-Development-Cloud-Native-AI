"""
Gemini-based Agent Processing
Replaces OpenAI with Google Gemini for chat functionality
"""

import json
import google.generativeai as genai
from typing import Dict, List
from app.config import settings
from app.models import Message
from sqlmodel import Session

# Configure Gemini
genai.configure(api_key="AIzaSyASfwmV2I4aKA-YF6ggmUfELxywTRG6u6k")


async def process_message_with_gemini_agent(
    message: str,
    history: List[Message],
    user_id: str,
    session: Session
) -> Dict:
    """
    Process user message with Gemini AI agent.

    Args:
        message: User's current message
        history: List of previous Message objects in conversation
        user_id: Authenticated user ID
        session: Database session

    Returns:
        Dict containing:
        - response (str): AI-generated natural language response
        - tool_calls (list): List of tool invocations with results
    """
    from app.mcp_server.agent import AGENT_INSTRUCTIONS

    # Define tool functions for Gemini
    tools = [
        genai.protos.Tool(
            function_declarations=[
                genai.protos.FunctionDeclaration(
                    name="add_task",
                    description="Create a new todo task for the user with optional due date, priority, and category",
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            "title": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="Task title (1-200 characters)"
                            ),
                            "description": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="Optional task description"
                            ),
                            "due_date": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="Optional due date. Can be 'today', 'tomorrow', or ISO format YYYY-MM-DD"
                            ),
                            "priority": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="Priority level: low, medium (default), or high",
                                enum=["low", "medium", "high"]
                            ),
                            "category": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="Task category: personal, work, study, health, shopping, or other (default)",
                                enum=["personal", "work", "study", "health", "shopping", "other"]
                            ),
                        },
                        required=["title"]
                    )
                ),
                genai.protos.FunctionDeclaration(
                    name="list_tasks",
                    description="Retrieve user's tasks with optional filtering by status, date, or category, and sorting by priority",
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            "filter": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="Filter by status or date: all (default), pending, completed, or today (tasks due today)",
                                enum=["all", "pending", "completed", "today"]
                            ),
                            "category": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="Filter by category: personal, work, study, health, shopping, or other",
                                enum=["personal", "work", "study", "health", "shopping", "other"]
                            ),
                            "sort_by_priority": genai.protos.Schema(
                                type=genai.protos.Type.BOOLEAN,
                                description="If true, sort tasks by priority (high first, then medium, then low)"
                            ),
                        },
                        required=[]
                    )
                ),
                genai.protos.FunctionDeclaration(
                    name="complete_task",
                    description="Mark a task as complete",
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            "task_id": genai.protos.Schema(
                                type=genai.protos.Type.INTEGER,
                                description="ID of task to complete"
                            ),
                        },
                        required=["task_id"]
                    )
                ),
                genai.protos.FunctionDeclaration(
                    name="delete_task",
                    description="Delete a task permanently. You can specify either the task ID or the task title. If using title, it will search for matching tasks.",
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            "task_id": genai.protos.Schema(
                                type=genai.protos.Type.INTEGER,
                                description="ID of task to delete (optional, use if you know the exact ID)"
                            ),
                            "title": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="Title of task to delete (optional, use if you don't know the ID)"
                            ),
                        },
                        required=[]
                    )
                ),
                genai.protos.FunctionDeclaration(
                    name="update_task",
                    description="Update task details (title, description, or completion status)",
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            "task_id": genai.protos.Schema(
                                type=genai.protos.Type.INTEGER,
                                description="ID of task to update"
                            ),
                            "title": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="New title"
                            ),
                            "description": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="New description"
                            ),
                            "completed": genai.protos.Schema(
                                type=genai.protos.Type.BOOLEAN,
                                description="New completion status"
                            ),
                        },
                        required=["task_id"]
                    )
                ),
            ]
        )
    ]

    # Use a compatible model - gemini-pro works best with function calling
    model = genai.GenerativeModel(
    model_name='models/gemini-2.5-flash',
    tools=tools,
    system_instruction=AGENT_INSTRUCTIONS
)
    # Format conversation history for Gemini
    chat_history = []

    # Add conversation history
    max_messages = settings.MAX_CONVERSATION_MESSAGES
    recent_history = history[-max_messages:] if len(history) > max_messages else history

    for msg in recent_history:
        chat_history.append({
            "role": "user" if msg.role == "user" else "model",
            "parts": [msg.content]
        })

    # Start chat session with history
    chat = model.start_chat(history=chat_history)

    # Send message and get response
    
    try:
        response = chat.send_message(message)
        
        # Check for function calls
        tool_calls_results = []
        response_text = ""

        # Process response to handle both text and function calls
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                # Check if this part is a function call
                if hasattr(part, 'function_call') and part.function_call:
                    function_call = part.function_call
                    tool_name = function_call.name
                    
                    # Convert arguments to proper dict
                    if hasattr(function_call, 'args'):
                        arguments = dict(function_call.args)
                    else:
                        arguments = {}
                    
                    # Execute tool
                    tool_result = execute_tool(
                        tool_name=tool_name,
                        arguments=arguments,
                        user_id=user_id,
                        session=session
                    )

                    tool_calls_results.append({
                        "tool": tool_name,
                        "arguments": arguments,
                        "result": tool_result
                    })
                    
                    # If we have tool results, send them back to Gemini for a final response
                    if tool_calls_results:
                        # Create a summary of tool results
                        tool_results_text = "Tool execution results:\n"
                        for tool_call in tool_calls_results:
                            tool_results_text += f"- {tool_call['tool']}: {json.dumps(tool_call['result'])}\n"
                        
                        # Get final response from Gemini with the tool results
                        final_response = chat.send_message(
                            f"Here are the results of the tools I executed:\n{tool_results_text}\n"
                            f"Please provide a helpful response to the user based on these results."
                        )
                        response_text = final_response.text
                else:
                    # This part is text
                    try:
                        if hasattr(part, 'text') and part.text:
                            response_text += part.text
                    except:
                        pass

        # If no response text was extracted, try to get it directly
        if not response_text:
            try:
              response = chat.send_message(message)
            except Exception as e:
                if "429" in str(e):
                   return {"response": "I'm receiving too many requests. Please wait a few seconds and try again.", "tool_calls": []}
                raise e
            try:
                response_text = response.text
            except:
                response_text = "I've processed your request."

        return {
            "response": response_text,
            "tool_calls": tool_calls_results
        }

    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        raise Exception(f"AI service error: {str(e)}")


def execute_tool(tool_name: str, arguments: dict, user_id: str, session: Session) -> dict:
    """Execute a tool function and return the result"""
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

    if tool_name not in tool_map:
        return {"success": False, "error": f"Unknown tool: {tool_name}"}

    try:
        # Prepare arguments for the tool function
        tool_args = arguments.copy()
        
        # Ensure user_id and session are passed
        tool_args['user_id'] = user_id
        tool_args['session'] = session
        
        # Call the tool function
        tool_func = tool_map[tool_name]
        result = tool_func(**tool_args)
        
        # Ensure result is serializable
        if isinstance(result, dict):
            return result
        else:
            return {"success": True, "result": str(result)}
            
    except Exception as e:
        import traceback
        print(f"Tool execution error for {tool_name}: {str(e)}")
        print(traceback.format_exc())
        return {"success": False, "error": str(e)}