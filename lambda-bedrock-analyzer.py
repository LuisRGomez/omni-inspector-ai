import boto3
import json
import base64
from datetime import datetime

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    Analiza fotos de inspección usando Bedrock Nova Pro
    """
    try:
        # Obtener datos del evento
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event
        
        photo_keys = body.get('photos', [])
        inspection_data = body.get('inspection', {})
        
        if not photo_keys:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No photos provided'})
            }
        
        # Descargar fotos de S3 y convertir a base64
        images_base64 = []
        for key in photo_keys[:5]:  # Máximo 5 fotos
            try:
                response = s3.get_object(Bucket='omni-inspector-photos-prod', Key=key)
                image_data = response['Body'].read()
                images_base64.append(base64.b64encode(image_data).decode('utf-8'))
            except Exception as e:
                print(f"Error loading image {key}: {e}")
        
        # Preparar prompt para Nova Pro
        prompt = f"""
Eres un inspector forense experto analizando un contenedor de carga.

DATOS DE LA INSPECCIÓN:
- Contenedor: {inspection_data.get('containerNumber', 'N/A')}
- Precinto: {inspection_data.get('sealNumber', 'N/A')}
- Ubicación: {inspection_data.get('location', 'N/A')}
- Módulo: {inspection_data.get('module', 'N/A')}

TAREA:
Analiza las {len(images_base64)} fotos proporcionadas e identifica:

1. DAÑOS VISIBLES:
   - Tipo de daño (abolladura, óxido, rotura, etc.)
   - Severidad (Leve, Media, Alta)
   - Ubicación exacta
   - Confianza del análisis (0-1)

2. ESTADO DEL PRECINTO:
   - ¿Está intacto? (true/false)
   - ¿Hay signos de manipulación?

3. NÚMERO DE CONTENEDOR:
   - Extrae el número visible (OCR)
   - ¿Coincide con el declarado?

4. DETECCIÓN DE FRAUDE:
   - Score de fraude (0-1, donde 1 es fraude seguro)
   - Indicadores sospechosos
   - Recomendación

5. ANÁLISIS GENERAL:
   - Resumen de la inspección
   - Recomendaciones

RESPONDE EN FORMATO JSON ESTRICTO:
{{
  "damages": [
    {{
      "type": "string",
      "severity": "Leve|Media|Alta",
      "location": "string",
      "confidence": 0.0-1.0
    }}
  ],
  "seal": {{
    "intact": true|false,
    "tampered": true|false,
    "notes": "string"
  }},
  "container": {{
    "numberDetected": "string",
    "matches": true|false
  }},
  "fraud": {{
    "score": 0.0-1.0,
    "indicators": ["string"],
    "recommendation": "string"
  }},
  "summary": "string",
  "recommendations": ["string"]
}}
"""
        
        # Llamar a Bedrock Nova Pro
        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"text": prompt}
                    ] + [
                        {
                            "image": {
                                "format": "jpeg",
                                "source": {"bytes": base64.b64decode(img)}
                            }
                        } for img in images_base64
                    ]
                }
            ],
            "inferenceConfig": {
                "maxTokens": 4000,
                "temperature": 0.3,
                "topP": 0.9
            }
        }
        
        response = bedrock.invoke_model(
            modelId='us.amazon.nova-pro-v1:0',
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        
        # Extraer el texto de la respuesta
        result_text = response_body['output']['message']['content'][0]['text']
        
        # Intentar parsear como JSON
        try:
            # Buscar JSON en la respuesta
            start = result_text.find('{')
            end = result_text.rfind('}') + 1
            if start >= 0 and end > start:
                result_json = json.loads(result_text[start:end])
            else:
                result_json = json.loads(result_text)
        except:
            # Si falla, devolver texto plano
            result_json = {
                "raw_analysis": result_text,
                "damages": [],
                "fraud": {"score": 0.0}
            }
        
        # Agregar metadata
        result_json['metadata'] = {
            'timestamp': datetime.utcnow().isoformat(),
            'photos_analyzed': len(images_base64),
            'model': 'us.amazon.nova-pro-v1:0'
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result_json)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Error analyzing inspection'
            })
        }
