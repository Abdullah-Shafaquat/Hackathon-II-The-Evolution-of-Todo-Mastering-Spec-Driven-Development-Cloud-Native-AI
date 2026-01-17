/**
 * MessageInput Component
 * Message input with send button, voice input, and keyboard shortcuts
 */

'use client';

import { useState, KeyboardEvent, useRef, useEffect } from 'react';
import { useVoice } from '@/contexts/VoiceContext';
import VoiceButton from '@/components/voice/VoiceButton';

interface MessageInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  onOpenVoiceSettings?: () => void;
}

export default function MessageInput({ onSend, disabled = false, onOpenVoiceSettings }: MessageInputProps) {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Voice context
  const { state, actions, preferences } = useVoice();
  const { transcript, interimTranscript, recognitionState } = state;
  const isListening = recognitionState === 'listening';

  // Append voice transcript to message when it changes
  useEffect(() => {
    if (transcript) {
      setMessage((prev) => {
        // Add space if there's existing text and it doesn't end with space
        const separator = prev && !prev.endsWith(' ') ? ' ' : '';
        return prev + separator + transcript;
      });
      // Clear transcript after appending
      actions.clearTranscript();
    }
  }, [transcript, actions]);

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  const handleSend = () => {
    const trimmedMessage = message.trim();
    if (trimmedMessage && !disabled) {
      onSend(trimmedMessage);
      setMessage('');

      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Enter to send, Shift+Enter for newline
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const characterCount = message.length;
  const maxLength = 5000;
  const isNearLimit = characterCount > maxLength * 0.9;
  const isOverLimit = characterCount > maxLength;

  // Show interim transcript as placeholder hint
  const showInterimHint = isListening && interimTranscript && !message;

  return (
    <div className="border-t border-gray-800 bg-gradient-to-br from-gray-900 to-black p-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex gap-3 items-end">
          {/* Textarea */}
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={
                isListening
                  ? 'Listening... speak now'
                  : 'Type your message... (Enter to send, Shift+Enter for new line)'
              }
              disabled={disabled}
              maxLength={maxLength}
              rows={1}
              className={`
                w-full resize-none bg-gray-800 border rounded-xl px-4 py-3
                text-white placeholder-gray-500
                focus:outline-none focus:ring-2 focus:ring-white focus:border-transparent
                disabled:bg-gray-900 disabled:cursor-not-allowed
                transition-all duration-200 max-h-32 overflow-y-auto
                ${isListening ? 'border-red-500 ring-1 ring-red-500/30' : 'border-gray-700'}
              `}
              style={{ minHeight: '48px' }}
            />

            {/* Interim transcript hint */}
            {showInterimHint && (
              <div className="absolute left-4 top-3 text-gray-500 italic text-sm pointer-events-none">
                {interimTranscript}...
              </div>
            )}

            {/* Character counter */}
            {characterCount > 0 && (
              <div className={`absolute -top-6 right-0 text-xs ${
                isOverLimit ? 'text-red-500 font-bold' :
                isNearLimit ? 'text-yellow-500' :
                'text-gray-500'
              }`}>
                {characterCount}/{maxLength}
              </div>
            )}
          </div>

          {/* Voice Button */}
          {preferences.enabled && state.isSupported.recognition && (
            <VoiceButton
              size="md"
              disabled={disabled}
              className="shrink-0"
            />
          )}

          {/* Voice Settings Button - Always visible for accessibility */}
          {onOpenVoiceSettings && (
            <button
              type="button"
              onClick={onOpenVoiceSettings}
              className="w-10 h-10 bg-gray-800 text-gray-400 hover:text-white hover:bg-gray-700 rounded-xl flex items-center justify-center transition-all duration-200 shrink-0"
              title="Voice Settings"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          )}

          {/* Send Button */}
          <button
            onClick={handleSend}
            disabled={disabled || !message.trim() || isOverLimit}
            className="px-6 py-3 bg-gradient-to-br from-white to-gray-200 text-black rounded-xl hover:shadow-lg hover:shadow-white/20 disabled:from-gray-700 disabled:to-gray-800 disabled:text-gray-500 disabled:cursor-not-allowed disabled:shadow-none transition-all duration-200 font-bold text-sm flex items-center gap-2 min-w-[100px] justify-center shrink-0"
          >
            {disabled ? (
              <>
                <div className="w-4 h-4 border-2 border-gray-500 border-t-transparent rounded-full animate-spin"></div>
                <span className="hidden sm:inline">Sending</span>
              </>
            ) : (
              <>
                <span>Send</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </>
            )}
          </button>
        </div>

        {/* Help Text */}
        <div className="mt-2 text-xs text-gray-500 flex items-center gap-4 flex-wrap">
          <span className="flex items-center gap-1">
            <kbd className="px-2 py-0.5 bg-gray-800 border border-gray-700 rounded text-gray-400">Enter</kbd>
            to send
          </span>
          <span className="flex items-center gap-1">
            <kbd className="px-2 py-0.5 bg-gray-800 border border-gray-700 rounded text-gray-400">Shift</kbd>
            +
            <kbd className="px-2 py-0.5 bg-gray-800 border border-gray-700 rounded text-gray-400">Enter</kbd>
            for new line
          </span>
          {preferences.enabled && state.isSupported.recognition && (
            <span className="flex items-center gap-1 text-gray-400">
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
              </svg>
              Voice enabled
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
