"""
Upload Talos photos to S3 for training
"""

import boto3
import glob
from pathlib import Path

def upload_dataset():
    s3 = boto3.client('s3')
    bucket = 'omni-inspector-models-472661249377'
    
    print("📤 Subiendo fotos de Talos a S3...")
    
    # Subir fotos
    photos = glob.glob('../talos-inspection-photos/*.jpg')
    
    for img_path in photos:
        filename = Path(img_path).name
        key = f'datasets/talos-v1/raw-images/{filename}'
        
        try:
            s3.upload_file(img_path, bucket, key)
            print(f"✅ {filename}")
        except Exception as e:
            print(f"❌ {filename}: {e}")
    
    print(f"\n✅ {len(photos)} fotos subidas a S3")
    print(f"   Bucket: s3://{bucket}/datasets/talos-v1/raw-images/")
    print("\n📋 Próximo paso:")
    print("   1. Ve a https://roboflow.com")
    print("   2. Crea proyecto 'Omni-Inspector'")
    print("   3. Descarga fotos de S3 o usa las locales")
    print("   4. Etiqueta daños (dent, dirt, rust, scratch, spoiled, mold)")
    print("   5. Genera augmentation (100+ imágenes)")
    print("   6. Exporta en formato YOLOv11")
    print("   7. Ejecuta: python upload-labeled-dataset.py")

if __name__ == '__main__':
    upload_dataset()
