"""
Launch SageMaker Training Job for YOLO fine-tuning
"""

import boto3
import sagemaker
from sagemaker.pytorch import PyTorch
from datetime import datetime

def launch_training():
    print("🚀 Lanzando SageMaker Training Job...")
    
    # Configuración
    role = 'arn:aws:iam::472661249377:role/OmniInspectorSageMakerRole'
    bucket = 'omni-inspector-models-472661249377'
    
    # Timestamp para versioning
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    # Crear estimator
    estimator = PyTorch(
        entry_point='sagemaker_train.py',
        source_dir='../yolo-detection',
        role=role,
        instance_type='ml.g4dn.xlarge',  # GPU instance
        instance_count=1,
        framework_version='2.0.0',
        py_version='py310',
        
        hyperparameters={
            'epochs': 100,
            'batch': 16,
            'imgsz': 640,
            'patience': 20
        },
        
        output_path=f's3://{bucket}/models/yolo-finetuned/{timestamp}/',
        
        # Usar Spot Instances (70% más barato)
        use_spot_instances=True,
        max_run=14400,  # 4 horas
        max_wait=18000,  # 5 horas
        
        # Checkpoints
        checkpoint_s3_uri=f's3://{bucket}/checkpoints/yolo-finetuned/{timestamp}/',
        checkpoint_local_path='/opt/ml/checkpoints',
        
        # Métricas
        metric_definitions=[
            {'Name': 'train:loss', 'Regex': 'train/loss: ([0-9\\.]+)'},
            {'Name': 'val:mAP50', 'Regex': 'metrics/mAP50\\(B\\): ([0-9\\.]+)'},
            {'Name': 'val:mAP50-95', 'Regex': 'metrics/mAP50-95\\(B\\): ([0-9\\.]+)'},
        ],
        
        # Tags
        tags=[
            {'Key': 'Project', 'Value': 'Omni-Inspector'},
            {'Key': 'Phase', 'Value': 'Fine-tuning'},
            {'Key': 'Version', 'Value': 'v1'}
        ]
    )
    
    # Iniciar entrenamiento
    print("\n📊 Configuración:")
    print(f"   Instance: ml.g4dn.xlarge (GPU)")
    print(f"   Spot: Sí (70% descuento)")
    print(f"   Epochs: 100")
    print(f"   Batch: 16")
    print(f"   Max time: 4 horas")
    print(f"   Output: s3://{bucket}/models/yolo-finetuned/{timestamp}/")
    
    print("\n⏳ Iniciando training job...")
    
    estimator.fit({
        'training': f's3://{bucket}/datasets/talos-v1/train/',
        'validation': f's3://{bucket}/datasets/talos-v1/val/'
    }, wait=False)
    
    job_name = estimator.latest_training_job.name
    
    print(f"\n✅ Training job iniciado!")
    print(f"   Job name: {job_name}")
    print(f"   Duración estimada: 2-4 horas")
    print(f"\n📊 Monitorear en:")
    print(f"   https://console.aws.amazon.com/sagemaker/home?region=us-east-1#/jobs/{job_name}")
    print(f"\n📝 Ver logs:")
    print(f"   aws logs tail /aws/sagemaker/TrainingJobs --follow --filter-pattern {job_name}")
    print(f"\n⏸️  Mientras esperas:")
    print(f"   - Trabajar en app móvil")
    print(f"   - Preparar backend")
    print(f"   - Tomar café ☕")
    
    # Guardar job name
    with open('training_job_name.txt', 'w') as f:
        f.write(job_name)
    
    return job_name

if __name__ == '__main__':
    launch_training()
