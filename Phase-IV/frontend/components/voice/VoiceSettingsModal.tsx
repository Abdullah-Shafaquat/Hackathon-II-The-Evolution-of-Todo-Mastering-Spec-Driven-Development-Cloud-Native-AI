/**
 * VoiceSettingsModal Component
 * Settings modal for voice preferences
 */

'use client';

import { useState, useEffect, useMemo } from 'react';
import { createPortal } from 'react-dom';
import { useVoice } from '@/contexts/VoiceContext';
import { VOICE_LANGUAGES } from '@/lib/voice/types';
import type { VoiceSettingsModalProps } from '@/lib/voice/types';

export default function VoiceSettingsModal({ isOpen, onClose }: VoiceSettingsModalProps) {
  const { state, preferences, actions } = useVoice();
  const { availableVoices, isSupported } = state;
  const [mounted, setMounted] = useState(false);

  // Mount portal on client side only
  useEffect(() => {
    setMounted(true);
  }, []);

  // Handle escape key
  useEffect(() => {
    if (!isOpen) return;

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  // Filter voices by selected language
  const filteredVoices = useMemo(() => {
    const langCode = preferences.language.split('-')[0];
    return availableVoices.filter((voice) =>
      voice.lang.toLowerCase().startsWith(langCode.toLowerCase())
    );
  }, [availableVoices, preferences.language]);

  // Test voice
  const handleTestVoice = () => {
    actions.speak('Hello! This is a test of the voice settings.');
  };

  if (!isOpen || !mounted) return null;

  const modalContent = (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[9998]"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed inset-0 flex items-center justify-center z-[9999] p-4">
        <div
          className="bg-gradient-to-br from-gray-900 to-gray-800 border border-gray-700 rounded-2xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-hidden animate-in fade-in zoom-in-95 duration-200"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-700">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                  <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
                </svg>
              </div>
              <div>
                <h2 className="text-lg font-bold text-white">Voice Settings</h2>
                <p className="text-xs text-gray-400">Configure speech recognition and synthesis</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Content */}
          <div className="px-6 py-4 overflow-y-auto max-h-[calc(90vh-140px)] space-y-6">
            {/* Voice Enabled Toggle */}
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-white">Voice Features</label>
                <p className="text-xs text-gray-400">Enable voice input and output</p>
              </div>
              <button
                onClick={() => actions.updatePreferences({ enabled: !preferences.enabled })}
                className={`
                  relative w-12 h-6 rounded-full transition-colors duration-200
                  ${preferences.enabled ? 'bg-green-600' : 'bg-gray-600'}
                `}
              >
                <span
                  className={`
                    absolute top-1 w-4 h-4 bg-white rounded-full transition-transform duration-200
                    ${preferences.enabled ? 'translate-x-7' : 'translate-x-1'}
                  `}
                />
              </button>
            </div>

            {/* Browser Support Info */}
            {(!isSupported.recognition || !isSupported.synthesis) && (
              <div className="bg-yellow-900/20 border border-yellow-700 rounded-lg px-4 py-3">
                <div className="flex items-start gap-2">
                  <svg className="w-5 h-5 text-yellow-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  <div>
                    <p className="text-sm text-yellow-300 font-medium">Limited Support</p>
                    <p className="text-xs text-yellow-400 mt-1">
                      {!isSupported.recognition && 'Speech recognition not supported. '}
                      {!isSupported.synthesis && 'Speech synthesis not supported. '}
                      For best experience, use Chrome or Edge.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Language Selection - Always accessible */}
            <div>
              <label className="text-sm font-medium text-white block mb-2">Language</label>
              <select
                value={preferences.language}
                onChange={(e) => actions.updatePreferences({ language: e.target.value, voiceURI: null })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {VOICE_LANGUAGES.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Voice Selection - Always accessible */}
            <div>
              <label className="text-sm font-medium text-white block mb-2">Voice</label>
              <select
                value={preferences.voiceURI || ''}
                onChange={(e) => actions.updatePreferences({ voiceURI: e.target.value || null })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={filteredVoices.length === 0}
              >
                <option value="">Default</option>
                {filteredVoices.map((voice) => (
                  <option key={voice.voiceURI} value={voice.voiceURI}>
                    {voice.name} {voice.localService ? '(Local)' : '(Network)'}
                  </option>
                ))}
              </select>
              {filteredVoices.length === 0 && (
                <p className="text-xs text-gray-500 mt-1">No voices available for selected language</p>
              )}
            </div>

            {/* Auto-speak Toggle */}
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-white">Auto-speak Responses</label>
                <p className="text-xs text-gray-400">Automatically read AI responses aloud</p>
              </div>
              <button
                onClick={() => actions.updatePreferences({ autoSpeak: !preferences.autoSpeak })}
                disabled={!preferences.enabled}
                className={`
                  relative w-12 h-6 rounded-full transition-colors duration-200
                  ${!preferences.enabled ? 'opacity-50 cursor-not-allowed' : ''}
                  ${preferences.autoSpeak && preferences.enabled ? 'bg-green-600' : 'bg-gray-600'}
                `}
              >
                <span
                  className={`
                    absolute top-1 w-4 h-4 bg-white rounded-full transition-transform duration-200
                    ${preferences.autoSpeak ? 'translate-x-7' : 'translate-x-1'}
                  `}
                />
              </button>
            </div>

            {/* Speech Rate - Always accessible */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-medium text-white">Speech Rate</label>
                <span className="text-xs text-gray-400">{preferences.rate.toFixed(1)}x</span>
              </div>
              <input
                type="range"
                min="0.5"
                max="2"
                step="0.1"
                value={preferences.rate}
                onChange={(e) => actions.updatePreferences({ rate: parseFloat(e.target.value) })}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>Slow</span>
                <span>Normal</span>
                <span>Fast</span>
              </div>
            </div>

            {/* Pitch - Always accessible */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-medium text-white">Pitch</label>
                <span className="text-xs text-gray-400">{preferences.pitch.toFixed(1)}</span>
              </div>
              <input
                type="range"
                min="0.5"
                max="2"
                step="0.1"
                value={preferences.pitch}
                onChange={(e) => actions.updatePreferences({ pitch: parseFloat(e.target.value) })}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>Low</span>
                <span>Normal</span>
                <span>High</span>
              </div>
            </div>

            {/* Volume - Always accessible */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-medium text-white">Volume</label>
                <span className="text-xs text-gray-400">{Math.round(preferences.volume * 100)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={preferences.volume}
                onChange={(e) => actions.updatePreferences({ volume: parseFloat(e.target.value) })}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
            </div>

            {/* Test Voice Button */}
            <button
              onClick={handleTestVoice}
              disabled={!preferences.enabled || !isSupported.synthesis}
              className="w-full px-4 py-2.5 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-medium text-sm hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z" />
              </svg>
              Test Voice
            </button>
          </div>

          {/* Footer */}
          <div className="px-6 py-4 border-t border-gray-700 flex items-center justify-between">
            <button
              onClick={() => actions.resetPreferences()}
              className="text-sm text-gray-400 hover:text-white transition-colors"
            >
              Reset to Defaults
            </button>
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg text-sm font-medium transition-colors"
            >
              Done
            </button>
          </div>
        </div>
      </div>
    </>
  );

  return createPortal(modalContent, document.body);
}
