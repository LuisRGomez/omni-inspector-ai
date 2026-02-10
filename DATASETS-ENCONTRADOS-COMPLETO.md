# 📦 Datasets Encontrados - Análisis Completo

---

## ✅ DATASETS PERFECTOS PARA TU CASO

### 1. Fresh and Rotten Fruits Dataset (Mendeley) ⭐⭐⭐⭐⭐

**URL**: https://data.mendeley.com/datasets/bdd69gyhv8

**📊 Detalles**:
- **12,335 imágenes** (3,200 originales + augmentation)
- **16 clases**:
  - ✅ Fresh Apple / Rotten Apple
  - ✅ Fresh Banana / Rotten Banana
  - ✅ Fresh Orange / Rotten Orange
  - ✅ Fresh Grape / Rotten Grape
  - ✅ Fresh Guava / Rotten Guava
  - ✅ Fresh Jujube / Rotten Jujube
  - ✅ Fresh Pomegranate / Rotten Pomegranate
  - ✅ Fresh Strawberry / Rotten Strawberry

**✅ Útil para tus clases**:
- `spoiled` ← Rotten classes
- `mold` ← Incluido en rotten
- `overripe` ← Parcialmente

**🎯 Perfecto para**: Detección de frutas podridas

**📥 Cómo descargar**:
1. Ve a: https://data.mendeley.com/datasets/bdd69gyhv8
2. Click "Download"
3. Requiere cuenta Mendeley (gratis)
4. Formato: Imágenes + labels

**💰 Costo**: Gratis

---

### 2. Fruit Freshness Detection Dataset (GitHub) ⭐⭐⭐⭐⭐

**URL**: https://github.com/zijianchen98/Fruit-freshness-detection-dataset

**📊 Detalles**:
- **9 clases**:
  - ✅ Fresh Apple / Normal Apple / Rotten Apple
  - ✅ Fresh Banana / Normal Banana / Rotten Banana
  - ✅ Fresh Orange / Normal Orange / Rotten Orange

**✅ Útil para tus clases**:
- `spoiled` ← Rotten classes
- `overripe` ← Normal classes
- `underripe` ← Fresh classes (parcialmente)

**🎯 Perfecto para**: 3 niveles de maduración

**📥 Cómo descargar**:
```bash
git clone https://github.com/zijianchen98/Fruit-freshness-detection-dataset.git
```

**💰 Costo**: Gratis

---

### 3. Banana Ripeness Stage Dataset (IEEE DataPort) ⭐⭐⭐⭐

**URL**: https://ieee-dataport.org/documents/banana-ripeness-stage-image-dataset-ladder-model-training-and-evaluation

**📊 Detalles**:
- **1,115 imágenes**
- **5 etapas de maduración**:
  - Day 1: Greenish-yellow (verde)
  - Day 2: Yellow (amarillo)
  - Day 3: Ripe (maduro)
  - Day 4: Overripe (sobre-maduro)
  - Day 5: Very overripe (muy sobre-maduro)

**✅ Útil para tus clases**:
- `underripe` ← Day 1
- `overripe` ← Day 4-5
- `spoiled` ← Day 5 (parcialmente)

**🎯 Perfecto para**: Maduración de bananas

**📥 Cómo descargar**:
1. Ve a: https://ieee-dataport.org
2. Requiere cuenta IEEE (gratis)
3. Busca "Banana Ripeness Stage"

**💰 Costo**: Gratis

---

### 4. ACFR Multifruit Dataset ⭐⭐⭐

**URL**: https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/

**📊 Detalles**:
- **3,704 imágenes**:
  - 1,120 imágenes de manzanas (Pink Lady, Kanzi)
  - 1,964 imágenes de mangos (Calypso)
  - 620 imágenes de almendras (Nonpareil)
- **Anotaciones**:
  - Apples: Circle annotations + pixel-wise segmentation
  - Mangoes: Rectangle annotations
  - Almonds: Rectangle annotations

**⚠️ Útil para tus clases**:
- Detección de frutas (NO daños específicos)
- Segmentación de frutas
- Conteo de frutas en árboles

**🎯 Útil para**: Detección de frutas en general, NO para spoiled/mold/bruise

**📥 Cómo descargar**:
```bash
wget https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/acfr-multifruit-2016.zip
```

**💰 Costo**: Gratis

---

### 5. Fruits 360 Dataset (GitHub) ⭐⭐⭐

**URL**: https://github.com/fruits-360

**📊 Detalles**:
- **166,293 imágenes**
- **237 tipos de frutas, verduras, nueces**
- Múltiples variedades:
  - Apples: Crimson Snow, Golden, Granny Smith, Pink Lady, Red Delicious
  - Bananas: Yellow, Red, Lady Finger
  - Avocado: Normal, Ripe

