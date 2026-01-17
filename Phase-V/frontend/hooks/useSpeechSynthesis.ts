/**
 * useSpeechSynthesis Hook
 * Wraps the Web Speech API SpeechSynthesis for text-to-speech functionality
 */

'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import type { VoicePlaybackState } from '@/lib/voice/types';

interface UseSpeechSynthesisOptions {
  voice?: SpeechSynthesisVoice | null;
  language?: string;
  rate?: number;
  pitch?: number;
  volume?: number;
  onStart?: () => void;
  onEnd?: () => void;
  onPause?: () => void;
  onResume?: () => void;
  onBoundary?: (charIndex: number) => void;
  onError?: (error: string) => void;
}

interface UseSpeechSynthesisReturn {
  speak: (text: string) => void;
  pause: () => void;
  resume: () => void;
  cancel: () => void;
  isSpeaking: boolean;
  isPaused: boolean;
  state: VoicePlaybackState;
  availableVoices: SpeechSynthesisVoice[];
  isSupported: boolean;
  currentCharIndex: number;
}

export function useSpeechSynthesis(
  options: UseSpeechSynthesisOptions = {}
): UseSpeechSynthesisReturn {
  const {
    voice = null,
    language = 'en-US',
    rate = 1.0,
    pitch = 1.0,
    volume = 1.0,
    onStart,
    onEnd,
    onPause,
    onResume,
    onBoundary,
    onError,
  } = options;

  const [state, setState] = useState<VoicePlaybackState>('idle');
  const [availableVoices, setAvailableVoices] = useState<SpeechSynthesisVoice[]>([]);
  const [isSupported, setIsSupported] = useState(false);
  const [currentCharIndex, setCurrentCharIndex] = useState(0);

  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);

  // Check for browser support and load voices
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const supported = 'speechSynthesis' in window;
    setIsSupported(supported);

    if (!supported) return;

    synthRef.current = window.speechSynthesis;

    // Load available voices
    const loadVoices = () => {
      const voices = synthRef.current?.getVoices() || [];
      setAvailableVoices(voices);
    };

    // Voices may load asynchronously (especially in Chrome)
    loadVoices();

    if (synthRef.current.onvoiceschanged !== undefined) {
      synthRef.current.onvoiceschanged = loadVoices;
    }

    // Cleanup on unmount
    return () => {
      if (synthRef.current?.speaking) {
        synthRef.current.cancel();
      }
    };
  }, []);

  const speak = useCallback(
    (text: string) => {
      if (!synthRef.current || !text) return;

      // Cancel any ongoing speech
      synthRef.current.cancel();

      const utterance = new SpeechSynthesisUtterance(text);

      // Apply settings
      if (voice) {
        utterance.voice = voice;
      } else if (availableVoices.length > 0) {
        // Find voice matching the selected language
        const langCode = language.split('-')[0].toLowerCase();
        const defaultVoice =
          availableVoices.find(
            (v) => v.lang.toLowerCase().startsWith(langCode) && v.default
          ) ||
          availableVoices.find((v) => v.lang.toLowerCase().startsWith(langCode)) ||
          availableVoices.find((v) => v.lang.toLowerCase() === language.toLowerCase()) ||
          availableVoices[0];
        if (defaultVoice) {
          utterance.voice = defaultVoice;
        }
      }

      // Set language on utterance for better TTS matching
      utterance.lang = language;

      utterance.rate = Math.max(0.5, Math.min(2, rate));
      utterance.pitch = Math.max(0.5, Math.min(2, pitch));
      utterance.volume = Math.max(0, Math.min(1, volume));

      // Event handlers
      utterance.onstart = () => {
        setState('speaking');
        setCurrentCharIndex(0);
        onStart?.();
      };

      utterance.onend = () => {
        setState('idle');
        setCurrentCharIndex(0);
        utteranceRef.current = null;
        onEnd?.();
      };

      utterance.onpause = () => {
        setState('paused');
        onPause?.();
      };

      utterance.onresume = () => {
        setState('speaking');
        onResume?.();
      };

      utterance.onboundary = (event) => {
        setCurrentCharIndex(event.charIndex);
        onBoundary?.(event.charIndex);
      };

      utterance.onerror = (event) => {
        // Don't treat 'interrupted' as an error (happens on cancel)
        if (event.error !== 'interrupted') {
          setState('idle');
          onError?.(`Speech synthesis error: ${event.error}`);
        }
        utteranceRef.current = null;
      };

      utteranceRef.current = utterance;
      setState('loading');

      // Start speaking
      synthRef.current.speak(utterance);
    },
    [voice, language, rate, pitch, volume, availableVoices, onStart, onEnd, onPause, onResume, onBoundary, onError]
  );

  const pause = useCallback(() => {
    if (synthRef.current?.speaking && !synthRef.current.paused) {
      synthRef.current.pause();
    }
  }, []);

  const resume = useCallback(() => {
    if (synthRef.current?.paused) {
      synthRef.current.resume();
    }
  }, []);

  const cancel = useCallback(() => {
    if (synthRef.current) {
      synthRef.current.cancel();
      setState('idle');
      setCurrentCharIndex(0);
      utteranceRef.current = null;
    }
  }, []);

  return {
    speak,
    pause,
    resume,
    cancel,
    isSpeaking: state === 'speaking',
    isPaused: state === 'paused',
    state,
    availableVoices,
    isSupported,
    currentCharIndex,
  };
}

export default useSpeechSynthesis;
