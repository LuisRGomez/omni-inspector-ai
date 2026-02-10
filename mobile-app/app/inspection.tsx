import { View, Text, StyleSheet, TouchableOpacity, TextInput, ScrollView } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { useState } from 'react';

export default function InspectionScreen() {
  const router = useRouter();
  const { module } = useLocalSearchParams();
  const [containerNumber, setContainerNumber] = useState('');
  const [sealNumber, setSealNumber] = useState('');
  const [location, setLocation] = useState('');

  const getModuleInfo = () => {
    switch (module) {
      case 'underwriting':
        return {
          title: 'Alta de Riesgo',
          icon: '🛡️',
          color: '#4CAF50',
        };
      case 'claims':
        return {
          title: 'Siniestros',
          icon: '📋',
          color: '#2196F3',
        };
      case 'legal':
        return {
          title: 'Recupero Legal',
          icon: '⚖️',
          color: '#FF9800',
        };
      default:
        return {
          title: 'Inspección',
          icon: '📸',
          color: '#666',
        };
    }
  };

  const moduleInfo = getModuleInfo();

  const handleStartInspection = () => {
    router.push({
      pathname: '/camera',
      params: {
        module,
        containerNumber,
        sealNumber,
        location,
      },
    });
  };

  return (
    <ScrollView style={styles.container}>
      <View style={[styles.header, { backgroundColor: moduleInfo.color }]}>
        <Text style={styles.icon}>{moduleInfo.icon}</Text>
        <Text style={styles.title}>{moduleInfo.title}</Text>
      </View>

      <View style={styles.form}>
        <Text style={styles.label}>Número de Contenedor</Text>
        <TextInput
          style={styles.input}
          placeholder="Ej: TCLU1234567"
          value={containerNumber}
          onChangeText={setContainerNumber}
          autoCapitalize="characters"
        />

        <Text style={styles.label}>Número de Precinto</Text>
        <TextInput
          style={styles.input}
          placeholder="Ej: 123456"
          value={sealNumber}
          onChangeText={setSealNumber}
        />

        <Text style={styles.label}>Ubicación</Text>
        <TextInput
          style={styles.input}
          placeholder="Ej: Puerto de Buenos Aires"
          value={location}
          onChangeText={setLocation}
        />

        <TouchableOpacity
          style={[styles.button, { backgroundColor: moduleInfo.color }]}
          onPress={handleStartInspection}
        >
          <Text style={styles.buttonText}>📸 Iniciar Captura</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.instructions}>
        <Text style={styles.instructionsTitle}>Instrucciones:</Text>
        <Text style={styles.instructionItem}>• Capture fotos de todos los ángulos</Text>
        <Text style={styles.instructionItem}>• Enfoque en daños visibles</Text>
        <Text style={styles.instructionItem}>• Capture placas CSC y números de contenedor</Text>
        <Text style={styles.instructionItem}>• Asegure buena iluminación</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 30,
    alignItems: 'center',
  },
  icon: {
    fontSize: 64,
    marginBottom: 12,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
  },
  form: {
    padding: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
    color: '#333',
  },
  input: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    fontSize: 16,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  button: {
    borderRadius: 8,
    padding: 18,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  instructions: {
    padding: 20,
    backgroundColor: '#fff',
    margin: 20,
    borderRadius: 8,
  },
  instructionsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 12,
    color: '#333',
  },
  instructionItem: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    lineHeight: 20,
  },
});
