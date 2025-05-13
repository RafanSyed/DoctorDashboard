import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, Button } from 'react-native';

import Voice, {
  SpeechResultsEvent,
  SpeechErrorEvent,
} from 'react-native-voice';

export default function App() {
  const [isListening, setIsListening] = useState(false);
  const [results, setResults] = useState<string[]>([]);

  // Handler for successful speech results
  const onSpeechResults = (event: SpeechResultsEvent) => {
    if (event.value) {
      setResults(event.value);
    }
  };

  // Handler for speech recognition errors
  const onSpeechError = (event: SpeechErrorEvent) => {
    console.error('Speech recognition error:', event.error);
  };

  // Set up event listeners once when the component mounts
  useEffect(() => {
    Voice.onSpeechResults = onSpeechResults;
    Voice.onSpeechError = onSpeechError;

    // Cleanup listeners on unmount
    return () => {
      Voice.destroy().then(Voice.removeAllListeners);
    };
  }, []);

  // Start the voice recognition session
  const startListening = async () => {
    try {
      setResults([]);
      setIsListening(true);
      await Voice.start('en-US'); // You can change the language code as needed
    } catch (error) {
      console.error('Error starting voice recognition:', error);
    }
  };

  // Stop the voice recognition session
  const stopListening = async () => {
    try {
      setIsListening(false);
      await Voice.stop();
    } catch (error) {
      console.error('Error stopping voice recognition:', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Voice Recognition Test</Text>
      <Button
        title={isListening ? 'Stop Listening' : 'Start Listening'}
        onPress={isListening ? stopListening : startListening}
      />
      <Text style={styles.subtitle}>Results:</Text>
      {results.map((result, index) => (
        <Text key={index} style={styles.resultText}>
          {result}
        </Text>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 20, marginBottom: 20 },
  subtitle: { fontSize: 16, marginTop: 20 },
  resultText: { fontSize: 14, marginTop: 10 },
});
