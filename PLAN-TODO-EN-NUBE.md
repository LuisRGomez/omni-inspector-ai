# Plan: TODO en la Nube (AWS)

> **Objetivo**: Fine-tuning y detección 100% en AWS  
> **Costo**: ~$10-20 para fine-tuning, ~$2/mes operación  
> **Tiempo**: 2-3 horas setup, 2-4 horas entrenamiento

---

## 🎯 Arquitectura 100% Cloud

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub (Código)                          │
│  • Dataset (anotaciones)                                    │
│  • Scripts de entrenamiento                                 │
│  • Configuración                                            │
└────────────────────┬────────────────────────────────────────┘
                     │ GitHub Actions (CI/CD)
┌────────────────────┴────────────────────────────────────────┐
│                    AWS S3                                   │
│  • Dataset (imágenes + labels)                              │
│  • Modelos entrenados                                       │
│  • Checkpoints                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                    SageMaker Training Job                   │
│  • Instancia: ml.g4dn.xlarge (GPU)                          │
│  • Entrenamiento: YOLOv11 fine-tuning                       │
│  • Duración: 2-4 horas                                      │
│  • Output: Modelo mejorado → S3                             │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                    SageMaker Endpoint                       │
│  • Tipo: Serverless                                         │
│  • Modelo: YOLOv11 fine-tuned                               │
│  • Inferencia: < 1s por imagen                              │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                    App Móvil                                │
│  • Captura foto                                             │
│  • Envía a API Gateway                                      │
│  • Recibe detecciones                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Paso a Paso

### Paso 1: Preparar Dataset en S3 (30 minutos)

**1.1. Subir fotos de Talos a S3**

```python
# upload_dataset.py
import boto3
import glob
from pathlib import Path

s3 = boto3.client('s3')
bucket = 'omni-inspector-models-472661249377'

# Subir fotos de Talos
for img_path in glob.glob('../talos-inspection-photos/*.jpg'):
    key = f'datasets/talos-v1/images/{Path(img_path).name}'
    s3.upload_file(img_path, bucket, key)
    print(f"✅ Uploaded: {key}")
```

**1.2. Crear anotaciones (usando Roboflow o manual)**

Opciones:
- **A) Roboflow** (recomendado): Etiquetar online, exportar a S3
- **B) LabelStudio en EC2**: Instancia temporal para etiquetar
- **C) Ground Truth**: Servicio de AWS para etiquetado (más caro)

**1.3. Estructura en S3**

```
s3://omni-inspector-models-472661249377/
└── datasets/
    └── talos-v1/
        ├── train/
        │   ├── images/
        │   │   ├── img1.jpg
        │   │   └── img2.jpg
        │   └── labels/
        │       ├── img1.txt
        │       └── img2.txt
        ├── val/
        │   ├── images/
        │   └── labels/
        └── data.yaml
```

---

### Paso 2: SageMaker Training Job (2-4 horas)

**2.1. Crear script de entrenamiento**

```python
# sagemaker_train.py
# Este script se ejecuta EN SageMaker (en la nube)

import os
import argparse
from ultralytics import YOLO

def train():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='/opt/ml/input/data/training/data.yaml')
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--batch', type=int, default=16)
    parser.add_argument('--imgsz', type=int, default=640)
    args = parser.parse_args()
    
    # Cargar modelo base
    model = YOLO('yolov11n.pt')
    
    # Entrenar
    results = model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=0,  # GPU
        
        # Augmentation
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=20,
        translate=0.2,
        scale=0.9,
        shear=5,
        flipud=0.5,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.15,
    )
    
    # Guardar modelo
    model.save('/opt/ml/model/best.pt')
    
    # Evaluar
    metrics = model.val()
    print(f"mAP50: {metrics.box.map50:.3f}")
    print(f"mAP50-95: {metrics.box.map:.3f}")

if __name__ == '__main__':
    train()
```

**2.2. Crear Training Job**

