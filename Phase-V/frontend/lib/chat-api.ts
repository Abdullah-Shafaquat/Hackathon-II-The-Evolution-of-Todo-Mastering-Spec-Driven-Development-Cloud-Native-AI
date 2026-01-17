/**
 * Chat API Module
 * Dedicated exports for chat-related API operations
 *
 * This module provides a clean interface for chat operations,
 * wrapping the main API client with chat-specific methods.
 */

import api from './api';
import type {
  ChatRequest,
  ChatResponse,
  Conversation,
  Message
} from './types/chat';

/**
 * Send a message to the AI assistant
 *
 * @param request - Chat request with optional conversation_id and message
 * @returns Promise<ChatResponse> - AI response with tool calls
 * @throws Error if user not authenticated or API request fails
 *
 * @example
 * ```typescript
 * const response = await sendMessage({
 *   message: "Add a task to buy groceries"
 * });
 * console.log(response.response); // AI's text response
 * console.log(response.tool_calls); // Tools the AI invoked
 * ```
 */
export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  return api.sendMessage(request);
}

/**
 * Get all conversations for the authenticated user
 *
 * @param limit - Maximum number of conversations to return (default: 20)
 * @param offset - Number of conversations to skip (default: 0)
 * @returns Promise with conversations array and pagination info
 * @throws Error if user not authenticated
 *
 * @example
 * ```typescript
 * const { conversations, total } = await getConversations(10, 0);
 * console.log(`Showing ${conversations.length} of ${total} conversations`);
 * ```
 */
export async function getConversations(
  limit: number = 20,
  offset: number = 0
): Promise<{
  conversations: Conversation[];
  total: number;
  limit: number;
  offset: number;
}> {
  return api.getConversations(limit, offset);
}

/**
 * Get conversation history with all messages
 *
 * @param conversationId - UUID of the conversation
 * @returns Promise with conversation metadata and all messages
 * @throws Error if user not authenticated or conversation not found
 *
 * @example
 * ```typescript
 * const { conversation, messages } = await getConversationHistory(conversationId);
 * messages.forEach(msg => {
 *   console.log(`${msg.role}: ${msg.content}`);
 * });
 * ```
 */
export async function getConversationHistory(conversationId: string): Promise<{
  conversation: Conversation;
  messages: Message[];
}> {
  return api.getConversationHistory(conversationId);
}

/**
 * Delete a conversation and all its messages
 *
 * @param conversationId - UUID of the conversation to delete
 * @returns Promise<void>
 * @throws Error if user not authenticated or conversation not found
 *
 * @example
 * ```typescript
 * await deleteConversation(conversationId);
 * console.log('Conversation deleted successfully');
 * ```
 */
export async function deleteConversation(conversationId: string): Promise<void> {
  return api.deleteConversation(conversationId);
}

/**
 * Get the current authenticated user
 * Helper function to check authentication status
 *
 * @returns User object or null if not authenticated
 */
export function getCurrentUser() {
  return api.getUser();
}

/**
 * Check if user is authenticated
 *
 * @returns boolean indicating authentication status
 */
export function isAuthenticated(): boolean {
  return api.isAuthenticated();
}

// Export types for convenience
export type {
  ChatRequest,
  ChatResponse,
  Conversation,
  Message,
} from './types/chat';
