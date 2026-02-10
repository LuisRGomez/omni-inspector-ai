# 🚀 ACCIÓN INMEDIATA - Empezar HOY

> **Fecha**: 9 de Febrero, 2026  
> **Objetivo**: Fine-tuning en AWS con dataset real  
> **Tiempo**: 4-6 horas  
> **Costo**: ~$1-2 USD

---

## ✅ LO QUE YA TIENES

- ✅ AWS configurado (Account: 472661249377, Region: us-east-1)
- ✅ Bedrock habilitado (Nova models)
- ✅ S3 buckets creados
- ✅ IAM role configurado
- ✅ 8 fotos de Talos en `talos-inspection-photos/`
- ✅ Fase 1 (Forensic) funcionando 100%
- ✅ Fase 3 (Nova) funcionando 100%
- ✅ Créditos AWS disponibles

---

## 🎯 PLAN DE HOY (Opción 2: Dataset Real)

### Opción A: Roboflow + Talos Photos (RECOMENDADO)
**Tiempo**: 2-3 horas  
**Costo**: Gratis  
**Resultado**: 100-200 imágenes etiquetadas con augmentation

### Opción B: Dataset Público + Talos Photos
**Tiempo**: 1-2 horas  
**Costo**: Gratis  
**Resultado**: 500-1000 imágenes pre-etiquetadas + tus 8 fotos

### Opción C: AWS Ground Truth Private Workforce
**Tiempo**: 1 semana (etiquetado por inspectores)  
**Costo**: Gratis (workforce privado)  
**Resultado**: Dataset etiquetado por expertos

---

## 📋 PASO A PASO - OPCIÓN A (EMPEZAR AHORA)

### Paso 1: Subir Fotos a S3 (5 minutos)

```powershell
cd scripts
python upload-dataset-to-s3.py
```

**Resultado**: 8 fotos en `s3://omni-inspector-models-472661249377/datasets/talos-v1/raw-images/`

---

### Paso 2: Etiquetar en Roboflow (1-2 horas)

#### 2.1. Crear Cuenta
1. Ve a: https://roboflow.com
2. Sign up (gratis hasta 10,000 imágenes)
3. Verifica email

#### 2.2. Crear Proyecto
1. Click "Create New Project"
2. Nombre: **Omni-Inspector**
3. Tipo: **Object Detection**
4. Annotation Group: **YOLO v11**
5. Click "Create Project"

#### 2.3. Subir Fotos
1. Click "Upload"
2. Arrastra las 8 fotos de `talos-inspection-photos/`
3. O descárgalas de S3
4. Click "Finish Uploading"

#### 2.4. Etiquetar Daños (CRÍTICO)

**Clases a crear**:

| Clase | Descripción | Ejemplo |
|-------|-------------|---------|
| `dent` | Abolladura/golpe | Chapa hundida, deformación |
| `dirt` | Suciedad (NO daño) | Polvo, barro, manchas removibles |
| `rust` | Óxido/corrosión | Manchas naranjas, metal oxidado |
| `scratch` | Rayadura | Líneas en pintura |
| `hole` | Agujero | Perforación visible |
| `crack` | Grieta | Fisura en superficie |
| `spoiled` | Podrido (alimentos) | Fruta/carne en mal estado |
| `mold` | Moho (alimentos) | Hongos visibles |

**Cómo etiquetar**:
1. Click en una foto
2. Presiona `B` (bounding box tool)
3. Dibuja cajita sobre el daño
4. Selecciona clase (dent, dirt, rust, etc.)
5. Repite para todos los daños en la foto
6. Click "Save" (o `Ctrl+S`)
7. Siguiente foto (flecha derecha)

**⚠️ IMPORTANTE - Diferencia DIRT vs DENT**:
- **DIRT**: Suciedad superficial, se puede limpiar
- **DENT**: Daño estructural, deformación permanente

**Tiempo estimado**: 10-15 minutos por foto = 1-2 horas total

