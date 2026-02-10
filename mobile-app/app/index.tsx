import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';

export default function HomeScreen() {
  const router = useRouter();

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Omni Inspector AI</Text>
        <Text style={styles.subtitle}>Inspección Forense Inteligente</Text>
      </View>

      <View style={styles.modulesContainer}>
        {/* Module A: Risk Underwriting */}
        <TouchableOpacity 
          style={[styles.moduleCard, styles.moduleA]}
          onPress={() => router.push('/inspection?module=underwriting')}
        >
          <Text style={styles.moduleIcon}>🛡️</Text>
          <Text style={styles.moduleTitle}>Alta de Riesgo</Text>
          <Text style={styles.moduleDescription}>
            Pre-inspección para evitar asegurar mercadería dañada
          </Text>
        </TouchableOpacity>

        {/* Module B: Claims Processing */}
        <TouchableOpacity 
          style={[styles.moduleCard, styles.moduleB]}
          onPress={() => router.push('/inspection?module=claims')}
        >
          <Text style={styles.moduleIcon}>📋</Text>
          <Text style={styles.moduleTitle}>Siniestros</Text>
          <Text style={styles.moduleDescription}>
            Liquidación rápida de reclamos con detección de fraude
          </Text>
        </TouchableOpacity>

        {/* Module C: Legal Recovery */}
        <TouchableOpacity 
          style={[styles.moduleCard, styles.moduleC]}
          onPress={() => router.push('/inspection?module=legal')}
        >
          <Text style={styles.moduleIcon}>⚖️</Text>
          <Text style={styles.moduleTitle}>Recupero Legal</Text>
          <Text style={styles.moduleDescription}>
            Recolección de evidencia para demandas contra terceros
          </Text>
        </TouchableOpacity>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>Powered by AWS AI</Text>
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
    backgroundColor: '#1a1a2e',
    padding: 30,
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#aaa',
  },
  modulesContainer: {
    padding: 20,
  },
  moduleCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 24,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  moduleA: {
    borderLeftWidth: 4,
    borderLeftColor: '#4CAF50',
  },
  moduleB: {
    borderLeftWidth: 4,
    borderLeftColor: '#2196F3',
  },
  moduleC: {
    borderLeftWidth: 4,
    borderLeftColor: '#FF9800',
  },
  moduleIcon: {
    fontSize: 48,
    marginBottom: 12,
  },
  moduleTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#1a1a2e',
  },
  moduleDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  footer: {
    padding: 20,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
    color: '#999',
  },
});
