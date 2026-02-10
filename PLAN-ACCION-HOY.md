# Plan de Acción - HOY

> **Objetivo**: Fine-tuning completo + App funcionando  
> **Tiempo**: 4-6 horas  
> **Créditos**: Disponibles para entrenamiento

---

## 🎯 Estrategia Rápida

En lugar de esperar SageMaker (lento), vamos a:

1. ✅ **Usar YOLO local** para desarrollo y fine-tuning
2. ✅ **Fine-tuning inmediato** con tus fotos de Talos
3. ✅ **Desplegar a SageMaker después** (opcional, para producción)

**Ventaja**: Empezamos YA, no esperamos 30 minutos

---

## 📋 Checklist de Hoy

### Parte 1: Setup YOLO Local (30 minutos)

- [ ] Instalar ultralytics
- [ ] Descargar YOLOv11n base
- [ ] Probar detección con fotos de Talos
- [ ] Validar que funciona

### Parte 2: Preparar Dataset (1 hora)

- [ ] Etiquetar 8 fotos de Talos con Roboflow
- [ ] Crear clases personalizadas:
  - `dent` (abolladura)
  - `dirt` (suciedad) ← CRÍTICO
  - `rust` (óxido)
  - `scratch` (rayadura)
  - `spoiled` (podrido - para alimentos)
  - `mold` (moho - para alimentos)
- [ ] Exportar en formato YOLO
- [ ] Data augmentation (generar 100+ variaciones)

### Parte 3: Fine-tuning (2 horas)

- [ ] Configurar entrenamiento
- [ ] Entrenar modelo (50-100 épocas)
- [ ] Evaluar métricas (mAP)
- [ ] Guardar mejor modelo

### Parte 4: Integrar con Sistema (1 hora)

- [ ] Actualizar `yolo_detector.py` con modelo fine-tuned
- [ ] Probar detección mejorada
- [ ] Validar diferencia dirt vs dent
- [ ] Probar con todas las fotos de Talos

### Parte 5: App Móvil - Inicio (2 horas)

- [ ] Setup React Native + Expo
- [ ] Migrar UI de tu POC
- [ ] Integrar con backend
- [ ] Detección en vivo básica

---

## 🚀 Empecemos

### Paso 1: Instalar Ultralytics

```powershell
cd yolo-detection
pip install ultralytics==8.1.0
```

### Paso 2: Descargar Modelo Base

```python
from ultralytics import YOLO

# Descargar YOLOv11n
model = YOLO('yolov11n.pt')

# Probar con foto de Talos
results = model('../talos-inspection-photos/20260207_091519.jpg')

# Ver resultados
results[0].show()
```

### Paso 3: Etiquetar Dataset

**Opción A: Roboflow (Recomendado - Rápido)**

1. Ve a: https://roboflow.com
2. Crea proyecto "Omni-Inspector"
3. Sube 8 fotos de Talos
4. Etiqueta daños:
   - Dibuja cajitas sobre daños
   - Asigna clase (dent, dirt, rust, etc.)
5. Genera dataset con augmentation (100+ imágenes)
6. Exporta en formato "YOLOv11"

**Opción B: LabelStudio (Local)**

```bash
pip install label-studio
label-studio start
```

**Opción C: Manual (Más rápido para 8 fotos)**

Voy a crear un script para etiquetar rápido:

```python
# quick_label.py
import cv2
import json

def label_image(image_path):
    img = cv2.imread(image_path)
    annotations = []
    
    print(f"Etiquetando: {image_path}")
    print("Clases: 0=dent, 1=dirt, 2=rust, 3=scratch, 4=spoiled, 5=mold")
    
    while True:
        # Mostrar imagen
        cv2.imshow('Image', img)
        
        # Seleccionar región
        roi = cv2.selectROI('Image', img, False)
        
        if roi == (0, 0, 0, 0):
            break
        
        # Pedir clase
        class_id = int(input("Clase (0-5): "))
        
        # Guardar anotación
        x, y, w, h = roi
        x_center = (x + w/2) / img.shape[1]
        y_center = (y + h/2) / img.shape[0]
        width = w / img.shape[1]
        height = h / img.shape[0]
        
        annotations.append(f"{class_id} {x_center} {y_center} {width} {height}")
    
    # Guardar
    txt_path = image_path.replace('.jpg', '.txt')
    with open(txt_path, 'w') as f:
        f.write('\n'.join(annotations))
    
    cv2.destroyAllWindows()

# Etiquetar todas las fotos
import glob
for img_path in glob.glob('../talos-inspection-photos/*.jpg'):
    label_image(img_path)
```

### Paso 4: Estructura del Dataset

```
dataset/
├── data.yaml
├── train/
│   ├── images/
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   │   └── ...
│   └── labels/
│       ├── img1.txt
│       ├── img2.txt
│       └── ...
└── val/
    ├── images/
    └── labels/
```

**data.yaml**:
```yaml
path: ./dataset
train: train/images
val: val/images

nc: 6  # número de clases
names: ['dent', 'dirt', 'rust', 'scratch', 'spoiled', 'mold']
```

### Paso 5: Fine-tuning

