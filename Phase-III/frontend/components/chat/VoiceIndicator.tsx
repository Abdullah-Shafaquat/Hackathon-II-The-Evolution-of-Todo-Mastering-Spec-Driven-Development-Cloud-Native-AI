/**
 * VoiceIndicator Component
 * Shows visual feedback when listening or speaking
 */

'use client';

import { useVoice } from '@/contexts/VoiceContext';
import type { VoiceIndicatorProps } from '@/lib/voice/types';

export default function VoiceIndicator({ className = '' }: VoiceIndicatorProps) {
  const { state, actions } = useVoice();
  const { recognitionState, interimTranscript, playbackState } = state;

  const isListening = recognitionState === 'listening';
  const isSpeaking = playbackState === 'speaking';
  const isPaused = playbackState === 'paused';

  // Don't show if nothing is happening
  if (!isListening && !isSpeaking && !isPaused) {
    return null;
  }

  return (
    <div
      className={`
        bg-gradient-to-r from-gray-800 to-gray-900
        border border-gray-700 rounded-xl
        px-4 py-3 mx-4 mb-2
        animate-fade-in
        ${className}
      `}
    >
      {/* Listening State */}
      {isListening && (
        <div className="flex items-center gap-3">
          {/* Animated microphone icon */}
          <div className="relative flex items-center justify-center w-8 h-8">
            <div className="absolute w-8 h-8 bg-red-500/20 rounded-full animate-ping" />
            <div className="relative w-6 h-6 bg-red-600 rounded-full flex items-center justify-center">
              <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
              </svg>
            </div>
          </div>

          <div className="flex-1">
            <div className="text-sm font-medium text-white flex items-center gap-2">
              Listening...
              <span className="flex gap-1">
                <span className="w-1.5 h-1.5 bg-red-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-1.5 h-1.5 bg-red-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-1.5 h-1.5 bg-red-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </span>
            </div>
            {interimTranscript && (
              <p className="text-xs text-gray-400 mt-1 italic truncate">
                &quot;{interimTranscript}&quot;
              </p>
            )}
          </div>

          {/* Stop button */}
          <button
            onClick={actions.stopListening}
            className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
            title="Stop listening"
          >
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <rect x="6" y="6" width="12" height="12" rx="2" />
            </svg>
          </button>
        </div>
      )}

      {/* Speaking State */}
      {(isSpeaking || isPaused) && (
        <div className="flex items-center gap-3">
          {/* Sound wave animation */}
          <div className="flex items-center justify-center w-8 h-8 gap-0.5">
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className={`
                  w-1 bg-blue-500 rounded-full
                  ${isSpeaking ? 'animate-voice-wave' : 'h-2'}
                `}
                style={{
                  animationDelay: `${i * 100}ms`,
                  height: isPaused ? '8px' : undefined,
                }}
              />
            ))}
          </div>

          <div className="flex-1">
            <div className="text-sm font-medium text-white">
              {isPaused ? 'Paused' : 'Speaking...'}
            </div>
          </div>

          {/* Playback controls */}
          <div className="flex items-center gap-1">
            {/* Pause/Resume button */}
            <button
              onClick={isPaused ? actions.resumeSpeech : actions.pauseSpeech}
              className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
              title={isPaused ? 'Resume' : 'Pause'}
            >
              {isPaused ? (
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z" />
                </svg>
              ) : (
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
                </svg>
              )}
            </button>

            {/* Stop button */}
            <button
              onClick={actions.stopSpeech}
              className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
              title="Stop"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <rect x="6" y="6" width="12" height="12" rx="2" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
