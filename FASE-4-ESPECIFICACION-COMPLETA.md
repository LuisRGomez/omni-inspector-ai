# Fase 4: App Móvil Profesional - Especificación Completa

> **Objetivo**: App móvil con detección en vivo, edición de detecciones, y fine-tuning automático  
> **Tecnología**: React Native + Expo (para iOS y Android)  
> **Estilo**: Basado en tu POC (dark mode, cyan, profesional)

---

## 🎯 Funcionalidades Requeridas

### 1. Detección en Vivo con Cajitas ✅

**Descripción**: Cámara en tiempo real con detección YOLO mostrando cajitas sobre los daños

**Implementación**:
```typescript
// Opción A: Detección en dispositivo (TensorFlow Lite)
import * as tf from '@tensorflow/tfjs';
import { bundleResourceIO } from '@tensorflow/tfjs-react-native';

// Cargar modelo YOLO convertido a TFLite
const model = await tf.loadGraphModel(bundleResourceIO(modelJson, modelWeights));

// Detección en cada frame
const detectFrame = async (imageData) => {
  const tensor = tf.browser.fromPixels(imageData);
  const predictions = await model.predict(tensor);
  return parsePredictions(predictions);
};

// Opción B: Streaming a backend (más preciso)
const streamToBackend = async (frame) => {
  const response = await fetch('https://api.omni-inspector.com/detect/stream', {
    method: 'POST',
    body: JSON.stringify({ frame: base64Frame }),
  });
  return response.json();
};
```

**UI Component**:
```tsx
<View style={styles.cameraContainer}>
  <Camera ref={cameraRef} style={styles.camera}>
    {/* Overlay con cajitas */}
    <Svg style={StyleSheet.absoluteFill}>
      {detections.map((det, i) => (
        <G key={i}>
          <Rect
            x={det.bbox[0]}
            y={det.bbox[1]}
            width={det.bbox[2] - det.bbox[0]}
            height={det.bbox[3] - det.bbox[1]}
            stroke={det.severity > 0.7 ? '#f43f5e' : '#06b6d4'}
            strokeWidth={3}
            fill="none"
          />
          <Text
            x={det.bbox[0]}
            y={det.bbox[1] - 10}
            fill="#06b6d4"
            fontSize={12}
            fontWeight="bold"
          >
            {det.label} ({(det.confidence * 100).toFixed(0)}%)
          </Text>
        </G>
      ))}
    </Svg>
  </Camera>
  
  {/* HUD Info */}
  <View style={styles.hud}>
    <View style={styles.liveIndicator}>
      <View style={styles.pulsingDot} />
      <Text style={styles.liveText}>DETECTANDO...</Text>
    </View>
    <Text style={styles.detectionCount}>
      {detections.length} daños detectados
    </Text>
  </View>
</View>
```

---

### 2. Visualización Nativa de Resultados ✅

**Pantalla de Análisis Completo**:

```tsx
const AnalysisScreen = ({ analysis }) => {
  return (
    <ScrollView style={styles.container}>
      {/* Header con foto */}
      <View style={styles.imageContainer}>
        <Image source={{ uri: analysis.imageUrl }} style={styles.image} />
        <Svg style={StyleSheet.absoluteFill}>
          {analysis.detections.map((det, i) => (
            <DetectionBox key={i} detection={det} />
          ))}
        </Svg>
      </View>

      {/* Métricas principales */}
      <View style={styles.metricsGrid}>
        <MetricCard
          icon="shield-check"
          label="Autenticidad"
          value={`${analysis.forensic.confidence}%`}
          color="#10b981"
        />
        <MetricCard
          icon="alert-triangle"
          label="Fraude Score"
          value={`${analysis.fraudScore}%`}
          color={analysis.fraudScore > 50 ? '#f43f5e' : '#06b6d4'}
        />
        <MetricCard
          icon="target"
          label="Daños"
          value={analysis.detections.length}
          color="#06b6d4"
        />
        <MetricCard
          icon="dollar-sign"
          label="Costo Est."
          value={`$${analysis.estimatedCost}`}
          color="#f59e0b"
        />
      </View>

      {/* Lista de daños */}
      <View style={styles.damageList}>
        <Text style={styles.sectionTitle}>Daños Detectados</Text>
        {analysis.detections.map((det, i) => (
          <DamageCard
            key={i}
            detection={det}
            onEdit={() => openEditor(det)}
            onDelete={() => deleteDetection(det.id)}
          />
        ))}
      </View>

      {/* Datos forenses */}
      <View style={styles.forensicData}>
        <Text style={styles.sectionTitle}>Datos Forenses</Text>
        <InfoRow label="GPS" value={analysis.forensic.gps} />
        <InfoRow label="Fecha" value={analysis.forensic.timestamp} />
        <InfoRow label="Cámara" value={analysis.forensic.camera} />
        <InfoRow label="Hash" value={analysis.forensic.hash} />
      </View>

      {/* Acciones */}
      <View style={styles.actions}>
        <Button
          title="Editar Detecciones"
          onPress={() => navigation.navigate('Editor', { analysis })}
          icon="edit"
        />
        <Button
          title="Descargar PDF"
          onPress={() => downloadPDF(analysis)}
          icon="download"
        />
        <Button
          title="Compartir"
          onPress={() => shareReport(analysis)}
          icon="share"
        />
      </View>
    </ScrollView>
  );
};
```

