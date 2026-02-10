# Setup AWS Completo - Guía Paso a Paso

> **Objetivo**: Activar Fase 2 (YOLO + SageMaker) y Fase 3 (Nova + Bedrock)  
> **Tiempo estimado**: 45-60 minutos  
> **Costo**: ~$2-3/mes para 1,000 inspecciones

---

## 🔐 Paso 1: Configurar Credenciales AWS (15 minutos)

### Problema Actual
Tus credenciales AWS tienen un error de firma. Necesitas reconfigurarlas.

### Solución

**Opción A: Reconfigurar credenciales (Recomendado)**

1. Ve a AWS Console: https://console.aws.amazon.com/
2. Click en tu nombre (arriba derecha) → Security Credentials
3. En "Access keys" → Create access key
4. Guarda el Access Key ID y Secret Access Key

**Luego ejecuta:**
```powershell
# Eliminar credenciales antiguas
Remove-Item Env:AWS_ACCESS_KEY_ID
Remove-Item Env:AWS_SECRET_ACCESS_KEY

# Configurar nuevas credenciales
aws configure

# Cuando te pregunte:
# AWS Access Key ID: [pega tu nuevo Access Key]
# AWS Secret Access Key: [pega tu nuevo Secret Key]
# Default region name: us-east-1
# Default output format: json
```

**Verificar:**
```powershell
aws sts get-caller-identity
```

Deberías ver algo como:
```json
{
    "UserId": "AIDAXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/tu-usuario"
}
```

---

## 🧠 Paso 2: Habilitar Amazon Bedrock (15 minutos)

### ¿Qué es Bedrock?
Amazon Bedrock es el servicio de AWS que da acceso a modelos de IA como Nova (de Amazon), Claude (Anthropic), etc.

### Habilitar Modelos Nova

**Opción A: Desde AWS Console (Más fácil)**

1. Ve a: https://console.aws.amazon.com/bedrock/
2. En el menú izquierdo → **Model access**
3. Click en **Manage model access** (botón naranja)
4. Busca y habilita:
   - ✅ **Amazon Nova Lite** (rápido, barato)
   - ✅ **Amazon Nova Pro** (más inteligente)
5. Click **Save changes**
6. Espera 2-5 minutos (aprobación automática)

**Opción B: Desde CLI**
```powershell
# Verificar modelos disponibles
aws bedrock list-foundation-models --region us-east-1 --query "modelSummaries[?contains(modelId, 'nova')]"

# Nota: La habilitación de modelos solo se puede hacer desde la consola
```

**Verificar acceso:**
```powershell
aws bedrock list-foundation-models --region us-east-1 --query "modelSummaries[?contains(modelId, 'nova')].{ModelId:modelId, Name:modelName}" --output table
```

Deberías ver:
```
---------------------------------------------------------
|              ListFoundationModels                     |
+----------------------------------+--------------------+
|            ModelId               |       Name         |
+----------------------------------+--------------------+
|  amazon.nova-lite-v1:0           |  Nova Lite         |
|  amazon.nova-pro-v1:0            |  Nova Pro          |
+----------------------------------+--------------------+
```

---

## 🎯 Paso 3: Desplegar SageMaker Endpoint (30 minutos)

### ¿Qué es SageMaker?
SageMaker es el servicio de AWS para ejecutar modelos de Machine Learning. Usaremos **SageMaker Serverless** para YOLO.

### Opción A: Despliegue Automático (Recomendado)

**1. Verificar permisos IAM**
```powershell
# Verificar que tu usuario tiene permisos de SageMaker
aws iam get-user
```

**2. Ejecutar script de setup**
```powershell
cd yolo-detection
python setup_sagemaker.py
```

Este script:
- ✅ Crea rol IAM para SageMaker
- ✅ Crea bucket S3 para modelos
- ✅ Descarga YOLOv11
- ✅ Sube modelo a S3
- ✅ Crea endpoint serverless
- ✅ Guarda configuración

**Tiempo**: ~20-30 minutos (la mayoría es subida del modelo)

---

### Opción B: Despliegue Manual (Si el script falla)