---

#### 2.5. Generate Dataset con Augmentation

1. Click "Generate" (botón verde)
2. **Preprocessing**:
   - ✅ Auto-Orient
   - ✅ Resize: 640x640 (YOLO standard)
   - ✅ Auto-Adjust Contrast
3. **Augmentation** (CRÍTICO para mejorar modelo):
   - ✅ Flip: Horizontal
   - ✅ Rotation: Between -15° and +15°
   - ✅ Brightness: Between -25% and +25%
   - ✅ Blur: Up to 2px
   - ✅ Noise: Up to 5%
   - ✅ Cutout: 3 boxes with 10% size each
4. **Generate**: 
   - Train/Val/Test Split: 70/20/10
   - Augmentation multiplier: **3x** (8 fotos → 24 imágenes)
5. Click "Generate"

**Resultado**: ~24 imágenes con variaciones

---

#### 2.6. Export Dataset

1. Click "Export"
2. Format: **YOLOv11**
3. Show download code: **Sí**
4. Click "Download ZIP"

**Estructura del ZIP**:
```
roboflow-export/
├── train/
│   ├── images/
│   │   ├── img1.jpg
│   │   └── img2.jpg
│   └── labels/
│       ├── img1.txt
│       └── img2.txt
├── valid/
│   ├── images/
│   └── labels/
├── test/
│   ├── images/
│   └── labels/
└── data.yaml
```

---

### Paso 3: Subir Dataset Etiquetado a S3 (10 minutos)

```powershell
# Descomprimir ZIP
# Luego ejecutar:
cd scripts
python upload-labeled-dataset.py --dataset-path "C:\path\to\roboflow-export"
```

**Resultado**: Dataset en `s3://omni-inspector-models-472661249377/datasets/talos-v1/`

---

### Paso 4: Lanzar SageMaker Training Job (5 minutos)

```powershell
cd scripts
python launch-sagemaker-training.py
```

**Configuración**:
- Instance: `ml.g4dn.xlarge` (GPU)
- Spot Instances: Sí (70% descuento)
- Epochs: 100
- Batch: 16
- Duración: 2-4 horas
- Costo: ~$0.88 USD

**Resultado**: Training job corriendo en AWS

**Monitorear**:
```powershell
# Ver estado
aws sagemaker describe-training-job --training-job-name [JOB_NAME]

# Ver logs en tiempo real
aws logs tail /aws/sagemaker/TrainingJobs --follow
```

**O en la consola**:
https://console.aws.amazon.com/sagemaker/home?region=us-east-1#/jobs

---

### Paso 5: Mientras Entrena... (2-4 horas)

**Opciones**:

#### A) Trabajar en App Móvil
- Diseñar UI basada en tu POC
- Implementar cámara con detección en vivo
- Sistema de correcciones

#### B) Preparar Backend
- Lambdas para API
- DynamoDB para correcciones
- SQS para feedback loop

#### C) Buscar Dataset Público (Opcional)
- Roboflow Universe: https://universe.roboflow.com
- Buscar: "vehicle damage", "container damage", "food quality"
- Descargar y combinar con tus fotos

#### D) Tomar café ☕
- El training corre solo en la nube
- No necesitas hacer nada

---

### Paso 6: Desplegar Modelo Fine-tuned (15 minutos)

Cuando el training termine (2-4 horas):

```powershell
cd scripts
python deploy-finetuned-model.py
```

**Resultado**: Modelo mejorado desplegado en SageMaker Endpoint

---

### Paso 7: Probar Modelo Mejorado (10 minutos)

```powershell
cd yolo-detection
python cli.py detect ..\talos-inspection-photos\20260207_091519.jpg --use-finetuned
```