---

### 3. Sistema de Correcciones (CRÍTICO) ✅

**Pantalla de Editor**:

```tsx
const DetectionEditorScreen = ({ route }) => {
  const { analysis } = route.params;
  const [detections, setDetections] = useState(analysis.detections);
  const [selectedDetection, setSelectedDetection] = useState(null);

  return (
    <View style={styles.container}>
      {/* Imagen con detecciones editables */}
      <View style={styles.imageContainer}>
        <Image source={{ uri: analysis.imageUrl }} style={styles.image} />
        <Svg style={StyleSheet.absoluteFill}>
          {detections.map((det, i) => (
            <TouchableOpacity
              key={i}
              onPress={() => setSelectedDetection(det)}
            >
              <DetectionBox
                detection={det}
                isSelected={selectedDetection?.id === det.id}
              />
            </TouchableOpacity>
          ))}
        </Svg>
      </View>

      {/* Panel de edición */}
      {selectedDetection && (
        <View style={styles.editorPanel}>
          <Text style={styles.panelTitle}>Editar Detección</Text>

          {/* Cambiar tipo */}
          <View style={styles.field}>
            <Text style={styles.label}>Tipo de Daño</Text>
            <Picker
              selectedValue={selectedDetection.type}
              onValueChange={(value) => updateDetection('type', value)}
            >
              <Picker.Item label="Dent (Abolladura)" value="dent" />
              <Picker.Item label="Dirt (Suciedad)" value="dirt" />
              <Picker.Item label="Rust (Óxido)" value="rust" />
              <Picker.Item label="Scratch (Rayadura)" value="scratch" />
              <Picker.Item label="Hole (Agujero)" value="hole" />
              <Picker.Item label="Crack (Grieta)" value="crack" />
              <Picker.Item label="Spoiled (Podrido)" value="spoiled" />
              <Picker.Item label="Mold (Moho)" value="mold" />
            </Picker>
          </View>

          {/* Cambiar severidad */}
          <View style={styles.field}>
            <Text style={styles.label}>Severidad</Text>
            <Slider
              value={selectedDetection.severity}
              onValueChange={(value) => updateDetection('severity', value)}
              minimumValue={0}
              maximumValue={1}
              step={0.1}
            />
            <Text style={styles.severityText}>
              {getSeverityLabel(selectedDetection.severity)}
            </Text>
          </View>

          {/* Agregar nota */}
          <View style={styles.field}>
            <Text style={styles.label}>Nota del Inspector</Text>
            <TextInput
              style={styles.textInput}
              placeholder="Ej: No es golpe, es suciedad acumulada"
              value={selectedDetection.note}
              onChangeText={(text) => updateDetection('note', text)}
              multiline
            />
          </View>

          {/* Acciones */}
          <View style={styles.actions}>
            <Button
              title="Eliminar"
              onPress={() => deleteDetection(selectedDetection.id)}
              color="#f43f5e"
              icon="trash"
            />
            <Button
              title="Guardar"
              onPress={() => saveCorrection(selectedDetection)}
              color="#10b981"
              icon="check"
            />
          </View>
        </View>
      )}

      {/* Botón para agregar detección manual */}
      <TouchableOpacity
        style={styles.addButton}
        onPress={() => setMode('adding')}
      >
        <Icon name="plus" size={24} color="#fff" />
        <Text style={styles.addButtonText}>Agregar Detección Manual</Text>
      </TouchableOpacity>
    </View>
  );
};
```

**Backend para Correcciones**:

