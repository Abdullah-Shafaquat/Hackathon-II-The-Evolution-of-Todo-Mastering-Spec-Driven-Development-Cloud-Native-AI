/**
 * VoicePlaybackControls Component
 * Floating controls for speech playback (pause/resume/stop)
 */

'use client';

import { useVoice } from '@/contexts/VoiceContext';
import type { VoicePlaybackControlsProps } from '@/lib/voice/types';

export default function VoicePlaybackControls({ className = '' }: VoicePlaybackControlsProps) {
  const { state, actions } = useVoice();
  const { playbackState } = state;

  const isSpeaking = playbackState === 'speaking';
  const isPaused = playbackState === 'paused';

  // Don't show if not speaking or paused
  if (!isSpeaking && !isPaused) {
    return null;
  }

  return (
    <div
      className={`
        fixed bottom-24 right-4 z-50
        bg-gradient-to-br from-gray-800 to-gray-900
        border border-gray-700 rounded-xl
        shadow-xl shadow-black/30
        px-3 py-2
        flex items-center gap-2
        animate-fade-in
        ${className}
      `}
    >
      {/* Sound wave animation */}
      <div className="flex items-center justify-center gap-0.5 w-8">
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

      {/* Status text */}
      <span className="text-xs text-gray-400 min-w-[60px]">
        {isPaused ? 'Paused' : 'Speaking'}
      </span>

      {/* Pause/Resume button */}
      <button
        onClick={isPaused ? actions.resumeSpeech : actions.pauseSpeech}
        className="p-2 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
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
        className="p-2 text-gray-300 hover:text-red-400 hover:bg-red-900/20 rounded-lg transition-colors"
        title="Stop"
      >
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <rect x="6" y="6" width="12" height="12" rx="2" />
        </svg>
      </button>
    </div>
  );
}
