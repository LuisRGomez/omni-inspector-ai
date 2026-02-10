# 🚀 Cómo Usar los Datasets Descargados

---

## ✅ Datasets que Descargaste

1. **Mendeley - Fresh & Rotten Fruits** (12,335 imágenes)
2. **GitHub - Fruit Freshness Detection** (~5,000 imágenes)

---

## 📋 PASO A PASO

### Paso 1: Esperar a que Terminen de Descargar

**Mendeley**:
- Archivo: `fresh-rotten-fruits.zip` (~2GB)
- Ubicación: Carpeta de descargas

**GitHub**:
- Carpeta: `Fruit-freshness-detection-dataset/`
- Ubicación: Donde ejecutaste `git clone`

---

### Paso 2: Descomprimir Mendeley

```powershell
# Si está en Downloads
cd C:\Users\TU_USUARIO\Downloads

# Descomprimir (usa 7-Zip o WinRAR)
# O en PowerShell:
Expand-Archive -Path fresh-rotten-fruits.zip -DestinationPath fresh-rotten-fruits
```

**Estructura esperada**:
```
fresh-rotten-fruits/
├── fresh_apple/
│   ├── img1.jpg
│   ├── img2.jpg
│   └── ...
├── rotten_apple/
├── fresh_banana/
├── rotten_banana/
└── ...
```

---

### Paso 3: Convertir a Formato YOLO

**Mendeley**:
```powershell
cd C:\path\to\omni-inspector\scripts
python convert-classification-to-yolo.py --input "C:\Users\TU_USUARIO\Downloads\fresh-rotten-fruits" --output "mendeley-yolo"
```

**GitHub**:
```powershell
python convert-classification-to-yolo.py --input "C:\path\to\Fruit-freshness-detection-dataset" --output "github-yolo"
```

**Resultado**: Datasets convertidos a formato YOLO con cajitas

---

### Paso 4: Combinar con tus Fotos de Talos

```powershell
# Opción A: Solo Mendeley + Talos
python combine-datasets.py --public-dataset "mendeley-yolo" --talos-photos "..\talos-inspection-photos" --output "combined-dataset"

# Opción B: Mendeley + GitHub + Talos (MEJOR)
python combine-multiple-datasets.py --datasets "mendeley-yolo,github-yolo" --talos-photos "..\talos-inspection-photos" --output "combined-dataset"
```

**Resultado**: Dataset combinado con 17,000+ imágenes

---

### Paso 5: Subir a S3

```powershell
python upload-labeled-dataset.py --dataset-path "combined-dataset"
```

**Resultado**: Dataset en S3 listo para entrenar

---

### Paso 6: Lanzar Training Job

```powershell
python launch-sagemaker-training.py
```

**Configuración**:
- Instance: ml.g4dn.xlarge (GPU)
- Epochs: 100
- Batch: 16
- Duración: 3-5 horas (más datos = más tiempo)
- Costo: ~$1.50 USD

---

### Paso 7: Esperar (3-5 horas)

Mientras entrena:
- ☕ Toma café
- 📱 Trabaja en diseño de app móvil
- 📊 Monitorea en AWS Console

---

### Paso 8: Desplegar Modelo

```powershell
python deploy-finetuned-model.py
```

**Resultado**: Modelo mejorado desplegado

---

### Paso 9: Probar

```powershell
cd ..\yolo-detection
python cli.py detect ..\talos-inspection-photos\20260207_091519.jpg --use-finetuned
```

**Resultado esperado**:
```
🎯 DETECTIONS (17,000+ imágenes entrenadas):
   1. spoiled (high) - 95% - [100, 200, 300, 400]
   2. overripe (medium) - 88% - [500, 100, 600, 250]
   3. bruise (low) - 82% - [700, 300, 800, 450]

📊 MEJORAS vs MODELO BASE:
   ✅ Detecta spoiled con 95% confianza
   ✅ Diferencia overripe vs spoiled
   ✅ Detecta bruise correctamente
   ✅ Menos falsos positivos
```

---

## ⏱️ TIMELINE