```python
# Lambda: save_correction
@app.route('/corrections', methods=['POST'])
def save_correction():
    data = request.json
    
    correction = {
        'correction_id': str(uuid.uuid4()),
        'case_id': data['case_id'],
        'detection_id': data['detection_id'],
        'original_type': data['original_type'],
        'corrected_type': data['corrected_type'],
        'original_severity': data['original_severity'],
        'corrected_severity': data['corrected_severity'],
        'reason': data['reason'],
        'note': data.get('note'),
        'inspector_id': data['inspector_id'],
        'timestamp': datetime.now().isoformat(),
        'image_region': data['image_region'],
        'image_url': data['image_url']
    }
    
    # Guardar en DynamoDB
    table = dynamodb.Table('omni-inspector-corrections')
    table.put_item(Item=correction)
    
    # Agregar a cola de entrenamiento
    sqs.send_message(
        QueueUrl=TRAINING_QUEUE_URL,
        MessageBody=json.dumps(correction)
    )
    
    return jsonify({'success': True, 'correction_id': correction['correction_id']})
```

---

### 4. Feedback Loop Automático ✅

**Sistema de Re-entrenamiento**:

```python
# Lambda: process_corrections_batch
# Se ejecuta mensualmente o cuando hay 500+ correcciones

def process_corrections_batch():
    # 1. Obtener correcciones del último mes
    corrections = get_corrections_from_dynamodb(days=30)
    
    # 2. Descargar imágenes y crear dataset
    dataset = []
    for correction in corrections:
        image = download_from_s3(correction['image_url'])
        
        # Crear anotación en formato YOLO
        annotation = {
            'image': image,
            'bbox': correction['image_region'],
            'class': correction['corrected_type'],
            'severity': correction['corrected_severity']
        }
        dataset.append(annotation)
    
    # 3. Exportar a formato YOLO
    export_to_yolo_format(dataset, 'corrections_dataset/')
    
    # 4. Fine-tuning del modelo
    from ultralytics import YOLO
    
    model = YOLO('yolov11n.pt')  # Modelo base
    
    results = model.train(
        data='corrections_dataset/data.yaml',
        epochs=50,
        imgsz=640,
        batch=16,
        name='omni-inspector-finetuned',
        patience=10
    )
    
    # 5. Evaluar modelo
    metrics = model.val()
    
    if metrics.box.map > 0.7:  # Si mejora
        # 6. Desplegar nuevo modelo
        deploy_to_sagemaker(model, version='v2')
        
        # 7. Notificar
        send_notification(f"Modelo mejorado desplegado. mAP: {metrics.box.map:.2%}")
    
    return {
        'corrections_processed': len(corrections),
        'model_improved': metrics.box.map > 0.7,
        'new_map': metrics.box.map
    }
```

---

### 5. Clases de Detección Expandidas ✅

**Clases Actuales** (YOLOv11 base):
```python
DAMAGE_CLASSES_BASE = {
    'dent': 'Abolladura',
    'rust': 'Óxido',
    'hole': 'Agujero',
    'crack': 'Grieta',
    'scratch': 'Rayadura'
}
```

**Clases Nuevas** (después de fine-tuning):
```python
DAMAGE_CLASSES_EXTENDED = {
    # Daños estructurales
    'dent': 'Abolladura',
    'rust': 'Óxido',
    'hole': 'Agujero',
    'crack': 'Grieta',
    'scratch': 'Rayadura',
    'broken_seal': 'Sello roto',
    'missing_part': 'Parte faltante',
    
    # Diferenciación crítica
    'dirt': 'Suciedad',  # ← NUEVO
    'stain': 'Mancha',   # ← NUEVO
    
    # Mercadería perecedera
    'spoiled': 'Podrido',      # ← NUEVO
    'mold': 'Moho',            # ← NUEVO
    'bruise': 'Magulladura',   # ← NUEVO
    'overripe': 'Sobre-maduro', # ← NUEVO
    'underripe': 'Verde',      # ← NUEVO
    
    # Contenedores
    'container_id': 'ID Contenedor',
    'water_damage': 'Daño por agua',
    'fire_damage': 'Daño por fuego',
    
    # Vehículos
    'paint_damage': 'Daño de pintura',
    'glass_crack': 'Vidrio roto',
    'tire_damage': 'Neumático dañado'
}
```

---

### 6. Proceso de Fine-Tuning ✅

**Paso 1: Recolección de Datos**

```python
# Script: collect_training_data.py

def collect_training_data():
    # Fuentes de datos:
    
    # 1. Correcciones de usuarios (DynamoDB)
    corrections = get_all_corrections()
    
    # 2. Fotos de Talos (8 imágenes iniciales)
    talos_photos = load_talos_photos()
    
    # 3. Dataset público (opcional)
    # - COCO dataset (vehículos, contenedores)
    # - Open Images (daños generales)
    
    # 4. Synthetic data (opcional)
    # - Generar variaciones con augmentation
    
    total_images = len(corrections) + len(talos_photos)
    
    print(f"Total imágenes: {total_images}")
    print(f"Recomendado: 500-1000 para buen fine-tuning")
    
    if total_images < 500:
        print("⚠️ Necesitas más datos. Opciones:")
        print("1. Esperar más correcciones de usuarios")
        print("2. Etiquetar más fotos manualmente")
        print("3. Usar data augmentation")
```