```python
# train_custom.py
from ultralytics import YOLO

# Cargar modelo base
model = YOLO('yolov11n.pt')

# Entrenar
results = model.train(
    data='dataset/data.yaml',
    epochs=100,
    imgsz=640,
    batch=8,
    patience=20,
    save=True,
    device='0',  # GPU (o 'cpu' si no tienes)
    
    # Augmentation agresivo (para compensar pocas imágenes)
    hsv_h=0.015,
    hsv_s=0.7,
    hsv_v=0.4,
    degrees=20,
    translate=0.2,
    scale=0.9,
    shear=5,
    perspective=0.001,
    flipud=0.5,
    fliplr=0.5,
    mosaic=1.0,
    mixup=0.15,
    copy_paste=0.3,
    
    # Optimización
    optimizer='AdamW',
    lr0=0.001,
    lrf=0.01,
    momentum=0.937,
    weight_decay=0.0005,
    warmup_epochs=3,
    warmup_momentum=0.8,
    warmup_bias_lr=0.1,
)

# Evaluar
metrics = model.val()

print(f"mAP50: {metrics.box.map50:.3f}")
print(f"mAP50-95: {metrics.box.map:.3f}")

# Guardar
model.save('omni-inspector-finetuned.pt')
```

---

## ⚡ Opción ULTRA RÁPIDA (Si no quieres etiquetar)

Voy a crear un dataset sintético con las fotos de Talos:

```python
# generate_synthetic_dataset.py
import cv2
import numpy as np
import random
from pathlib import Path

def generate_synthetic_annotations(image_path, num_annotations=5):
    """Genera anotaciones sintéticas para empezar rápido"""
    img = cv2.imread(str(image_path))
    h, w = img.shape[:2]
    
    annotations = []
    
    for _ in range(num_annotations):
        # Generar bbox aleatorio
        x = random.randint(0, w - 100)
        y = random.randint(0, h - 100)
        box_w = random.randint(50, 200)
        box_h = random.randint(50, 200)
        
        # Clase aleatoria
        class_id = random.randint(0, 5)
        
        # Convertir a formato YOLO
        x_center = (x + box_w/2) / w
        y_center = (y + box_h/2) / h
        width = box_w / w
        height = box_h / h
        
        annotations.append(f"{class_id} {x_center} {y_center} {width} {height}")
    
    return annotations

# Generar dataset
dataset_path = Path('dataset_synthetic')
dataset_path.mkdir(exist_ok=True)

(dataset_path / 'train' / 'images').mkdir(parents=True, exist_ok=True)
(dataset_path / 'train' / 'labels').mkdir(parents=True, exist_ok=True)

# Procesar fotos de Talos
talos_photos = list(Path('../talos-inspection-photos').glob('*.jpg'))

for i, photo in enumerate(talos_photos):
    # Copiar imagen
    img = cv2.imread(str(photo))
    
    # Generar múltiples variaciones (augmentation)
    for j in range(10):  # 10 variaciones por foto = 80 imágenes
        # Aplicar transformaciones
        if random.random() > 0.5:
            img_aug = cv2.flip(img, 1)  # Flip horizontal
        else:
            img_aug = img.copy()
        
        # Rotar
        angle = random.randint(-15, 15)
        M = cv2.getRotationMatrix2D((img.shape[1]/2, img.shape[0]/2), angle, 1)
        img_aug = cv2.warpAffine(img_aug, M, (img.shape[1], img.shape[0]))
        
        # Ajustar brillo
        brightness = random.uniform(0.7, 1.3)
        img_aug = cv2.convertScaleAbs(img_aug, alpha=brightness, beta=0)
        
        # Guardar
        img_name = f"talos_{i}_{j}.jpg"
        cv2.imwrite(str(dataset_path / 'train' / 'images' / img_name), img_aug)
        
        # Generar anotaciones
        annotations = generate_synthetic_annotations(photo)
        
        # Guardar anotaciones
        txt_name = f"talos_{i}_{j}.txt"
        with open(dataset_path / 'train' / 'labels' / txt_name, 'w') as f:
            f.write('\n'.join(annotations))

print(f"Dataset generado: {len(list((dataset_path / 'train' / 'images').glob('*.jpg')))} imágenes")
```

**NOTA**: Este dataset sintético NO será preciso, pero te permite:
1. ✅ Empezar a entrenar YA
2. ✅ Probar el pipeline completo
3. ✅ Ver cómo funciona el fine-tuning
4. ❌ NO usar en producción (necesitas etiquetar bien después)

---

## 🎯 Decisión: ¿Qué Hacemos?

### Opción A: Etiquetado Rápido (1 hora)
- Usar Roboflow
- Etiquetar 8 fotos manualmente
- Augmentation automático → 100+ imágenes
- **Resultado**: Modelo decente

### Opción B: Dataset Sintético (5 minutos)
- Generar anotaciones automáticas
- Entrenar modelo de prueba
- **Resultado**: Modelo malo, pero funciona para probar

### Opción C: Híbrido (Recomendado)
- Generar dataset sintético YA
- Entrenar modelo v1 (para probar)
- Mientras tanto, etiquetar bien en Roboflow
- Entrenar modelo v2 (bueno)

---

## ⏰ Timeline de Hoy

### Ahora - 1:00 PM
- [ ] Instalar ultralytics
- [ ] Generar dataset sintético
- [ ] Entrenar modelo v1

### 1:00 PM - 2:00 PM
- [ ] Etiquetar fotos en Roboflow
- [ ] Exportar dataset real

### 2:00 PM - 4:00 PM
- [ ] Entrenar modelo v2 (con datos reales)
- [ ] Evaluar mejoras

### 4:00 PM - 6:00 PM
- [ ] Integrar modelo en sistema
- [ ] Probar detección mejorada
- [ ] Iniciar app móvil

---

## 🚀 ¿Empezamos?

**Dime**:
1. ¿Tienes GPU? (para entrenar más rápido)
2. ¿Prefieres Opción A, B o C?
3. ¿Empiezo a generar el dataset sintético mientras decides?

**Mientras tanto**, voy a:
- Instalar ultralytics
- Preparar scripts de entrenamiento
- Crear estructura de dataset

¿Dale? 🚀
