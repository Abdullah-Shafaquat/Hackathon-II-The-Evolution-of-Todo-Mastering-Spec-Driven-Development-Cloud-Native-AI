/**
 * VoiceButton Component
 * Microphone button for voice input with visual states
 */

'use client';

import { useVoice } from '@/contexts/VoiceContext';
import type { VoiceButtonProps } from '@/lib/voice/types';

export default function VoiceButton({
  size = 'md',
  disabled = false,
  className = '',
  showTooltip = true,
}: VoiceButtonProps) {
  const { state, preferences, actions } = useVoice();
  const { recognitionState } = state;
  const { isSupported } = state;

  const isListening = recognitionState === 'listening';
  const isProcessing = recognitionState === 'processing';
  const hasError = recognitionState === 'error';

  // Size classes
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12',
  };

  const iconSizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  };

  // Don't render if speech recognition is not supported
  if (!isSupported.recognition) {
    return null;
  }

  // Don't render if voice is disabled in preferences
  if (!preferences.enabled) {
    return null;
  }

  const handleClick = () => {
    if (disabled) return;

    if (isListening) {
      actions.stopListening();
    } else {
      actions.startListening();
    }
  };

  // Get button state styles
  const getButtonStyles = () => {
    if (disabled) {
      return 'bg-gray-800 text-gray-600 cursor-not-allowed';
    }

    if (isListening) {
      return 'bg-red-600 text-white hover:bg-red-700 shadow-lg shadow-red-600/30';
    }

    if (isProcessing) {
      return 'bg-yellow-600 text-white';
    }

    if (hasError) {
      return 'bg-red-900 text-red-400 hover:bg-red-800';
    }

    return 'bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-white';
  };

  // Get tooltip text
  const getTooltipText = () => {
    if (!isSupported.recognition) return 'Voice input not supported';
    if (disabled) return 'Voice input disabled';
    if (isListening) return 'Click to stop listening';
    if (isProcessing) return 'Processing...';
    if (hasError) return 'Error - click to retry';
    return 'Click to start voice input';
  };

  return (
    <div className="relative">
      <button
        type="button"
        onClick={handleClick}
        disabled={disabled || isProcessing}
        className={`
          ${sizeClasses[size]}
          ${getButtonStyles()}
          rounded-xl flex items-center justify-center
          transition-all duration-200
          focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-900
          ${className}
        `}
        title={showTooltip ? getTooltipText() : undefined}
        aria-label={isListening ? 'Stop voice input' : 'Start voice input'}
      >
        {/* Pulsing rings when listening */}
        {isListening && (
          <>
            <span className="absolute inset-0 rounded-xl bg-red-500 animate-ping opacity-25" />
            <span className="absolute inset-0 rounded-xl bg-red-500 animate-pulse opacity-40" />
          </>
        )}

        {/* Processing spinner */}
        {isProcessing ? (
          <div className={`${iconSizes[size]} border-2 border-white border-t-transparent rounded-full animate-spin`} />
        ) : (
          /* Microphone icon */
          <svg
            className={`${iconSizes[size]} relative z-10`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            {isListening ? (
              // Microphone with waves (listening)
              <>
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                />
              </>
            ) : (
              // Regular microphone
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
              />
            )}
          </svg>
        )}
      </button>
    </div>
  );
}