**1. Crear rol IAM**
```powershell
# Crear política de confianza
@"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "sagemaker.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
"@ | Out-File -FilePath trust-policy.json

# Crear rol
aws iam create-role --role-name OmniInspectorSageMakerRole --assume-role-policy-document file://trust-policy.json

# Adjuntar políticas
aws iam attach-role-policy --role-name OmniInspectorSageMakerRole --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess
aws iam attach-role-policy --role-name OmniInspectorSageMakerRole --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
```

**2. Crear bucket S3**
```powershell
aws s3 mb s3://omni-inspector-models-$(aws sts get-caller-identity --query Account --output text)
```

**3. Descargar y preparar YOLOv11**
```powershell
# Instalar ultralytics
pip install ultralytics

# Descargar modelo
python -c "from ultralytics import YOLO; model = YOLO('yolov11n.pt'); model.export(format='torchscript')"
```

**4. Subir modelo a S3**
```powershell
aws s3 cp yolov11n.torchscript s3://omni-inspector-models-ACCOUNT_ID/yolo/model.tar.gz
```

**5. Crear endpoint (desde consola)**
- Ve a: https://console.aws.amazon.com/sagemaker/
- Models → Create model
- Endpoints → Create endpoint configuration (Serverless)
- Create endpoint

---

## 🧪 Paso 4: Probar Todo (10 minutos)

### Probar Bedrock (Fase 3)

```powershell
cd nova-reasoning

# Test básico
python cli.py test --image ..\talos-inspection-photos\20260207_091519.jpg

# Test de análisis completo (requiere S3)
python cli.py analyze `
  --case-id TEST-001 `
  --forensic-report ..\forensic-detective\test_forensic.json `
  --yolo-report ..\yolo-detection\test_yolo.json `
  --image s3://tu-bucket/test.jpg `
  --module claims `
  --output analysis.json
```

**Resultado esperado:**
```
Testing Nova Reasoning Layer

1. Initializing Nova analyzer...
✓ Analyzer initialized

2. Initializing fraud detector...
✓ Fraud detector initialized

3. Initializing report generator...
✓ Report generator initialized

All tests passed!
```

---

### Probar SageMaker (Fase 2)

```powershell
cd yolo-detection

# Test de detección
python cli.py detect ..\talos-inspection-photos\20260207_091519.jpg --output test_yolo.json
```

**Resultado esperado:**
```
======================================================================
YOLO DETECTION REPORT
======================================================================

📁 Image: file://..\talos-inspection-photos\20260207_091519.jpg
📐 Dimensions: 4000x3000
⏱️  Inference Time: 850ms

🎯 DETECTIONS:
   1. dent (medium) - Confidence: 0.87
   2. rust (low) - Confidence: 0.65

📊 SUMMARY:
   Total Detections: 2
   Critical Issues: 0
   Overall Severity: medium

======================================================================
```

---

### Probar Pipeline Completo

```powershell
# Ejecutar script automatizado
.\test-complete-pipeline.ps1
```

**Resultado esperado:**
```
🚀 Testing complete pipeline for case: TEST-20260209-120000

📋 Phase 1: Forensic analysis...
✅ Phase 1 complete

🎯 Phase 2: YOLO detection...
✅ Phase 2 complete

🧠 Phase 3: Nova reasoning...
✅ Phase 3 complete

📄 Generating report...
✅ Report generated

🎉 Complete pipeline test successful!

📊 Results:
   - Verdict: APPROVED
   - Confidence: 87.5%
   - Fraud Score: 12.3%
   - Risk Score: 3.2/10
   - Damages: 2
   - Processing Time: 8,234ms
```

---

## 💰 Costos Estimados

### Setup (Una vez)
- Crear recursos: **$0.00** (gratis)
- Subir modelo a S3: **$0.00** (< 1GB)

### Operación (Mensual, 1,000 inspecciones)

| Servicio | Costo |
|----------|-------|
| **Bedrock (Nova Pro)** | $2.00 |
| **SageMaker Serverless** | $0.03 |
| **S3 Storage** | $0.10 |
| **Lambda** (Fase 4) | $0.40 |
| **DynamoDB** (Fase 4) | $1.75 |
| **Total** | **$4.28/mes** |

**Costo por inspección**: $0.004 (menos de medio centavo)

---

## 🎓 Preguntas Frecuentes

