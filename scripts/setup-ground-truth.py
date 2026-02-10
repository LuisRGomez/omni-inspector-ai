"""
Setup Amazon SageMaker Ground Truth para etiquetado
"""

import boto3
import json
from datetime import datetime

def setup_ground_truth():
    sagemaker = boto3.client('sagemaker')
    s3 = boto3.client('s3')
    
    bucket = 'omni-inspector-models-472661249377'
    
    print("🏷️  Configurando Ground Truth...")
    
    # 1. Crear Private Workforce
    print("\n1️⃣  Creando Private Workforce...")
    
    workforce_name = 'omni-inspector-labelers'
    
    try:
        response = sagemaker.create_workteam(
            WorkteamName=workforce_name,
            MemberDefinitions=[
                {
                    'CognitoMemberDefinition': {
                        'UserPool': 'us-east-1_XXXXXXX',  # Crear Cognito User Pool
                        'UserGroup': 'labelers',
                        'ClientId': 'XXXXXXXXX'
                    }
                }
            ],
            Description='Equipo de etiquetado Omni-Inspector'
        )
        print(f"✅ Workforce creado: {workforce_name}")
    except sagemaker.exceptions.ResourceInUse:
        print(f"✅ Workforce ya existe: {workforce_name}")
    
    # 2. Crear manifest de imágenes
    print("\n2️⃣  Creando manifest de imágenes...")
    
    # Listar fotos en S3
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix='datasets/talos-v1/raw-images/'
    )
    
    manifest = []
    for obj in response.get('Contents', []):
        if obj['Key'].endswith('.jpg'):
            manifest.append({
                'source-ref': f"s3://{bucket}/{obj['Key']}"
            })
    
    # Guardar manifest
    manifest_key = 'datasets/talos-v1/manifest.jsonl'
    manifest_content = '\n'.join([json.dumps(item) for item in manifest])
    
    s3.put_object(
        Bucket=bucket,
        Key=manifest_key,
        Body=manifest_content
    )
    
    print(f"✅ Manifest creado: {len(manifest)} imágenes")
    
    # 3. Crear label categories
    print("\n3️⃣  Creando categorías de etiquetas...")
    
    categories = {
        'labels': [
            {'label': 'dent', 'description': 'Abolladura o golpe'},
            {'label': 'dirt', 'description': 'Suciedad (NO es daño)'},
            {'label': 'rust', 'description': 'Óxido o corrosión'},
            {'label': 'scratch', 'description': 'Rayadura'},
            {'label': 'spoiled', 'description': 'Podrido (alimentos)'},
            {'label': 'mold', 'description': 'Moho (alimentos)'}
        ]
    }
    
    categories_key = 'datasets/talos-v1/label-categories.json'
    s3.put_object(
        Bucket=bucket,
        Key=categories_key,
        Body=json.dumps(categories)
    )
    
    print(f"✅ Categorías creadas: {len(categories['labels'])}")
    
    # 4. Crear Labeling Job
    print("\n4️⃣  Creando Labeling Job...")
    
    job_name = f'omni-inspector-labeling-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
    
    try:
        response = sagemaker.create_labeling_job(
            LabelingJobName=job_name,
            LabelAttributeName='labels',
            
            InputConfig={
                'DataSource': {
                    'S3DataSource': {
                        'ManifestS3Uri': f's3://{bucket}/{manifest_key}'
                    }
                }
            },
            
            OutputConfig={
                'S3OutputPath': f's3://{bucket}/datasets/talos-v1/labeled/'
            },
            
            RoleArn='arn:aws:iam::472661249377:role/OmniInspectorSageMakerRole',
            
            LabelCategoryConfigS3Uri=f's3://{bucket}/{categories_key}',
            
            HumanTaskConfig={
                'WorkteamArn': f'arn:aws:sagemaker:us-east-1:472661249377:workteam/private-crowd/{workforce_name}',
                
                'UiConfig': {
                    'UiTemplateS3Uri': 's3://omni-inspector-models-472661249377/datasets/ui-template.html'
                },
                
                'PreHumanTaskLambdaArn': 'arn:aws:lambda:us-east-1:432418664414:function:PRE-BoundingBox',
                
                'TaskTitle': 'Etiquetar daños en vehículos/contenedores',
                'TaskDescription': 'Dibuja cajitas sobre daños visibles y clasifícalos',
                'NumberOfHumanWorkersPerDataObject': 1,
                'TaskTimeLimitInSeconds': 600,
                'TaskAvailabilityLifetimeInSeconds': 864000,
                'MaxConcurrentTaskCount': 10,
                
                'AnnotationConsolidationConfig': {
                    'AnnotationConsolidationLambdaArn': 'arn:aws:lambda:us-east-1:432418664414:function:ACS-BoundingBox'
                }
            }
        )
        
        print(f"✅ Labeling Job creado: {job_name}")
        print(f"\n📊 Monitorear en:")
        print(f"   https://console.aws.amazon.com/sagemaker/groundtruth?region=us-east-1#/labeling-jobs/{job_name}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n⚠️  Nota: Necesitas configurar Cognito User Pool primero")
        print("   Ver: setup-cognito-for-ground-truth.py")
    
    print("\n" + "="*70)
    print("PRÓXIMOS PASOS")
    print("="*70)
    print("\n1. Invitar etiquetadores:")
    print("   - Ve a SageMaker Console → Ground Truth → Private workforce")
    print("   - Click 'Invite workers'")
    print("   - Ingresa emails de tus inspectores")
    print("   - Ellos recibirán invitación por email")
    print("\n2. Etiquetadores acceden a:")
    print("   https://[tu-workforce-url].labeling.sagemaker.aws")
    print("\n3. Cuando terminen, ejecuta:")
    print("   python process-ground-truth-output.py")

if __name__ == '__main__':
    setup_ground_truth()
