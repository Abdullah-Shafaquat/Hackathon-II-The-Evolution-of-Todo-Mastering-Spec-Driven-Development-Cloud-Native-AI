/**
 * Voice Feature Type Definitions
 * Types for speech recognition and synthesis functionality
 */

// Voice recognition states
export type VoiceRecognitionState =
  | 'idle'        // Not listening
  | 'listening'   // Actively listening for speech
  | 'processing'  // Processing speech input
  | 'error';      // Error occurred

// Voice playback states
export type VoicePlaybackState =
  | 'idle'        // Not speaking
  | 'speaking'    // Currently speaking
  | 'paused'      // Speech paused
  | 'loading';    // Loading voice

// Supported languages for speech recognition
export interface VoiceLanguage {
  code: string;
  name: string;
  flag?: string;
}

// Available languages
export const VOICE_LANGUAGES: VoiceLanguage[] = [
  { code: 'en-US', name: 'English (US)', flag: '🇺🇸' },
  { code: 'en-GB', name: 'English (UK)', flag: '🇬🇧' },
  { code: 'es-ES', name: 'Spanish (Spain)', flag: '🇪🇸' },
  { code: 'es-MX', name: 'Spanish (Mexico)', flag: '🇲🇽' },
  { code: 'fr-FR', name: 'French', flag: '🇫🇷' },
  { code: 'de-DE', name: 'German', flag: '🇩🇪' },
  { code: 'it-IT', name: 'Italian', flag: '🇮🇹' },
  { code: 'pt-BR', name: 'Portuguese (Brazil)', flag: '🇧🇷' },
  { code: 'zh-CN', name: 'Chinese (Simplified)', flag: '🇨🇳' },
  { code: 'ja-JP', name: 'Japanese', flag: '🇯🇵' },
  { code: 'ko-KR', name: 'Korean', flag: '🇰🇷' },
  { code: 'hi-IN', name: 'Hindi', flag: '🇮🇳' },
  { code: 'ar-SA', name: 'Arabic', flag: '🇸🇦' },
  { code: 'ru-RU', name: 'Russian', flag: '🇷🇺' },
];

// User preferences for voice features
export interface VoicePreferences {
  enabled: boolean;              // Master on/off toggle
  autoSpeak: boolean;            // Auto-speak AI responses
  language: string;              // Speech recognition language (e.g., 'en-US')
  voiceURI: string | null;       // Selected voice identifier for TTS
  rate: number;                  // Speech rate (0.5 - 2.0)
  pitch: number;                 // Voice pitch (0.5 - 2.0)
  volume: number;                // Volume (0 - 1)
}

// Default preferences
export const DEFAULT_VOICE_PREFERENCES: VoicePreferences = {
  enabled: true,
  autoSpeak: false,
  language: 'en-US',
  voiceURI: null,
  rate: 1.0,
  pitch: 1.0,
  volume: 1.0,
};

// Speech recognition error types
export type SpeechRecognitionErrorType =
  | 'no-speech'
  | 'audio-capture'
  | 'not-allowed'
  | 'network'
  | 'aborted'
  | 'service-not-allowed'
  | 'bad-grammar'
  | 'language-not-supported';

// Error messages for user display
export const SPEECH_ERROR_MESSAGES: Record<SpeechRecognitionErrorType, string> = {
  'no-speech': 'No speech detected. Please try again.',
  'audio-capture': 'Microphone not available. Please check your device.',
  'not-allowed': 'Microphone permission denied. Please enable it in your browser settings.',
  'network': 'Network error. Please check your connection.',
  'aborted': 'Speech recognition was cancelled.',
  'service-not-allowed': 'Speech recognition service not allowed.',
  'bad-grammar': 'Speech recognition grammar error.',
  'language-not-supported': 'Selected language is not supported.',
};

// Voice context state
export interface VoiceState {
  // Recognition state
  recognitionState: VoiceRecognitionState;
  transcript: string;
  interimTranscript: string;
  recognitionError: string | null;

  // Playback state
  playbackState: VoicePlaybackState;
  currentSpeakingMessageId: number | null;
  playbackError: string | null;

  // Available voices from browser
  availableVoices: SpeechSynthesisVoice[];

  // Feature support
  isSupported: {
    recognition: boolean;
    synthesis: boolean;
  };
}

// Voice context actions
export interface VoiceActions {
  // Recognition actions
  startListening: () => void;
  stopListening: () => void;
  clearTranscript: () => void;

  // Synthesis actions
  speak: (text: string, messageId?: number) => void;
  pauseSpeech: () => void;
  resumeSpeech: () => void;
  stopSpeech: () => void;

  // Settings actions
  updatePreferences: (prefs: Partial<VoicePreferences>) => void;
  resetPreferences: () => void;
}

// Complete voice context value
export interface VoiceContextValue {
  state: VoiceState;
  preferences: VoicePreferences;
  actions: VoiceActions;
}

// Props for voice button component
export interface VoiceButtonProps {
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  className?: string;
  showTooltip?: boolean;
}

// Props for voice settings modal
export interface VoiceSettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

// Props for voice playback controls
export interface VoicePlaybackControlsProps {
  className?: string;
}

// Props for voice indicator
export interface VoiceIndicatorProps {
  className?: string;
}