```
Ahora     - Descargas terminando
+10 min   - Descomprimir Mendeley
+15 min   - Convertir a YOLO (Mendeley)
+10 min   - Convertir a YOLO (GitHub)
+15 min   - Combinar con Talos
+20 min   - Subir a S3
+5 min    - Lanzar training
+3-5 hrs  - Training en AWS
+15 min   - Desplegar modelo
+10 min   - Probar
─────────────────────────────
Total: ~5-7 horas (mayoría esperando)
```

---

## 💰 COSTOS

| Concepto | Costo |
|----------|-------|
| Descargas | Gratis |
| S3 Storage (17K imgs) | ~$0.50 |
| SageMaker Training | ~$1.50 |
| **Total** | **~$2 USD** |

---

## 🎯 COMPARACIÓN

| Opción | Imágenes | Tiempo | Precisión | Costo |
|--------|----------|--------|-----------|-------|
| **Solo 8 fotos** | 24 | 2-3 hrs | Media | $1 |
| **Mendeley + Talos** | 12,335 | 5-6 hrs | Alta | $2 |
| **Mendeley + GitHub + Talos** | 17,335 | 6-7 hrs | Muy Alta | $2 |

---

## ⚠️ IMPORTANTE

### Mientras Descargan

**NO esperes sin hacer nada**. Puedes:

1. **Continuar etiquetando en Roboflow**
   - Tus 8 fotos son valiosas
   - Específicas para tu caso
   - Combínalas después con los datasets

2. **Preparar ambiente**
   - Verificar que Python tiene PIL: `pip install Pillow`
   - Verificar espacio en disco (necesitas ~5GB)

3. **Leer documentación**
   - `FASE-4-ESPECIFICACION-COMPLETA.md`
   - Diseñar UI de app móvil

---

## 🚨 PROBLEMAS COMUNES

### Error: "No module named 'PIL'"
```powershell
pip install Pillow
```

### Error: "Permission denied"
```powershell
# Ejecuta PowerShell como Administrador
```

### Error: "Out of disk space"
```powershell
# Libera espacio (necesitas ~5GB)
# O usa disco externo
```

### Conversión muy lenta
```powershell
# Es normal, 17,000 imágenes toman 15-20 minutos
# Verás progreso cada 100 imágenes
```

---

## 📞 COMANDOS RÁPIDOS

```powershell
# 1. Convertir Mendeley
cd scripts
python convert-classification-to-yolo.py --input "C:\path\to\fresh-rotten-fruits" --output "mendeley-yolo"

# 2. Convertir GitHub
python convert-classification-to-yolo.py --input "C:\path\to\Fruit-freshness-detection-dataset" --output "github-yolo"

# 3. Combinar todo
python combine-datasets.py --public-dataset "mendeley-yolo" --talos-photos "..\talos-inspection-photos" --output "combined-dataset"

# 4. Subir a S3
python upload-labeled-dataset.py --dataset-path "combined-dataset"

# 5. Entrenar
python launch-sagemaker-training.py

# 6. Esperar 3-5 horas...

# 7. Desplegar
python deploy-finetuned-model.py

# 8. Probar
cd ..\yolo-detection
python cli.py detect ..\talos-inspection-photos\20260207_091519.jpg --use-finetuned
```

---

## ✅ CHECKLIST

- [ ] Mendeley descargado
- [ ] GitHub clonado
- [ ] Mendeley descomprimido
- [ ] Mendeley convertido a YOLO
- [ ] GitHub convertido a YOLO
- [ ] Datasets combinados con Talos
- [ ] Dataset subido a S3
- [ ] Training job lanzado
- [ ] Training completado (3-5 horas)
- [ ] Modelo desplegado
- [ ] Modelo probado

---

## 🎯 PRÓXIMO PASO

**Espera a que terminen las descargas** (~10-30 minutos)

Luego ejecuta:
```powershell
cd scripts
python convert-classification-to-yolo.py --input "C:\path\to\fresh-rotten-fruits" --output "mendeley-yolo"
```

**¿Necesitas ayuda?** Avísame cuando terminen de descargar! 🚀
