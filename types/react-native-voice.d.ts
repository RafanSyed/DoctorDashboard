// types/react-native-voice.d.ts
declare module 'react-native-voice' {
    // Define the type for speech results
    export interface SpeechResultsEvent {
      value?: string[];
    }
  
    // Define the type for speech error events
    export interface SpeechError {
      message: string;
    }
  
    export interface SpeechErrorEvent {
      error: SpeechError;
    }
  
    // Declare functions available in the module
    export function start(language: string): Promise<any>;
    export function stop(): Promise<any>;
    export function destroy(): Promise<any>;
    export function removeAllListeners(): void;
  
    // Declare event handler properties
    export let onSpeechResults: ((event: SpeechResultsEvent) => void) | null;
    export let onSpeechError: ((event: SpeechErrorEvent) => void) | null;
  }
  