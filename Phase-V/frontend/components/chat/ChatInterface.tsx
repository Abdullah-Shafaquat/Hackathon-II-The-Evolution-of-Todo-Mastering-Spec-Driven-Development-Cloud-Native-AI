/**
 * ChatInterface Component
 * Main chat interface with message list, input, AI integration, and voice features
 */

'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import { sendMessage, getConversationHistory } from '@/lib/chat-api';
import type { Message, ChatResponse } from '@/lib/types/chat';
import { useVoice } from '@/contexts/VoiceContext';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import VoiceIndicator from './VoiceIndicator';
import VoiceSettingsModal from '@/components/voice/VoiceSettingsModal';
import VoicePlaybackControls from '@/components/voice/VoicePlaybackControls';

interface ChatInterfaceProps {
  conversationId?: string;
  onConversationIdChange?: (id: string) => void;
}

export default function ChatInterface({
  conversationId: externalConversationId,
  onConversationIdChange
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | undefined>(externalConversationId);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [showVoiceSettings, setShowVoiceSettings] = useState(false);

  // Voice context
  const { preferences, actions } = useVoice();
  const lastMessageIdRef = useRef<number | null>(null);

  /**
   * Load conversation history when conversation ID changes
   */
  useEffect(() => {
    if (externalConversationId && externalConversationId !== conversationId) {
      loadConversationHistory(externalConversationId);
    } else if (!externalConversationId && conversationId) {
      // External conversation was cleared, reset local state
      setConversationId(undefined);
      setMessages([]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [externalConversationId]);

  /**
   * Auto-speak new AI responses when enabled
   */
  useEffect(() => {
    if (!preferences.autoSpeak || !preferences.enabled) return;

    // Find the latest assistant message
    const lastMessage = messages[messages.length - 1];
    if (!lastMessage || lastMessage.role !== 'assistant') return;

    // Only speak if this is a new message we haven't spoken yet
    if (lastMessage.id !== lastMessageIdRef.current) {
      lastMessageIdRef.current = lastMessage.id;
      // Small delay to ensure UI is ready
      setTimeout(() => {
        actions.speak(lastMessage.content, lastMessage.id);
      }, 100);
    }
  }, [messages, preferences.autoSpeak, preferences.enabled, actions]);

  /**
   * Load conversation history from API
   */
  const loadConversationHistory = async (convId: string) => {
    try {
      setIsLoadingHistory(true);
      setError(null);
      const data = await getConversationHistory(convId);
      setMessages(data.messages);
      setConversationId(convId);
    } catch (err) {
      console.error('Failed to load conversation history:', err);
      setError(err instanceof Error ? err.message : 'Failed to load conversation');
    } finally {
      setIsLoadingHistory(false);
    }
  };

  /**
   * Handle sending a message to the AI assistant
   */
  const handleSendMessage = useCallback(async (content: string) => {
    // Create optimistic user message
    const optimisticUserMessage: Message = {
      id: Date.now(), // Temporary ID
      role: 'user',
      content,
      created_at: new Date().toISOString()
    };

    // Add user message to UI immediately (optimistic update)
    setMessages(prev => [...prev, optimisticUserMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Send message to API
      const response: ChatResponse = await sendMessage({
        conversation_id: conversationId,
        message: content
      });

      // Update conversation ID if this was a new conversation
      if (!conversationId) {
        setConversationId(response.conversation_id);
        // Notify parent of new conversation
        onConversationIdChange?.(response.conversation_id);
      }

      // Create assistant message from response
      const assistantMessage: Message = {
        id: Date.now() + 1, // Temporary ID
        role: 'assistant',
        content: response.response,
        created_at: response.created_at
      };

      // Add assistant response to messages
      setMessages(prev => [...prev, assistantMessage]);

      // Log tool calls for debugging
      if (response.tool_calls && response.tool_calls.length > 0) {
        console.log('AI executed tools:', response.tool_calls);
      }

    } catch (err) {
      console.error('Chat error:', err);

      // Remove optimistic user message on error
      setMessages(prev => prev.slice(0, -1));

      // Set error message
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);

      // Show error in UI as system message
      const errorSystemMessage: Message = {
        id: Date.now() + 2,
        role: 'assistant',
        content: `Error: ${errorMessage}. Please try again.`,
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorSystemMessage]);

    } finally {
      setIsLoading(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [conversationId]);

  /**
   * Handle clearing the conversation
   */
  const handleClearConversation = useCallback(() => {
    if (confirm('Clear this conversation? This will start a new chat session.')) {
      setMessages([]);
      setConversationId(undefined);
      setError(null);
      // Stop any ongoing speech
      actions.stopSpeech();
    }
  }, [actions]);

  return (
    <div className="h-full flex flex-col bg-gradient-to-br from-gray-900 to-black border-x border-gray-800">
      {/* Chat Header with Actions */}
      {messages.length > 0 && (
        <div className="border-b border-gray-800 px-4 py-3 flex items-center justify-between bg-gray-900/50">
          <div className="flex items-center gap-3">
            {/* Conversation indicator */}
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-xs text-gray-400">
                {messages.length} message{messages.length !== 1 ? 's' : ''}
              </span>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <button
              onClick={handleClearConversation}
              className="text-xs text-gray-400 hover:text-white px-3 py-1.5 rounded-lg hover:bg-gray-800 transition-colors flex items-center gap-1"
              title="Clear conversation"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              <span className="hidden sm:inline">Clear</span>
            </button>
          </div>
        </div>
      )}

      {/* Error Banner */}
      {error && (
        <div className="bg-red-900/20 border-b border-red-800 px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-sm text-red-400">{error}</span>
          </div>
          <button
            onClick={() => setError(null)}
            className="text-red-400 hover:text-red-300 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      )}

      {/* Messages */}
      {isLoadingHistory ? (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-gray-700 border-t-white rounded-full animate-spin mx-auto mb-3"></div>
            <p className="text-sm text-gray-400">Loading conversation...</p>
          </div>
        </div>
      ) : (
        <MessageList messages={messages} isLoading={isLoading} />
      )}

      {/* Voice Indicator (above input) */}
      <VoiceIndicator />

      {/* Input */}
      <MessageInput
        onSend={handleSendMessage}
        disabled={isLoading}
        onOpenVoiceSettings={() => setShowVoiceSettings(true)}
      />

      {/* Voice Settings Modal */}
      <VoiceSettingsModal
        isOpen={showVoiceSettings}
        onClose={() => setShowVoiceSettings(false)}
      />

      {/* Floating Playback Controls */}
      <VoicePlaybackControls />
    </div>
  );
}