### ¿Necesito entrenar YOLOv11 con mis fotos?

**No, para empezar.** YOLOv11 base ya detecta:
- Objetos generales (contenedores, vehículos)
- Daños visibles (abolladuras, grietas, óxido)
- Anomalías estructurales

**Sí, para mejorar.** Después puedes hacer fine-tuning con tus fotos de Talos para:
- Mejorar precisión en contenedores específicos
- Detectar daños particulares de tu industria
- Reducir falsos positivos

**Proceso de fine-tuning** (opcional, después):
1. Etiquetar 500-1,000 fotos (usar LabelStudio o Roboflow)
2. Entrenar modelo personalizado (SageMaker Training Job)
3. Desplegar nuevo modelo (reemplazar endpoint)

**Costo**: ~$10-20 por entrenamiento

---

### ¿Bedrock necesita entrenamiento?

**No.** Bedrock con Nova es un servicio **ya entrenado** por Amazon. Solo lo habilitas y usas.

Nova ya sabe:
- Analizar imágenes
- Detectar fraude
- Generar reportes
- Razonamiento multimodal

---

### ¿Qué pasa si no tengo acceso a Bedrock?

Algunas cuentas AWS nuevas requieren aprobación manual para Bedrock. Si ves "Access denied":

1. Ve a Bedrock Console
2. Click "Request access"
3. Llena formulario (2 minutos)
4. Espera aprobación (24-48 horas)

Mientras tanto, puedes usar **Fase 1 y 2** sin problemas.

---

### ¿Puedo usar otro modelo en vez de Nova?

**Sí.** Bedrock soporta varios modelos:
- **Claude 3** (Anthropic) - Muy bueno para razonamiento
- **Llama 3** (Meta) - Open source, más barato
- **Titan** (Amazon) - Alternativa a Nova

Solo cambia el `model_id` en `nova_analyzer.py`:
```python
analyzer = NovaAnalyzer(model='anthropic.claude-3-sonnet-20240229-v1:0')
```

---

## 🚨 Troubleshooting

### Error: "SignatureDoesNotMatch"
**Causa**: Credenciales AWS incorrectas o expiradas  
**Solución**: Reconfigurar credenciales (Paso 1)

### Error: "Access Denied" en Bedrock
**Causa**: Modelos no habilitados  
**Solución**: Habilitar modelos en Bedrock Console (Paso 2)

### Error: "Endpoint not found" en SageMaker
**Causa**: Endpoint no desplegado  
**Solución**: Ejecutar `setup_sagemaker.py` (Paso 3)

### Error: "No module named 'ultralytics'"
**Causa**: Dependencias no instaladas  
**Solución**: `pip install ultralytics`

### Error: "Insufficient permissions"
**Causa**: Usuario IAM sin permisos  
**Solución**: Agregar políticas:
```powershell
aws iam attach-user-policy --user-name TU_USUARIO --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess
aws iam attach-user-policy --user-name TU_USUARIO --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
```

---

## ✅ Checklist de Verificación

Antes de continuar, verifica:

- [ ] Credenciales AWS configuradas correctamente
- [ ] `aws sts get-caller-identity` funciona
- [ ] Bedrock habilitado (Nova Lite y Pro)
- [ ] SageMaker endpoint desplegado
- [ ] Fase 1 probada (forensic)
- [ ] Fase 2 probada (YOLO)
- [ ] Fase 3 probada (Nova)
- [ ] Pipeline completo funciona

---

## 📞 Soporte

**Documentación AWS:**
- [Bedrock Getting Started](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html)
- [SageMaker Serverless](https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html)
- [IAM Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)

**Documentación del Proyecto:**
- [TEST-RESULTS.md](TEST-RESULTS.md) - Resultados de pruebas
- [NEXT-ACTIONS.md](NEXT-ACTIONS.md) - Próximos pasos
- [PHASE-2-COMPLETE.md](PHASE-2-COMPLETE.md) - Documentación YOLO
- [PHASE-3-COMPLETE.md](PHASE-3-COMPLETE.md) - Documentación Nova

---

**Proyecto**: Omni-Inspector AI  
**Objetivo**: Sistema 100% funcional en AWS  
**Tiempo**: 45-60 minutos  
**Resultado**: Pipeline completo operativo
