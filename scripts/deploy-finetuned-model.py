"""
Deploy fine-tuned YOLO model to SageMaker Endpoint
"""

import boto3
import time
import json

def deploy_finetuned_model():
    print("🚀 Desplegando modelo fine-tuned...")
    
    sagemaker = boto3.client('sagemaker')
    bucket = 'omni-inspector-models-472661249377'
    
    # 1. Obtener último training job
    print("\n1️⃣  Buscando último training job...")
    
    try:
        with open('training_job_name.txt', 'r') as f:
            job_name = f.read().strip()
    except FileNotFoundError:
        # Buscar último job
        response = sagemaker.list_training_jobs(
            SortBy='CreationTime',
            SortOrder='Descending',
            MaxResults=1
        )
        if not response['TrainingJobSummaries']:
            print("❌ No se encontraron training jobs")
            return
        job_name = response['TrainingJobSummaries'][0]['TrainingJobName']
    
    print(f"   Job: {job_name}")
    
    # 2. Verificar que el training terminó
    print("\n2️⃣  Verificando estado del training...")
    
    job_info = sagemaker.describe_training_job(TrainingJobName=job_name)
    status = job_info['TrainingJobStatus']
    
    if status == 'InProgress':
        print(f"   ⏳ Training aún en progreso...")
        print(f"   💡 Espera a que termine antes de desplegar")
        print(f"   📊 Monitorear en: https://console.aws.amazon.com/sagemaker/home?region=us-east-1#/jobs/{job_name}")
        return
    elif status == 'Failed':
        print(f"   ❌ Training falló")
        print(f"   Razón: {job_info.get('FailureReason', 'Unknown')}")
        return
    elif status == 'Completed':
        print(f"   ✅ Training completado")
    
    # 3. Obtener modelo entrenado
    model_data_url = job_info['ModelArtifacts']['S3ModelArtifacts']
    print(f"\n3️⃣  Modelo entrenado:")
    print(f"   {model_data_url}")
    
    # 4. Crear modelo en SageMaker
    print("\n4️⃣  Creando modelo en SageMaker...")
    
    model_name = f'omni-inspector-yolo-finetuned-{int(time.time())}'
    
    # Imagen de inferencia PyTorch
    inference_image = '763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:2.0.0-cpu-py310'
    
    try:
        sagemaker.create_model(
            ModelName=model_name,
            PrimaryContainer={
                'Image': inference_image,
                'ModelDataUrl': model_data_url,
                'Environment': {
                    'SAGEMAKER_PROGRAM': 'inference.py',
                    'SAGEMAKER_SUBMIT_DIRECTORY': model_data_url
                }
            },
            ExecutionRoleArn='arn:aws:iam::472661249377:role/OmniInspectorSageMakerRole'
        )
        print(f"   ✅ Modelo creado: {model_name}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 5. Crear endpoint config (serverless)
    print("\n5️⃣  Creando endpoint config...")
    
    config_name = f'{model_name}-config'
    
    try:
        sagemaker.create_endpoint_config(
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
        print(f"   ✅ Config creado: {config_name}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 6. Actualizar o crear endpoint
    print("\n6️⃣  Desplegando endpoint...")
    
    endpoint_name = 'omni-inspector-yolo'
    
    try:
        # Verificar si endpoint existe
        sagemaker.describe_endpoint(EndpointName=endpoint_name)
        
        # Endpoint existe, actualizar
        print(f"   🔄 Actualizando endpoint existente...")
        sagemaker.update_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=config_name
        )
        print(f"   ✅ Endpoint actualizando...")
        
    except sagemaker.exceptions.ClientError:
        # Endpoint no existe, crear nuevo
        print(f"   🆕 Creando nuevo endpoint...")
        sagemaker.create_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=config_name
        )
        print(f"   ✅ Endpoint creando...")
    
    # 7. Esperar a que esté en servicio
    print("\n7️⃣  Esperando a que endpoint esté en servicio...")
    print(f"   ⏳ Esto puede tomar 5-10 minutos...")
    
    waiter = sagemaker.get_waiter('endpoint_in_service')
    try:
        waiter.wait(
            EndpointName=endpoint_name,
            WaiterConfig={
                'Delay': 30,
                'MaxAttempts': 20
            }
        )
        print(f"   ✅ Endpoint en servicio!")
    except Exception as e:
        print(f"   ⚠️  Timeout esperando endpoint")
        print(f"   💡 El endpoint seguirá desplegándose en background")
    
    print("\n" + "="*70)
    print("✅ DESPLIEGUE COMPLETO")
    print("="*70)
    print(f"\n📊 Detalles:")
    print(f"   Endpoint: {endpoint_name}")
    print(f"   Modelo: {model_name}")
    print(f"   Tipo: Serverless (2GB RAM, 5 concurrent)")
    print(f"\n🧪 Probar modelo:")
    print(f"   cd yolo-detection")
    print(f"   python cli.py detect ..\\talos-inspection-photos\\20260207_091519.jpg --use-finetuned")
    print(f"\n📊 Monitorear en:")
    print(f"   https://console.aws.amazon.com/sagemaker/home?region=us-east-1#/endpoints/{endpoint_name}")
    
    # Guardar config
    config = {
        'endpoint_name': endpoint_name,
        'model_name': model_name,
        'training_job': job_name,
        'deployed_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('finetuned-model-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n💾 Config guardado en: finetuned-model-config.json")

if __name__ == '__main__':
    deploy_finetuned_model()
