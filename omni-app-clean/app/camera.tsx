import { useState, useRef, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, Alert } from 'react-native';
import { Camera, CameraType } from 'expo-camera';
import { useRouter, useLocalSearchParams } from 'expo-router';
import * as MediaLibrary from 'expo-media-library';

export default function CameraScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const [facing, setFacing] = useState<CameraType>(CameraType.back);
  const [permission, requestPermission] = Camera.useCameraPermissions();
  const [mediaPermission, requestMediaPermission] = MediaLibrary.usePermissions();
  const [photos, setPhotos] = useState<string[]>([]);
  const cameraRef = useRef<Camera>(null);

  useEffect(() => {
    if (!permission?.granted) {
      requestPermission();
    }
    if (!mediaPermission?.granted) {
      requestMediaPermission();
    }
  }, []);

  if (!permission) {
    return <View />;
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={styles.message}>Necesitamos permiso para usar la cámara</Text>
        <TouchableOpacity style={styles.button} onPress={requestPermission}>
          <Text style={styles.buttonText}>Otorgar Permiso</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const takePicture = async () => {
    if (cameraRef.current) {
      try {
        const photo = await cameraRef.current.takePictureAsync({
          quality: 1,
          base64: false,
        });
        
        if (photo) {
          setPhotos([...photos, photo.uri]);
          
          // Save to media library
          if (mediaPermission?.granted) {
            await MediaLibrary.saveToLibraryAsync(photo.uri);
          }
          
          Alert.alert('Foto Capturada', `Total: ${photos.length + 1} fotos`);
        }
      } catch (error) {
        console.error('Error taking picture:', error);
        Alert.alert('Error', 'No se pudo capturar la foto');
      }
    }
  };

  const finishInspection = () => {
    if (photos.length === 0) {
      Alert.alert('Sin Fotos', 'Debes capturar al menos una foto');
      return;
    }

    router.push({
      pathname: '/results',
      params: {
        ...params,
        photoCount: photos.length.toString(),
      },
    });
  };

  const toggleCameraFacing = () => {
    setFacing(current => (current === CameraType.back ? CameraType.front : CameraType.back));
  };

  return (
    <View style={styles.container}>
      <Camera style={styles.camera} type={facing} ref={cameraRef}>
        <View style={styles.overlay}>
          <View style={styles.topBar}>
            <TouchableOpacity
              style={styles.closeButton}
              onPress={() => router.back()}
            >
              <Text style={styles.closeButtonText}>✕</Text>
            </TouchableOpacity>
            <Text style={styles.photoCount}>📸 {photos.length} fotos</Text>
          </View>

          <View style={styles.bottomBar}>
            <TouchableOpacity
              style={styles.thumbnailContainer}
              onPress={() => {
                if (photos.length > 0) {
                  // Show gallery
                }
              }}
            >
              {photos.length > 0 && (
                <Image
                  source={{ uri: photos[photos.length - 1] }}
                  style={styles.thumbnail}
                />
              )}
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.captureButton}
              onPress={takePicture}
            >
              <View style={styles.captureButtonInner} />
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.flipButton}
              onPress={toggleCameraFacing}
            >
              <Text style={styles.flipButtonText}>🔄</Text>
            </TouchableOpacity>
          </View>

          {photos.length > 0 && (
            <TouchableOpacity
              style={styles.finishButton}
              onPress={finishInspection}
            >
              <Text style={styles.finishButtonText}>
                ✓ Finalizar ({photos.length} fotos)
              </Text>
            </TouchableOpacity>
          )}
        </View>
      </Camera>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  message: {
    textAlign: 'center',
    paddingBottom: 10,
    color: '#fff',
  },
  camera: {
    flex: 1,
  },
  overlay: {
    flex: 1,
    backgroundColor: 'transparent',
  },
  topBar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingTop: 50,
  },
  closeButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  closeButtonText: {
    color: '#fff',
    fontSize: 24,
  },
  photoCount: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    backgroundColor: 'rgba(0,0,0,0.5)',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  bottomBar: {
    position: 'absolute',
    bottom: 40,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  thumbnailContainer: {
    width: 60,
    height: 60,
    borderRadius: 8,
    backgroundColor: 'rgba(255,255,255,0.3)',
    overflow: 'hidden',
  },
  thumbnail: {
    width: '100%',
    height: '100%',
  },
  captureButton: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 4,
    borderColor: 'rgba(255,255,255,0.5)',
  },
  captureButtonInner: {
    width: 68,
    height: 68,
    borderRadius: 34,
    backgroundColor: '#fff',
  },
  flipButton: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  flipButtonText: {
    fontSize: 28,
  },
  finishButton: {
    position: 'absolute',
    bottom: 140,
    left: 20,
    right: 20,
    backgroundColor: '#4CAF50',
    padding: 18,
    borderRadius: 12,
    alignItems: 'center',
  },
  finishButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  button: {
    backgroundColor: '#4CAF50',
    padding: 16,
    borderRadius: 8,
    margin: 20,
  },
  buttonText: {
    color: '#fff',
    textAlign: 'center',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
