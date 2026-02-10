# 🚀 Empezar AHORA - Guía Rápida

> **TODO en la nube (AWS)**  
> **Tiempo total**: 4-6 horas  
> **Costo**: ~$2 para fine-tuning

---

## ✅ Paso 1: Subir Fotos a S3 (5 minutos)

```powershell
cd scripts
python upload-dataset-to-s3.py
```

**Resultado**: 8 fotos de Talos en S3

---

## ✅ Paso 2: Etiquetar Dataset (1 hora)

### Opción A: Roboflow (Recomendado)

1. **Crear cuenta**: https://roboflow.com (gratis)

2. **Crear proyecto**:
   - Click "Create New Project"
   - Nombre: "Omni-Inspector"
   - Tipo: "Object Detection"
   - Annotation Group: "YOLO v11"

3. **Subir fotos**:
   - Click "Upload"
   - Selecciona las 8 fotos de `talos-inspection-photos/`
   - O descárgalas de S3

4. **Etiquetar** (30-45 minutos):
   
   **Clases a crear**:
   - `dent` - Abolladura/golpe
   - `dirt` - Suciedad (CRÍTICO - diferenciarlo de dent)
   - `rust` - Óxido/corrosión
   - `scratch` - Rayadura
   - `spoiled` - Podrido (para alimentos)
   - `mold` - Moho (para alimentos)
   
   **Cómo etiquetar**:
   - Click en una foto
   - Dibuja cajita sobre el daño
   - Selecciona clase
   - Repite para todos los daños visibles
   - Click "Save"
   - Siguiente foto

5. **Generate Dataset**:
   - Click "Generate"
   - Preprocessing: Auto-Orient, Resize 640x640
   - Augmentation:
     - ✅ Flip: Horizontal
     - ✅ Rotation: Between -15° and +15°
     - ✅ Brightness: Between -25% and +25%
     - ✅ Blur: Up to 2px
     - ✅ Noise: Up to 5%
   - Generate: 3x augmentation = ~24 imágenes
   - Click "Generate"

6. **Export**:
   - Format: "YOLOv11"
   - Show download code: Sí
   - Download ZIP

7. **Subir a S3**:
   ```powershell
   # Descomprimir ZIP
   # Ejecutar:
   python upload-labeled-dataset.py --dataset-path "C:\path\to\roboflow-export"
   ```

---

### Opción B: Etiquetado Manual Rápido (15 minutos)

Si quieres empezar MÁS RÁPIDO (pero menos preciso):

```powershell
cd scripts
python generate-quick-labels.py
```

Esto genera anotaciones automáticas para probar el pipeline.

**⚠️ IMPORTANTE**: Estas anotaciones NO son precisas. Solo para testing.

---

## ✅ Paso 3: Lanzar Training Job (5 minutos)

```powershell
cd scripts
python launch-sagemaker-training.py
```

**Resultado**:
- Training job iniciado en SageMaker
- Duración: 2-4 horas
- Costo: ~$1 (con Spot Instances)

**Monitorear**:
```powershell
# Ver progreso
aws sagemaker describe-training-job --training-job-name [JOB_NAME]

# Ver logs en tiempo real
aws logs tail /aws/sagemaker/TrainingJobs --follow
```

**O en la consola**:
https://console.aws.amazon.com/sagemaker/home?region=us-east-1#/jobs

---

## ✅ Paso 4: Mientras Entrena... (2-4 horas)

### Opción A: Trabajar en App Móvil

```powershell
# Crear proyecto React Native
npx create-expo-app omni-inspector-mobile
cd omni-inspector-mobile

# Instalar dependencias
npm install @react-navigation/native @react-navigation/stack
npm install react-native-svg
npm install expo-camera
npm install axios
```

### Opción B: Preparar Backend

```powershell
cd backend
# Crear Lambdas
# Configurar API Gateway
# Setup DynamoDB
```

### Opción C: Tomar café ☕

El training job corre solo en la nube. No necesitas hacer nada.

---

## ✅ Paso 5: Desplegar Modelo (15 minutos)

Cuando el training termine:

```powershell
cd scripts
python deploy-finetuned-model.py
```

**Resultado**:
- Modelo fine-tuned desplegado en SageMaker Endpoint
- Listo para usar en producción

---

## ✅ Paso 6: Probar Modelo (10 minutos)

```powershell
cd yolo-detection
python cli.py detect ../talos-inspection-photos/20260207_091519.jpg --use-finetuned
```

**Resultado esperado**:
```
🎯 DETECTIONS:
   1. dent (medium) - 87% - [100, 200, 300, 400]
   2. dirt (low) - 65% - [500, 100, 600, 250]  ← NUEVO!
   3. rust (low) - 72% - [700, 300, 800, 450]

📊 SUMMARY:
   Total: 3 detections
   Critical: 0
   Severity: medium
```

---

## 💰 Costos

### Training (Una vez)
- ml.g4dn.xlarge Spot: $0.22/hora × 4 horas = **$0.88**
- S3 storage: **$0.01**
- **Total**: **~$1**

### Operación (Mensual, 1,000 inspecciones)
- SageMaker Endpoint: **$0.03**
- Bedrock (Nova): **$2.00**
- Lambda: **$0.40**
- DynamoDB: **$1.75**
- S3: **$0.10**
- **Total**: **$4.28/mes**

---

## 🎯 Timeline de Hoy

```
12:00 PM - Subir fotos a S3 (5 min)
12:05 PM - Etiquetar en Roboflow (1 hora)
1:05 PM  - Subir dataset etiquetado (5 min)
1:10 PM  - Lanzar training job (5 min)
1:15 PM  - ☕ Trabajar en app móvil (2-4 horas)
5:15 PM  - Training completo
5:20 PM  - Desplegar modelo (15 min)
5:35 PM  - Probar detección mejorada (10 min)
5:45 PM  - ✅ LISTO!
```

---

## 📞 Comandos Útiles

```powershell
# Ver training jobs
aws sagemaker list-training-jobs --region us-east-1 --max-results 5

# Ver estado de training
aws sagemaker describe-training-job --training-job-name [JOB_NAME]

# Ver endpoints
aws sagemaker list-endpoints --region us-east-1

# Ver logs
aws logs tail /aws/sagemaker/TrainingJobs --follow

# Cancelar training (si es necesario)
aws sagemaker stop-training-job --training-job-name [JOB_NAME]
```

---

## ❓ FAQ

### ¿Puedo usar GPU local en vez de SageMaker?
**No**. Quieres TODO en la nube. SageMaker es la solución.

### ¿Qué pasa si el training falla?
SageMaker guarda checkpoints. Puedes reanudar desde el último checkpoint.

### ¿Puedo ver el progreso en tiempo real?
Sí, en la consola de SageMaker o con `aws logs tail`.

### ¿Cuánto tarda el training?
2-4 horas dependiendo del tamaño del dataset y número de épocas.

### ¿Puedo usar el modelo mientras entrena?
No. Debes esperar a que termine y desplegarlo.

### ¿El modelo mejorará con más datos?
Sí. Cuantas más fotos etiquetadas, mejor precisión.

---

## 🚀 ¿Listo?

**Ejecuta**:
```powershell
cd scripts
python upload-dataset-to-s3.py
```

**Luego ve a**: https://roboflow.com y empieza a etiquetar! 🎯
