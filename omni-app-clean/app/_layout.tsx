import { Stack } from 'expo-router';
import { SafeAreaProvider } from 'react-native-safe-area-context';

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <Stack>
        <Stack.Screen name="index" options={{ title: 'Omni Inspector' }} />
        <Stack.Screen name="camera" options={{ title: 'Capturar Evidencia', headerShown: false }} />
        <Stack.Screen name="inspection" options={{ title: 'Nueva Inspección' }} />
        <Stack.Screen name="results" options={{ title: 'Resultados' }} />
      </Stack>
    </SafeAreaProvider>
  );
}