**Paso 2: Etiquetado**

```python
# Usar Roboflow o LabelStudio

# Formato YOLO:
# image.txt:
# class_id x_center y_center width height
# 0 0.5 0.5 0.2 0.3
# 1 0.7 0.3 0.1 0.15

def export_to_yolo_format(corrections):
    for correction in corrections:
        # Convertir bbox a formato YOLO
        x_center = (correction['bbox'][0] + correction['bbox'][2]) / 2
        y_center = (correction['bbox'][1] + correction['bbox'][3]) / 2
        width = correction['bbox'][2] - correction['bbox'][0]
        height = correction['bbox'][3] - correction['bbox'][1]
        
        # Guardar anotación
        with open(f"{correction['image_id']}.txt", 'w') as f:
            f.write(f"{class_to_id[correction['class']]} {x_center} {y_center} {width} {height}\n")
```

**Paso 3: Entrenamiento**

```python
# Script: train_model.py

from ultralytics import YOLO

# Cargar modelo base
model = YOLO('yolov11n.pt')

# Configuración de entrenamiento
results = model.train(
    data='dataset/data.yaml',  # Configuración del dataset
    epochs=100,                 # Número de épocas
    imgsz=640,                  # Tamaño de imagen
    batch=16,                   # Batch size
    patience=20,                # Early stopping
    save=True,                  # Guardar checkpoints
    device='0',                 # GPU
    workers=8,                  # Parallel workers
    
    # Augmentation
    hsv_h=0.015,               # Hue augmentation
    hsv_s=0.7,                 # Saturation
    hsv_v=0.4,                 # Value
    degrees=10,                # Rotation
    translate=0.1,             # Translation
    scale=0.5,                 # Scaling
    shear=0.0,                 # Shearing
    perspective=0.0,           # Perspective
    flipud=0.0,                # Flip up-down
    fliplr=0.5,                # Flip left-right
    mosaic=1.0,                # Mosaic augmentation
    mixup=0.0,                 # Mixup augmentation
)

# Evaluar
metrics = model.val()

print(f"mAP50: {metrics.box.map50:.3f}")
print(f"mAP50-95: {metrics.box.map:.3f}")

# Exportar
model.export(format='torchscript')  # Para SageMaker
```

**Paso 4: Despliegue**

```python
# Script: deploy_finetuned_model.py

def deploy_finetuned_model():
    # 1. Empaquetar modelo
    package_model('runs/train/omni-inspector-finetuned/weights/best.pt')
    
    # 2. Subir a S3
    upload_to_s3('model.tar.gz', 'omni-inspector-models-472661249377/yolo-v2/')
    
    # 3. Crear nuevo modelo en SageMaker
    create_sagemaker_model(
        model_name='omni-inspector-yolo-v2',
        model_data='s3://omni-inspector-models-472661249377/yolo-v2/model.tar.gz'
    )
    
    # 4. Actualizar endpoint (blue-green deployment)
    update_endpoint(
        endpoint_name='omni-inspector-yolo',
        new_model='omni-inspector-yolo-v2'
    )
    
    # 5. Monitorear métricas
    monitor_endpoint_metrics(hours=24)
```

---

## 📱 Estructura de la App

```
mobile-app/
├── src/
│   ├── screens/
│   │   ├── HomeScreen.tsx
│   │   ├── CameraScreen.tsx          # Detección en vivo
│   │   ├── AnalysisScreen.tsx        # Visualización de resultados
│   │   ├── EditorScreen.tsx          # Edición de detecciones
│   │   ├── ReportScreen.tsx          # Vista de reporte
│   │   └── HistoryScreen.tsx         # Historial de casos
│   │
│   ├── components/
│   │   ├── DetectionBox.tsx          # Cajita de detección
│   │   ├── MetricCard.tsx            # Tarjeta de métrica
│   │   ├── DamageCard.tsx            # Tarjeta de daño
│   │   ├── LiveHUD.tsx               # HUD de cámara en vivo
│   │   └── CorrectionPanel.tsx       # Panel de corrección
│   │
│   ├── services/
│   │   ├── api.ts                    # Cliente API
│   │   ├── camera.ts                 # Servicio de cámara
│   │   ├── detection.ts              # Servicio de detección
│   │   └── storage.ts                # Almacenamiento local
│   │
│   ├── models/
│   │   └── yolo-lite.tflite          # Modelo YOLO para dispositivo
│   │
│   └── utils/
│       ├── colors.ts                 # Paleta de colores
│       ├── constants.ts              # Constantes
│       └── helpers.ts                # Funciones auxiliares
│
├── assets/
│   ├── fonts/
│   └── images/
│
└── package.json
```