**Resultado esperado**:
```
🎯 DETECTIONS (MODELO FINE-TUNED):
   1. dent (medium) - 92% - [100, 200, 300, 400]
   2. dirt (low) - 78% - [500, 100, 600, 250]  ← NUEVO! Diferencia dirt vs dent
   3. rust (low) - 85% - [700, 300, 800, 450]

📊 MEJORAS vs MODELO BASE:
   ✅ Detecta dirt vs dent correctamente
   ✅ Mayor confianza en detecciones
   ✅ Menos falsos positivos
```

---

## 📋 PASO A PASO - OPCIÓN B (MÁS RÁPIDO)

### Usar Dataset Público + Talos Photos

#### 1. Buscar Dataset en Roboflow Universe (30 minutos)

1. Ve a: https://universe.roboflow.com
2. Busca:
   - "vehicle damage detection"
   - "container damage"
   - "rust detection"
   - "dent detection"
3. Encuentra dataset con >500 imágenes
4. Click "Download Dataset"
5. Format: **YOLOv11**
6. Download ZIP

**Datasets recomendados**:
- Vehicle Damage Detection: https://universe.roboflow.com/vehicle-damage
- Container Inspection: https://universe.roboflow.com/container-damage
- Rust Detection: https://universe.roboflow.com/rust-detection

#### 2. Combinar con Fotos de Talos (15 minutos)

```powershell
cd scripts
python combine-datasets.py --public-dataset "C:\path\to\public-dataset" --talos-photos "..\talos-inspection-photos"
```

**Resultado**: Dataset combinado con 500+ imágenes

#### 3. Subir a S3 y Entrenar (igual que Opción A)

```powershell
python upload-labeled-dataset.py --dataset-path "C:\path\to\combined-dataset"
python launch-sagemaker-training.py
```

---

## 📋 PASO A PASO - OPCIÓN C (MÁS LENTO PERO MEJOR)

### AWS Ground Truth Private Workforce

**Ventajas**:
- Gratis (workforce privado)
- Etiquetado por tus inspectores (expertos)
- Mejor calidad de anotaciones

**Desventajas**:
- Toma 1 semana (depende de inspectores)
- Requiere setup de Cognito

#### 1. Setup Ground Truth (30 minutos)

```powershell
cd scripts
python setup-ground-truth.py
```

**Resultado**: Labeling job creado

#### 2. Invitar Inspectores (10 minutos)

1. Ve a: https://console.aws.amazon.com/sagemaker/groundtruth
2. Click "Private workforce"
3. Click "Invite workers"
4. Ingresa emails de inspectores
5. Ellos reciben invitación

#### 3. Inspectores Etiquetan (1 semana)

- Acceden a portal de etiquetado
- Dibujan cajitas sobre daños
- Clasifican (dent, dirt, rust, etc.)

#### 4. Procesar Output y Entrenar

```powershell
python process-ground-truth-output.py
python launch-sagemaker-training.py
```

---

## 💰 COSTOS

### Opción A: Roboflow + Talos
- Roboflow: **Gratis** (hasta 10,000 imágenes)
- SageMaker Training: **~$0.88 USD** (Spot Instances)
- S3 Storage: **~$0.01 USD**
- **Total**: **~$1 USD**

### Opción B: Dataset Público + Talos
- Dataset público: **Gratis**
- SageMaker Training: **~$0.88 USD**
- S3 Storage: **~$0.02 USD**
- **Total**: **~$1 USD**

### Opción C: Ground Truth
- Ground Truth (private workforce): **Gratis**
- SageMaker Training: **~$0.88 USD**
- S3 Storage: **~$0.01 USD**
- **Total**: **~$1 USD**

---

## ⏱️ TIMELINE DE HOY

```
12:00 PM - Subir fotos a S3 (5 min)
12:05 PM - Crear cuenta Roboflow (5 min)
12:10 PM - Crear proyecto y subir fotos (10 min)
12:20 PM - Etiquetar 8 fotos (1-2 horas)
2:20 PM  - Generate dataset con augmentation (10 min)
2:30 PM  - Export y descargar (5 min)
2:35 PM  - Subir dataset a S3 (10 min)
2:45 PM  - Lanzar training job (5 min)
2:50 PM  - ☕ Trabajar en app móvil (2-4 horas)
6:50 PM  - Training completo
7:00 PM  - Desplegar modelo (15 min)
7:15 PM  - Probar detección mejorada (10 min)
7:25 PM  - ✅ LISTO!
```