**✅ Útil para tus clases**:
- `overripe` ← Avocado ripe, Banana ripe
- Variedades de frutas

**⚠️ Limitaciones**:
- Mayoría son frutas frescas
- Pocas imágenes de frutas podridas
- Enfoque en clasificación, NO detección

**🎯 Útil para**: Clasificación de tipos de frutas

**📥 Cómo descargar**:
```bash
git clone https://github.com/Horea94/Fruit-Images-Dataset.git
```

**💰 Costo**: Gratis

---

### 6. Fruit and Vegetable Disease Dataset (GTS.ai) ⭐⭐⭐⭐

**URL**: https://gts.ai/dataset-download/fruit-and-vegetable-disease-dataset/

**📊 Detalles**:
- **28 directorios**
- **14 frutas y verduras**
- **Healthy vs Rotten**

**✅ Útil para tus clases**:
- `spoiled` ← Rotten classes
- `mold` ← Disease classes

**🎯 Perfecto para**: Enfermedades y daños en frutas/verduras

**📥 Cómo descargar**:
1. Ve a: https://gts.ai/dataset-download/fruit-and-vegetable-disease-dataset/
2. Requiere registro (gratis)

**💰 Costo**: Gratis

---

## 📊 Comparación de Datasets

| Dataset | Imágenes | Clases Útiles | Formato | Mejor Para |
|---------|----------|---------------|---------|------------|
| **Fresh & Rotten (Mendeley)** | 12,335 | spoiled, mold | Images + Labels | ⭐ Frutas podridas |
| **Fruit Freshness (GitHub)** | ~5,000 | spoiled, overripe | Images + Annotations | ⭐ 3 niveles maduración |
| **Banana Ripeness (IEEE)** | 1,115 | underripe, overripe, spoiled | Images | ⭐ Maduración bananas |
| **ACFR Multifruit** | 3,704 | - | Object Detection | Detección general |
| **Fruits 360** | 166,293 | overripe (parcial) | Classification | Tipos de frutas |
| **Fruit Disease (GTS)** | ~10,000 | spoiled, mold | Images | ⭐ Enfermedades |

---

## 🎯 RECOMENDACIÓN FINAL

### Opción A: Fresh & Rotten (Mendeley) + tus 8 fotos ⭐⭐⭐⭐⭐

**Mejor opción para HOY**

**Ventajas**:
- ✅ 12,335 imágenes de frutas frescas vs podridas
- ✅ Clases perfectas: fresh vs rotten
- ✅ Augmentation ya aplicado
- ✅ Gratis y fácil de descargar

**Cómo usarlo**:
```powershell
# 1. Descargar de Mendeley
# 2. Convertir a formato YOLO
cd scripts
python convert-mendeley-to-yolo.py --input "C:\path\to\mendeley-dataset" --output "mendeley-yolo"

# 3. Combinar con tus fotos
python combine-datasets.py --public-dataset "mendeley-yolo" --talos-photos "..\talos-inspection-photos" --output "combined-dataset"

# 4. Subir a S3
python upload-labeled-dataset.py --dataset-path "combined-dataset"

# 5. Entrenar
python launch-sagemaker-training.py
```

**Resultado**: 12,335+ imágenes para entrenar

---

### Opción B: Fruit Freshness (GitHub) + tus 8 fotos ⭐⭐⭐⭐

**Segunda mejor opción**

**Ventajas**:
- ✅ 3 niveles de maduración (fresh, normal, rotten)
- ✅ Ya en formato de detección
- ✅ Fácil de clonar desde GitHub

**Cómo usarlo**:
```bash
# 1. Clonar repo
git clone https://github.com/zijianchen98/Fruit-freshness-detection-dataset.git

# 2. Combinar con tus fotos
cd scripts
python combine-datasets.py --public-dataset "Fruit-freshness-detection-dataset" --talos-photos "..\talos-inspection-photos"

# 3. Subir y entrenar
python upload-labeled-dataset.py --dataset-path "combined-dataset"
python launch-sagemaker-training.py
```

---

### Opción C: Solo tus 8 fotos + augmentation ⭐⭐⭐

**Opción más rápida (2-3 horas)**

**Ventajas**:
- ✅ Más rápido
- ✅ Específico para tu caso
- ✅ Control total

**Desventajas**:
- ❌ Pocas imágenes (24 con augmentation)
- ❌ Menor precisión inicial

---

## 📥 GUÍA DE DESCARGA RÁPIDA

### Fresh & Rotten (Mendeley)

1. Ve a: https://data.mendeley.com/datasets/bdd69gyhv8
2. Click "Download" (botón azul)
3. Crea cuenta Mendeley (gratis)
4. Descarga ZIP (~2GB)
5. Descomprime

