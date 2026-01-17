/**
 * Chat Type Definitions
 * TypeScript interfaces matching backend Pydantic schemas
 */

/**
 * Conversation metadata
 * Matches backend ConversationResponse schema
 */
export interface Conversation {
  id: string;         // UUID
  created_at: string; // ISO 8601 timestamp
  updated_at: string; // ISO 8601 timestamp
}

/**
 * Individual chat message
 * Matches backend MessageResponse schema
 */
export interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: string; // ISO 8601 timestamp
}

/**
 * Request payload for chat API
 * Matches backend MessageCreate schema
 */
export interface ChatRequest {
  conversation_id?: string; // Optional UUID - creates new conversation if not provided
  message: string;          // User message (1-5000 characters)
}

/**
 * Tool execution result
 * Represents a single MCP tool call made by the AI agent
 */
export interface ToolCall {
  tool: string;                    // Tool name (e.g., "add_task", "list_tasks")
  arguments: Record<string, any>;  // Arguments passed to the tool
  result: {
    success: boolean;
    [key: string]: any;            // Tool-specific result data
  };
}

/**
 * Chat API response
 * Matches backend ChatResponse schema
 */
export interface ChatResponse {
  conversation_id: string;   // UUID of conversation (new or existing)
  response: string;          // AI-generated natural language response
  tool_calls: ToolCall[];    // List of tools invoked by AI agent
  created_at: string;        // ISO 8601 timestamp
}