---

## 🎨 Estilo Visual (Basado en tu POC)

```typescript
// colors.ts
export const colors = {
  // Fondo
  background: '#02040a',
  backgroundSecondary: '#0b0e14',
  
  // Primarios
  primary: '#06b6d4',      // Cyan
  primaryDark: '#0891b2',
  primaryLight: '#22d3ee',
  
  // Acentos
  success: '#10b981',
  warning: '#f59e0b',
  error: '#f43f5e',
  
  // Texto
  textPrimary: '#f1f5f9',
  textSecondary: '#94a3b8',
  textMuted: '#64748b',
  
  // Bordes
  border: 'rgba(6, 182, 212, 0.2)',
  borderLight: 'rgba(255, 255, 255, 0.1)',
};

// styles.ts
export const globalStyles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  
  card: {
    backgroundColor: colors.backgroundSecondary,
    borderRadius: 24,
    padding: 16,
    borderWidth: 1,
    borderColor: colors.border,
  },
  
  button: {
    backgroundColor: colors.primary,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  
  buttonText: {
    color: colors.textPrimary,
    fontSize: 14,
    fontWeight: '900',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
});
```

---

## 🚀 Timeline de Implementación

### Semana 1: Setup + Detección en Vivo
- [ ] Setup proyecto React Native + Expo
- [ ] Implementar cámara con detección en vivo
- [ ] Integrar con backend (API Gateway + Lambda)
- [ ] Mostrar cajitas en tiempo real
- [ ] HUD profesional

### Semana 2: Visualización + Edición
- [ ] Pantalla de análisis completo
- [ ] Dashboard con métricas
- [ ] Sistema de correcciones
- [ ] Editor de detecciones
- [ ] Agregar detecciones manuales

### Semana 3: Backend + Feedback Loop
- [ ] API para correcciones
- [ ] DynamoDB para almacenar correcciones
- [ ] Cola SQS para entrenamiento
- [ ] Lambda para procesamiento batch
- [ ] Sistema de notificaciones

### Semana 4: Fine-tuning + Despliegue
- [ ] Recolectar correcciones
- [ ] Etiquetar dataset
- [ ] Entrenar modelo mejorado
- [ ] Desplegar a SageMaker
- [ ] Testing completo

---

## 💰 Costos Estimados

### Desarrollo
- **Tiempo**: 4 semanas
- **Recursos**: 1 desarrollador full-time

### Operación (1,000 inspecciones/mes)
| Servicio | Costo |
|----------|-------|
| SageMaker (YOLO) | $0.03 |
| Bedrock (Nova) | $2.00 |
| Lambda (API) | $0.40 |
| DynamoDB | $1.75 |
| S3 Storage | $0.10 |
| SQS (correcciones) | $0.01 |
| **Total** | **$4.29/mes** |

### Fine-tuning (mensual)
- **SageMaker Training**: ~$5-10 por entrenamiento
- **Frecuencia**: 1 vez al mes (o cuando hay 500+ correcciones)

---

## ✅ Checklist de Funcionalidades

### Detección
- [ ] Detección en vivo con cajitas
- [ ] Detección en fotos capturadas
- [ ] Detección en fotos subidas
- [ ] Batch detection (múltiples fotos)

### Visualización
- [ ] Dashboard con métricas
- [ ] Foto anotada interactiva
- [ ] Lista de daños detallada
- [ ] Datos forenses completos
- [ ] Gráficos de severidad

### Edición
- [ ] Cambiar tipo de daño
- [ ] Ajustar severidad
- [ ] Eliminar falsos positivos
- [ ] Agregar detecciones manuales
- [ ] Agregar notas del inspector

### Reportes
- [ ] Vista nativa en app
- [ ] Exportar PDF
- [ ] Compartir (email, WhatsApp)
- [ ] Historial de reportes

### Fine-tuning
- [ ] Guardar correcciones
- [ ] Cola de entrenamiento
- [ ] Procesamiento batch
- [ ] Re-entrenamiento automático
- [ ] Despliegue de modelo mejorado

---

**Proyecto**: Omni-Inspector AI  
**Fase**: 4 - App Móvil Profesional  
**Estado**: Especificación completa  
**Próximo**: Implementación