**Estructura esperada**:
```
fresh-rotten-fruits/
├── fresh_apple/
├── rotten_apple/
├── fresh_banana/
├── rotten_banana/
├── fresh_orange/
├── rotten_orange/
└── ...
```

---

### Fruit Freshness (GitHub)

```bash
git clone https://github.com/zijianchen98/Fruit-freshness-detection-dataset.git
cd Fruit-freshness-detection-dataset
```

**Estructura esperada**:
```
Fruit-freshness-detection-dataset/
├── train/
│   ├── fresh_apple/
│   ├── normal_apple/
│   ├── rotten_apple/
│   └── ...
└── test/
    └── ...
```

---

### Banana Ripeness (IEEE)

1. Ve a: https://ieee-dataport.org
2. Crea cuenta IEEE (gratis)
3. Busca "Banana Ripeness Stage"
4. Click "Download"
5. Descarga ZIP

---

## 🔄 Script de Conversión

Voy a crear un script para convertir estos datasets a formato YOLO:

**Archivo**: `scripts/convert-mendeley-to-yolo.py`

```python
"""
Convertir Fresh & Rotten Fruits (Mendeley) a formato YOLO
"""

import os
import shutil
from pathlib import Path

def convert_mendeley_to_yolo(input_path, output_path):
    # Mapeo de clases
    class_mapping = {
        'fresh_apple': 'fresh',
        'rotten_apple': 'spoiled',
        'fresh_banana': 'fresh',
        'rotten_banana': 'spoiled',
        'fresh_orange': 'fresh',
        'rotten_orange': 'spoiled',
        # ... más clases
    }
    
    # Crear estructura YOLO
    os.makedirs(f'{output_path}/train/images', exist_ok=True)
    os.makedirs(f'{output_path}/train/labels', exist_ok=True)
    
    # Procesar imágenes
    for class_folder in os.listdir(input_path):
        class_path = os.path.join(input_path, class_folder)
        if not os.path.isdir(class_path):
            continue
        
        for img_file in os.listdir(class_path):
            if img_file.endswith(('.jpg', '.png')):
                # Copiar imagen
                src = os.path.join(class_path, img_file)
                dst = f'{output_path}/train/images/{img_file}'
                shutil.copy2(src, dst)
                
                # Crear label (imagen completa = 1 objeto)
                label_file = f'{output_path}/train/labels/{Path(img_file).stem}.txt'
                with open(label_file, 'w') as f:
                    # Clase 0 (spoiled) o 1 (fresh)
                    class_id = 0 if 'rotten' in class_folder else 1
                    # Cajita completa: centro (0.5, 0.5), tamaño (1.0, 1.0)
                    f.write(f'{class_id} 0.5 0.5 1.0 1.0\n')
    
    print(f"✅ Conversión completa: {output_path}")
```

---

## 💰 COSTOS

| Dataset | Descarga | Almacenamiento S3 | Training | Total |
|---------|----------|-------------------|----------|-------|
| **Mendeley (12K imgs)** | Gratis | ~$0.30 | ~$1.50 | **~$2** |
| **GitHub (5K imgs)** | Gratis | ~$0.15 | ~$1.00 | **~$1** |
| **Tus 8 fotos** | Gratis | ~$0.01 | ~$0.88 | **~$1** |

---

## ⏱️ TIEMPO ESTIMADO

| Opción | Descarga | Conversión | Upload S3 | Training | Total |
|--------|----------|------------|-----------|----------|-------|
| **Mendeley** | 30 min | 15 min | 20 min | 3-4 horas | **5-6 horas** |
| **GitHub** | 10 min | 10 min | 15 min | 2-3 horas | **3-4 horas** |
| **Tus 8 fotos** | 0 min | 0 min | 5 min | 2-4 horas | **2-4 horas** |

---

## 🚀 PRÓXIMO PASO

### Para HOY (Opción Rápida):

**Usa tus 8 fotos + augmentation**
```powershell
cd scripts
python upload-dataset-to-s3.py
```
Luego etiqueta en Roboflow (1-2 horas)

### Para MEJOR PRECISIÓN (Opción Completa):

**Descarga Mendeley + tus 8 fotos**
1. Descarga: https://data.mendeley.com/datasets/bdd69gyhv8
2. Convierte a YOLO
3. Combina con tus fotos
4. Entrena

---

## ✅ CONCLUSIÓN

**SÍ encontré datasets perfectos** para tu caso:

1. ✅ **Fresh & Rotten Fruits** (12,335 imágenes) - PERFECTO
2. ✅ **Fruit Freshness** (5,000 imágenes) - MUY BUENO
3. ✅ **Banana Ripeness** (1,115 imágenes) - BUENO

**Recomendación**: 
- **HOY**: Tus 8 fotos (rápido, valida que funciona)
- **MAÑANA**: Descarga Mendeley (mejor precisión)

¿Cuál prefieres? 🚀