---

## 🎓 SOBRE LAS FOTOS DE TALOS

### ¿Qué Hay en las Fotos?

Tienes 8 fotos en `talos-inspection-photos/`:
- `20260207_091519.jpg`
- `20260207_091522.jpg`
- `20260207_091525.jpg`
- `20260207_092811.jpg`
- `20260207_092814.jpg`
- `20260207_092815.jpg`
- `20260207_092817.jpg`
- `20260207_092819.jpg`

### ¿Necesito Más Fotos?

**Para empezar HOY**: NO, 8 fotos + augmentation = 24-50 imágenes (suficiente para probar)

**Para producción**: SÍ, necesitas 500-1000 imágenes para mejor precisión

**Opciones para conseguir más fotos**:
1. **Tomar más fotos** de vehículos/contenedores con daños
2. **Dataset público** de Roboflow Universe (500+ imágenes)
3. **Correcciones de usuarios** (feedback loop automático)
4. **Ground Truth** con inspectores etiquetando

---

## 🎯 CLASES DE DAÑOS A ETIQUETAR

### Vehículos
- ✅ `dent` - Abolladura/golpe
- ✅ `dirt` - Suciedad (CRÍTICO - diferenciarlo)
- ✅ `scratch` - Rayadura
- ✅ `rust` - Óxido
- ✅ `paint_damage` - Daño de pintura
- ✅ `glass_crack` - Vidrio roto

### Contenedores
- ✅ `dent` - Abolladura
- ✅ `dirt` - Suciedad
- ✅ `rust` - Óxido
- ✅ `hole` - Agujero
- ✅ `crack` - Grieta
- ✅ `broken_seal` - Sello roto

### Alimentos Perecederos
- ✅ `spoiled` - Podrido
- ✅ `mold` - Moho
- ✅ `bruise` - Magulladura
- ✅ `overripe` - Sobre-maduro
- ✅ `underripe` - Verde

---

## ✅ CHECKLIST

- [ ] Fotos subidas a S3
- [ ] Cuenta Roboflow creada
- [ ] Proyecto creado
- [ ] 8 fotos etiquetadas
- [ ] Dataset generado con augmentation
- [ ] Dataset exportado (YOLOv11)
- [ ] Dataset subido a S3
- [ ] Training job lanzado
- [ ] Modelo desplegado
- [ ] Detección mejorada validada

---

## 📞 COMANDOS ÚTILES

```powershell
# Subir fotos a S3
cd scripts
python upload-dataset-to-s3.py

# Subir dataset etiquetado
python upload-labeled-dataset.py --dataset-path "C:\path\to\roboflow-export"

# Lanzar training
python launch-sagemaker-training.py

# Ver estado de training
aws sagemaker describe-training-job --training-job-name [JOB_NAME]

# Ver logs
aws logs tail /aws/sagemaker/TrainingJobs --follow

# Desplegar modelo
python deploy-finetuned-model.py

# Probar modelo
cd ..\yolo-detection
python cli.py detect ..\talos-inspection-photos\20260207_091519.jpg --use-finetuned
```

---

## 🚀 EMPEZAR AHORA

**Recomendación**: Opción A (Roboflow + Talos)

**Razón**: 
- Más rápido (empiezas en 5 minutos)
- Gratis
- Control total sobre etiquetado
- Aprenderás qué daños detectar

**Próximo paso**:
```powershell
cd scripts
python upload-dataset-to-s3.py
```

**Luego ve a**: https://roboflow.com y empieza a etiquetar! 🎯

---

**¿Listo para empezar?** 🚀