```python
# launch_training.py
import boto3
import sagemaker
from sagemaker.pytorch import PyTorch

# Configuración
role = 'arn:aws:iam::472661249377:role/OmniInspectorSageMakerRole'
bucket = 'omni-inspector-models-472661249377'

# Crear estimator
estimator = PyTorch(
    entry_point='sagemaker_train.py',
    role=role,
    instance_type='ml.g4dn.xlarge',  # GPU
    instance_count=1,
    framework_version='2.0.0',
    py_version='py310',
    
    hyperparameters={
        'epochs': 100,
        'batch': 16,
        'imgsz': 640
    },
    
    output_path=f's3://{bucket}/models/yolo-finetuned/',
    
    # Usar Spot Instances (70% más barato)
    use_spot_instances=True,
    max_run=14400,  # 4 horas
    max_wait=18000,  # 5 horas
)

# Iniciar entrenamiento
estimator.fit({
    'training': f's3://{bucket}/datasets/talos-v1/'
})

print(f"✅ Training job iniciado")
print(f"   Job name: {estimator.latest_training_job.name}")
print(f"   Monitorear en: https://console.aws.amazon.com/sagemaker/")
```

**Costo estimado**:
- ml.g4dn.xlarge: $0.736/hora
- Spot instance (70% descuento): ~$0.22/hora
- 4 horas entrenamiento: ~$0.88
- **Total: < $1** 🎉

---

### Paso 3: Desplegar Modelo Fine-tuned (15 minutos)

```python
# deploy_finetuned.py
import boto3
import sagemaker

# Obtener modelo entrenado
s3_model_path = 's3://omni-inspector-models-472661249377/models/yolo-finetuned/model.tar.gz'

# Crear modelo en SageMaker
sagemaker_client = boto3.client('sagemaker')

model_name = 'omni-inspector-yolo-finetuned-v1'

sagemaker_client.create_model(
    ModelName=model_name,
    PrimaryContainer={
        'Image': '763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:2.0.0-cpu-py310',
        'ModelDataUrl': s3_model_path,
        'Environment': {
            'SAGEMAKER_PROGRAM': 'inference.py',
            'SAGEMAKER_SUBMIT_DIRECTORY': s3_model_path
        }
    },
    ExecutionRoleArn='arn:aws:iam::472661249377:role/OmniInspectorSageMakerRole'
)

# Crear endpoint config (serverless)
config_name = f'{model_name}-config'

sagemaker_client.create_endpoint_config(
    EndpointConfigName=config_name,
    ProductionVariants=[{
        'VariantName': 'AllTraffic',
        'ModelName': model_name,
        'ServerlessConfig': {
            'MemorySizeInMB': 2048,
            'MaxConcurrency': 5
        }
    }]
)

# Crear endpoint
endpoint_name = 'omni-inspector-yolo'

sagemaker_client.create_endpoint(
    EndpointName=endpoint_name,
    EndpointConfigName=config_name
)

print(f"✅ Endpoint desplegando: {endpoint_name}")
print(f"   Espera 5-10 minutos...")
```

---

### Paso 4: GitHub Actions para CI/CD (Opcional)

```yaml
# .github/workflows/train-model.yml
name: Train YOLO Model

on:
  workflow_dispatch:  # Manual trigger
    inputs:
      epochs:
        description: 'Number of epochs'
        required: true
        default: '100'

jobs:
  train:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Upload dataset to S3
        run: |
          aws s3 sync ./dataset s3://omni-inspector-models-472661249377/datasets/talos-v1/
      
      - name: Launch SageMaker Training
        run: |
          python scripts/launch_training.py --epochs ${{ github.event.inputs.epochs }}
      
      - name: Wait for training
        run: |
          python scripts/wait_for_training.py
      
      - name: Deploy model
        run: |
          python scripts/deploy_finetuned.py
```

---

## 🎓 Etiquetado del Dataset

### Opción A: Roboflow (Recomendado - Cloud)

1. **Crear cuenta**: https://roboflow.com
2. **Crear proyecto**: "Omni-Inspector"
3. **Subir fotos**: 8 fotos de Talos
4. **Etiquetar**:
   - Dibujar cajitas sobre daños
   - Asignar clases:
     - `dent` (abolladura)
     - `dirt` (suciedad) ← CRÍTICO
     - `rust` (óxido)
     - `scratch` (rayadura)
     - `spoiled` (podrido)
     - `mold` (moho)
5. **Augmentation**: Generar 100+ variaciones
6. **Exportar**: Formato YOLOv11
7. **Descargar** y subir a S3

**Tiempo**: 30-60 minutos

---

### Opción B: Ground Truth (AWS - Más caro)

