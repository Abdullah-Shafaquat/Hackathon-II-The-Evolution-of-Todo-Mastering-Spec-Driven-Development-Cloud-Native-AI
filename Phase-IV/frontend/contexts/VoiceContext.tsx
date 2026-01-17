/**
 * VoiceContext Provider
 * Global voice state management for speech recognition and synthesis
 */

'use client';

import {
  createContext,
  useContext,
  useCallback,
  useMemo,
  useState,
  ReactNode,
} from 'react';
import { useSpeechRecognition } from '@/hooks/useSpeechRecognition';
import { useSpeechSynthesis } from '@/hooks/useSpeechSynthesis';
import { useVoicePreferences } from '@/hooks/useVoicePreferences';
import type {
  VoiceContextValue,
  VoiceState,
  VoicePreferences,
} from '@/lib/voice/types';
import { DEFAULT_VOICE_PREFERENCES } from '@/lib/voice/types';

// Create context with undefined default (will check for provider)
const VoiceContext = createContext<VoiceContextValue | undefined>(undefined);

interface VoiceProviderProps {
  children: ReactNode;
}

export function VoiceProvider({ children }: VoiceProviderProps) {
  const [currentSpeakingMessageId, setCurrentSpeakingMessageId] = useState<number | null>(null);

  // Load preferences
  const {
    preferences,
    updatePreferences,
    resetPreferences,
    isLoaded: preferencesLoaded,
  } = useVoicePreferences();

  // Find the selected voice from available voices
  const findSelectedVoice = useCallback(
    (voices: SpeechSynthesisVoice[]): SpeechSynthesisVoice | null => {
      if (!preferences.voiceURI) return null;
      return voices.find((v) => v.voiceURI === preferences.voiceURI) || null;
    },
    [preferences.voiceURI]
  );

  // Speech synthesis hook
  const {
    speak: synthSpeak,
    pause: synthPause,
    resume: synthResume,
    cancel: synthCancel,
    state: playbackState,
    availableVoices,
    isSupported: synthSupported,
  } = useSpeechSynthesis({
    language: preferences.language,
    rate: preferences.rate,
    pitch: preferences.pitch,
    volume: preferences.volume,
    onEnd: () => {
      setCurrentSpeakingMessageId(null);
    },
    onError: (error) => {
      console.error('Speech synthesis error:', error);
      setCurrentSpeakingMessageId(null);
    },
  });

  // Speech recognition hook
  const {
    state: recognitionState,
    transcript,
    interimTranscript,
    error: recognitionError,
    isSupported: recognitionSupported,
    startListening: recStartListening,
    stopListening: recStopListening,
    resetTranscript,
  } = useSpeechRecognition({
    language: preferences.language,
    continuous: true,
    interimResults: true,
  });

  // Actions
  const startListening = useCallback(() => {
    if (!preferences.enabled) return;
    recStartListening();
  }, [preferences.enabled, recStartListening]);

  const stopListening = useCallback(() => {
    recStopListening();
  }, [recStopListening]);

  const clearTranscript = useCallback(() => {
    resetTranscript();
  }, [resetTranscript]);

  const speak = useCallback(
    (text: string, messageId?: number) => {
      if (!preferences.enabled) return;

      // Find selected voice
      const selectedVoice = findSelectedVoice(availableVoices);

      // Create utterance with selected voice
      const utterance = new SpeechSynthesisUtterance(text);
      if (selectedVoice) {
        utterance.voice = selectedVoice;
      }
      utterance.rate = preferences.rate;
      utterance.pitch = preferences.pitch;
      utterance.volume = preferences.volume;

      // Cancel any ongoing speech first
      synthCancel();

      // Set message ID if provided
      if (messageId !== undefined) {
        setCurrentSpeakingMessageId(messageId);
      }

      // Speak the text
      synthSpeak(text);
    },
    [preferences, availableVoices, findSelectedVoice, synthSpeak, synthCancel]
  );

  const pauseSpeech = useCallback(() => {
    synthPause();
  }, [synthPause]);

  const resumeSpeech = useCallback(() => {
    synthResume();
  }, [synthResume]);

  const stopSpeech = useCallback(() => {
    synthCancel();
    setCurrentSpeakingMessageId(null);
  }, [synthCancel]);

  // Build state object
  const state: VoiceState = useMemo(
    () => ({
      recognitionState,
      transcript,
      interimTranscript,
      recognitionError,
      playbackState,
      currentSpeakingMessageId,
      playbackError: null,
      availableVoices,
      isSupported: {
        recognition: recognitionSupported,
        synthesis: synthSupported,
      },
    }),
    [
      recognitionState,
      transcript,
      interimTranscript,
      recognitionError,
      playbackState,
      currentSpeakingMessageId,
      availableVoices,
      recognitionSupported,
      synthSupported,
    ]
  );

  // Build context value
  const contextValue: VoiceContextValue = useMemo(
    () => ({
      state,
      preferences: preferencesLoaded ? preferences : DEFAULT_VOICE_PREFERENCES,
      actions: {
        startListening,
        stopListening,
        clearTranscript,
        speak,
        pauseSpeech,
        resumeSpeech,
        stopSpeech,
        updatePreferences,
        resetPreferences,
      },
    }),
    [
      state,
      preferences,
      preferencesLoaded,
      startListening,
      stopListening,
      clearTranscript,
      speak,
      pauseSpeech,
      resumeSpeech,
      stopSpeech,
      updatePreferences,
      resetPreferences,
    ]
  );

  return (
    <VoiceContext.Provider value={contextValue}>
      {children}
    </VoiceContext.Provider>
  );
}

// Custom hook to use voice context
export function useVoice(): VoiceContextValue {
  const context = useContext(VoiceContext);

  if (context === undefined) {
    throw new Error('useVoice must be used within a VoiceProvider');
  }

  return context;
}

// Export convenience hooks for specific functionality
export function useVoiceRecognitionState() {
  const { state } = useVoice();
  return {
    isListening: state.recognitionState === 'listening',
    state: state.recognitionState,
    transcript: state.transcript,
    interimTranscript: state.interimTranscript,
    error: state.recognitionError,
    isSupported: state.isSupported.recognition,
  };
}

export function useVoiceSynthesisState() {
  const { state } = useVoice();
  return {
    isSpeaking: state.playbackState === 'speaking',
    isPaused: state.playbackState === 'paused',
    state: state.playbackState,
    currentMessageId: state.currentSpeakingMessageId,
    error: state.playbackError,
    availableVoices: state.availableVoices,
    isSupported: state.isSupported.synthesis,
  };
}

export default VoiceContext;
