/**
 * useVoicePreferences Hook
 * Persists voice settings to localStorage and provides access to preferences
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import type { VoicePreferences } from '@/lib/voice/types';
import { DEFAULT_VOICE_PREFERENCES } from '@/lib/voice/types';

const STORAGE_KEY = 'voice-preferences';

interface UseVoicePreferencesReturn {
  preferences: VoicePreferences;
  updatePreferences: (updates: Partial<VoicePreferences>) => void;
  resetPreferences: () => void;
  isLoaded: boolean;
}

export function useVoicePreferences(): UseVoicePreferencesReturn {
  const [preferences, setPreferences] = useState<VoicePreferences>(DEFAULT_VOICE_PREFERENCES);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load preferences from localStorage on mount
  useEffect(() => {
    if (typeof window === 'undefined') {
      setIsLoaded(true);
      return;
    }

    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as Partial<VoicePreferences>;
        // Merge with defaults to handle new properties added in updates
        setPreferences({
          ...DEFAULT_VOICE_PREFERENCES,
          ...parsed,
        });
      }
    } catch (err) {
      console.warn('Failed to load voice preferences:', err);
    }

    setIsLoaded(true);
  }, []);

  // Save preferences to localStorage whenever they change
  useEffect(() => {
    if (!isLoaded || typeof window === 'undefined') return;

    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(preferences));
    } catch (err) {
      console.warn('Failed to save voice preferences:', err);
    }
  }, [preferences, isLoaded]);

  const updatePreferences = useCallback((updates: Partial<VoicePreferences>) => {
    setPreferences((prev) => ({
      ...prev,
      ...updates,
    }));
  }, []);

  const resetPreferences = useCallback(() => {
    setPreferences(DEFAULT_VOICE_PREFERENCES);

    if (typeof window !== 'undefined') {
      try {
        localStorage.removeItem(STORAGE_KEY);
      } catch (err) {
        console.warn('Failed to clear voice preferences:', err);
      }
    }
  }, []);

  return {
    preferences,
    updatePreferences,
    resetPreferences,
    isLoaded,
  };
}

export default useVoicePreferences;
