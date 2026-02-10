# 🚀 Integración AWS Completa - Omni Inspector

## ✅ Lo que Tenemos

- ✅ App móvil completa (4 pantallas)
- ✅ Servicio AWS configurado (aws-service.ts)
- ✅ Dataset de 3,202 imágenes
- ✅ Scripts de análisis forense

## 🎯 Plan de Integración

### Fase 1: Configurar AWS Amplify (30 min)

```bash
cd mobile-app

# 1. Instalar dependencias
npm install aws-amplify @aws-amplify/react-native

# 2. Inicializar Amplify
amplify init

# 3. Agregar autenticación
amplify add auth

# 4. Agregar almacenamiento (S3)
amplify add storage

# 5. Agregar API
amplify add api

# 6. Desplegar
amplify push
```

### Fase 2: Configurar S3 para Fotos (15 min)

1. **Crear bucket:**
```bash
aws s3 mb s3://omni-inspector-photos --region us-east-1
```

2. **Configurar CORS:**
```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": []
  }
]
```

3. **Aplicar política:**
```bash
aws s3api put-bucket-cors --bucket omni-inspector-photos --cors-configuration file://cors.json
```

### Fase 3: Configurar Bedrock Nova Pro (20 min)

1. **Habilitar modelo en consola AWS:**
   - Ve a AWS Bedrock Console
   - Model access > Request access
   - Selecciona "Amazon Nova Pro"
   - Espera aprobación (instantánea)

2. **Crear función Lambda para análisis:**

```python
import boto3
import json
import base64

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    # Obtener fotos del evento
    photos = event['photos']
    
    # Preparar prompt para Nova Pro
    prompt = f"""
    Analiza estas {len(photos)} fotos de un contenedor de carga.
    
    Identifica:
    1. Daños visibles (tipo, severidad, ubicación)
    2. Estado del precinto
    3. Número de contenedor (OCR)
    4. Indicadores de fraude
    
    Responde en formato JSON.
    """
    
    # Llamar a Bedrock Nova Pro
    response = bedrock.invoke_model(
        modelId='us.amazon.nova-pro-v1:0',
        body=json.dumps({
            "prompt": prompt,
            "images": photos,
            "max_tokens": 2000,
            "temperature": 0.7
        })
    )
    
    result = json.loads(response['body'].read())
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```

3. **Crear API Gateway:**
```bash
aws apigateway create-rest-api --name OmniInspectorAPI --region us-east-1
```

### Fase 4: Entrenar Modelo en SageMaker (60 min)

1. **Subir dataset a S3:**
```bash
aws s3 sync Fruit-freshness-detection-dataset/ s3://omni-inspector-training/dataset/
```

2. **Crear notebook de entrenamiento:**
```python
import sagemaker
from sagemaker.pytorch import PyTorch

# Configuración
role = 'arn:aws:iam::ACCOUNT:role/SageMakerRole'
bucket = 'omni-inspector-training'

# Entrenar YOLOv11
estimator = PyTorch(
    entry_point='train.py',
    role=role,
    instance_type='ml.p3.2xlarge',
    instance_count=1,
    framework_version='2.0',
    py_version='py310',
    hyperparameters={
        'epochs': 50,
        'batch-size': 16,
        'img-size': 640
    }
)

estimator.fit({'training': f's3://{bucket}/dataset/'})
```

3. **Desplegar endpoint:**
```python
predictor = estimator.deploy(
    initial_instance_count=1,
    instance_type='ml.m5.xlarge',
    endpoint_name='omni-inspector-yolo-endpoint'
)
```

### Fase 5: Integrar en la App (30 min)

1. **Actualizar aws-config.ts** con los valores reales

2. **Implementar upload real en aws-service.ts:**
```typescript
import { Storage } from 'aws-amplify';

static async uploadPhoto(uri: string, inspectionId: string): Promise<string> {
  const response = await fetch(uri);
  const blob = await response.blob();
  
  const filename = `inspections/${inspectionId}/${Date.now()}.jpg`;
  
  const result = await Storage.put(filename, blob, {
    contentType: 'image/jpeg',
    level: 'private'
  });
  
  return result.key;
}
```

3. **Implementar llamada a Bedrock:**
```typescript
static async analyzeWithBedrock(photoUrls: string[]): Promise<any> {
  const response = await fetch(awsConfig.API.endpoints[0].endpoint + '/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${await Auth.currentSession().getIdToken().getJwtToken()}`
    },
    body: JSON.stringify({ photos: photoUrls })
  });
  
  return await response.json();
}
```

## 📊 Costos Estimados

### Desarrollo/Testing (por mes):
- **S3:** ~$1 (1000 fotos)
- **Bedrock Nova Pro:** ~$10 (100 análisis)
- **SageMaker Endpoint:** ~$70 (ml.m5.xlarge 24/7)
- **API Gateway:** ~$1 (1000 requests)
- **Lambda:** ~$0.20 (1000 invocaciones)
- **Total:** ~$82/mes

### Producción (por mes, 1000 inspecciones):
- **S3:** ~$5 (5000 fotos)
- **Bedrock Nova Pro:** ~$50 (500 análisis)
- **SageMaker:** ~$70 (endpoint siempre activo)
- **API Gateway:** ~$3.50
- **Lambda:** ~$1
- **Total:** ~$130/mes

## 🧪 Testing

### Probar en Web (Desarrollo):
```bash
cd mobile-app
npm start
# Presiona 'w' para abrir en navegador
```

### Probar con Expo Go:
```bash
npm start
# Escanea QR con Expo Go
```

### Probar con Android Studio:
```bash
npx expo run:android
```

## 📝 Próximos Pasos

1. ✅ Descargar Android Studio (en progreso)
2. ⏳ Configurar AWS Amplify
3. ⏳ Subir dataset a S3
4. ⏳ Entrenar modelo en SageMaker
5. ⏳ Desplegar Lambda + API Gateway
6. ⏳ Integrar todo en la app
7. ⏳ Generar APK con Android Studio

## 🆘 Troubleshooting

### Error: "Amplify not configured"
```typescript
import { Amplify } from 'aws-amplify';
import awsconfig from './aws-exports';

Amplify.configure(awsconfig);
```

### Error: "S3 upload failed"
- Verificar permisos del bucket
- Verificar CORS configurado
- Verificar credenciales AWS

### Error: "Bedrock access denied"
- Verificar que el modelo esté habilitado
- Verificar permisos IAM
- Verificar región correcta

## 🎯 Estado Actual

- ✅ App móvil: 100%
- ⏳ Integración AWS: 30%
- ⏳ Modelo entrenado: 0%
- ⏳ APK: En progreso (Android Studio)