```python
# create_labeling_job.py
import boto3

sagemaker = boto3.client('sagemaker')

sagemaker.create_labeling_job(
    LabelingJobName='omni-inspector-labeling-v1',
    LabelAttributeName='labels',
    InputConfig={
        'DataSource': {
            'S3DataSource': {
                'ManifestS3Uri': 's3://omni-inspector-models-472661249377/datasets/manifest.json'
            }
        }
    },
    OutputConfig={
        'S3OutputPath': 's3://omni-inspector-models-472661249377/datasets/labeled/'
    },
    RoleArn='arn:aws:iam::472661249377:role/OmniInspectorSageMakerRole',
    LabelCategoryConfigS3Uri='s3://omni-inspector-models-472661249377/datasets/label-categories.json',
    HumanTaskConfig={
        'WorkteamArn': 'arn:aws:sagemaker:us-east-1:394669845002:workteam/public-crowd/default',
        'UiConfig': {
            'UiTemplateS3Uri': 's3://omni-inspector-models-472661249377/datasets/ui-template.html'
        },
        'PreHumanTaskLambdaArn': 'arn:aws:lambda:us-east-1:432418664414:function:PRE-BoundingBox',
        'TaskTitle': 'Etiquetar daños en contenedores',
        'TaskDescription': 'Dibuja cajitas sobre daños visibles',
        'NumberOfHumanWorkersPerDataObject': 1,
        'TaskTimeLimitInSeconds': 600,
        'TaskAvailabilityLifetimeInSeconds': 864000,
        'MaxConcurrentTaskCount': 10,
        'AnnotationConsolidationConfig': {
            'AnnotationConsolidationLambdaArn': 'arn:aws:lambda:us-east-1:432418664414:function:ACS-BoundingBox'
        },
        'PublicWorkforceTaskPrice': {
            'AmountInUsd': {
                'Dollars': 0,
                'Cents': 12,
                'TenthFractionsOfACent': 0
            }
        }
    }
)
```

**Costo**: ~$0.12 por imagen (crowd workers)

---

## 💰 Costos Totales

### Setup Inicial (Una vez)
| Servicio | Costo |
|----------|-------|
| Etiquetado (Roboflow) | Gratis (hasta 1,000 imágenes) |
| Etiquetado (Ground Truth) | ~$1 (8 imágenes × $0.12) |
| SageMaker Training (Spot) | ~$1 (4 horas × $0.22/hora) |
| S3 Storage | ~$0.01 |
| **Total** | **~$2** |

### Operación Mensual (1,000 inspecciones)
| Servicio | Costo |
|----------|-------|
| SageMaker Endpoint | $0.03 |
| Bedrock (Nova) | $2.00 |
| Lambda | $0.40 |
| DynamoDB | $1.75 |
| S3 | $0.10 |
| **Total** | **$4.28/mes** |

---

## 🚀 Plan de Acción HOY

### Ahora - 1:00 PM
- [ ] Subir fotos de Talos a S3
- [ ] Crear cuenta en Roboflow
- [ ] Empezar a etiquetar

### 1:00 PM - 2:00 PM
- [ ] Terminar etiquetado (8 fotos)
- [ ] Generar augmentation (100+ imágenes)
- [ ] Exportar dataset

### 2:00 PM - 2:30 PM
- [ ] Subir dataset a S3
- [ ] Crear script de entrenamiento
- [ ] Configurar SageMaker Training Job

### 2:30 PM - 6:30 PM
- [ ] Lanzar Training Job (4 horas)
- [ ] Monitorear progreso
- [ ] Mientras tanto: trabajar en app móvil

### 6:30 PM - 7:00 PM
- [ ] Desplegar modelo fine-tuned
- [ ] Probar endpoint
- [ ] Validar mejoras

---

## ✅ Checklist

- [ ] Fotos en S3
- [ ] Dataset etiquetado
- [ ] Training Job configurado
- [ ] Training Job ejecutado
- [ ] Modelo desplegado
- [ ] Endpoint funcionando
- [ ] Detección mejorada validada

---

## 📞 Comandos Útiles

```bash
# Subir dataset a S3
aws s3 sync ./dataset s3://omni-inspector-models-472661249377/datasets/talos-v1/

# Listar training jobs
aws sagemaker list-training-jobs --region us-east-1

# Ver logs de training
aws logs tail /aws/sagemaker/TrainingJobs --follow

# Verificar endpoint
aws sagemaker describe-endpoint --endpoint-name omni-inspector-yolo

# Invocar endpoint
aws sagemaker-runtime invoke-endpoint \
  --endpoint-name omni-inspector-yolo \
  --body fileb://test-image.jpg \
  --content-type image/jpeg \
  output.json
```

---

**¿Empezamos con el etiquetado en Roboflow?** 🚀

Te puedo guiar paso a paso mientras etiquetas las 8 fotos.
