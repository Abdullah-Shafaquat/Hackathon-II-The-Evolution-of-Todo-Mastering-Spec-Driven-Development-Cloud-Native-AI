/**
 * MessageList Component
 * Displays chat message history with auto-scrolling and voice playback
 */

'use client';

import { useEffect, useRef } from 'react';
import type { Message } from '@/lib/types/chat';
import { useVoice } from '@/contexts/VoiceContext';

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
}

export default function MessageList({ messages, isLoading }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { state, preferences, actions } = useVoice();
  const { currentSpeakingMessageId, playbackState, isSupported } = state;

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle speak button click
  const handleSpeak = (message: Message) => {
    if (currentSpeakingMessageId === message.id) {
      // If already speaking this message, stop
      actions.stopSpeech();
    } else {
      // Speak the message
      actions.speak(message.content, message.id);
    }
  };

  // Check if a message is currently being spoken
  const isSpeakingMessage = (messageId: number) => {
    return currentSpeakingMessageId === messageId && (playbackState === 'speaking' || playbackState === 'paused');
  };

  // Empty state
  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center max-w-md">
          {/* Welcome Icon */}
          <div className="mb-6">
            <div className="w-16 h-16 mx-auto bg-gradient-to-br from-gray-700 to-gray-800 rounded-full flex items-center justify-center border-2 border-gray-600">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
          </div>

          {/* Welcome Message */}
          <h2 className="text-xl font-bold text-white mb-2">
            Welcome to Your AI Assistant
          </h2>
          <p className="text-gray-400 text-sm mb-4">
            Start a conversation by typing a message below
            {preferences.enabled && isSupported.recognition && ' or use voice input'}
          </p>

          {/* Example Messages */}
          <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-4 text-left">
            <p className="text-xs font-semibold text-gray-300 mb-3 uppercase tracking-wide">
              Try asking:
            </p>
            <div className="space-y-2">
              {[
                'Add a task to buy groceries',
                'Show me my pending tasks',
                'Mark task 1 as complete',
                'What tasks do I have today?'
              ].map((example, idx) => (
                <div key={idx} className="flex items-start gap-2 text-sm text-gray-400">
                  <span className="text-white mt-0.5">•</span>
                  <span className="italic">&quot;{example}&quot;</span>
                </div>
              ))}
            </div>
          </div>

          {/* Voice hint */}
          {preferences.enabled && isSupported.recognition && (
            <div className="mt-4 flex items-center justify-center gap-2 text-xs text-gray-500">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
              </svg>
              <span>Click the microphone to use voice input</span>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
        >
          <div
            className={`max-w-[80%] sm:max-w-[70%] rounded-2xl px-4 py-3 ${
              message.role === 'user'
                ? 'bg-gradient-to-br from-white to-gray-200 text-gray-900'
                : 'bg-gradient-to-br from-gray-800 to-gray-900 text-white border border-gray-700'
            } ${
              isSpeakingMessage(message.id) ? 'ring-2 ring-blue-500/50' : ''
            } shadow-lg`}
          >
            {/* Message Content */}
            <p className="whitespace-pre-wrap break-words text-sm leading-relaxed">
              {message.content}
            </p>

            {/* Footer: Timestamp and Speak Button */}
            <div className={`flex items-center justify-between gap-2 mt-2 ${
              message.role === 'user' ? 'text-gray-600' : 'text-gray-400'
            }`}>
              {/* Timestamp - Convert UTC to local time */}
              <span className="text-xs">
                {(() => {
                  const date = new Date(message.created_at);
                  // Ensure UTC string is parsed correctly
                  const utcDate = message.created_at.endsWith('Z') || message.created_at.includes('+')
                    ? date
                    : new Date(message.created_at + 'Z');
                  return utcDate.toLocaleTimeString([], {
                    hour: 'numeric',
                    minute: '2-digit',
                    hour12: true
                  });
                })()}
              </span>

              {/* Speak Button (only for assistant messages) */}
              {message.role === 'assistant' && preferences.enabled && isSupported.synthesis && (
                <button
                  onClick={() => handleSpeak(message)}
                  className={`
                    p-1.5 rounded-lg transition-all duration-200
                    ${isSpeakingMessage(message.id)
                      ? 'text-blue-400 bg-blue-900/30 hover:bg-blue-900/50'
                      : 'text-gray-400 hover:text-white hover:bg-gray-700/50'
                    }
                  `}
                  title={isSpeakingMessage(message.id) ? 'Stop speaking' : 'Read aloud'}
                >
                  {isSpeakingMessage(message.id) ? (
                    // Speaking indicator
                    <div className="flex items-center gap-0.5 w-4 h-4">
                      {[1, 2, 3].map((i) => (
                        <div
                          key={i}
                          className={`
                            w-0.5 bg-blue-400 rounded-full
                            ${playbackState === 'speaking' ? 'animate-voice-wave' : 'h-1'}
                          `}
                          style={{
                            animationDelay: `${i * 100}ms`,
                            height: playbackState === 'paused' ? '4px' : undefined,
                          }}
                        />
                      ))}
                    </div>
                  ) : (
                    // Speaker icon
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z" />
                    </svg>
                  )}
                </button>
              )}
            </div>
          </div>
        </div>
      ))}

      {/* Loading Indicator (Typing Animation) */}
      {isLoading && (
        <div className="flex justify-start animate-fade-in">
          <div className="bg-gradient-to-br from-gray-800 to-gray-900 border border-gray-700 rounded-2xl px-4 py-3 shadow-lg">
            <div className="flex space-x-2">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          </div>
        </div>
      )}

      {/* Scroll anchor */}
      <div ref={messagesEndRef} />
    </div>
  );
}
