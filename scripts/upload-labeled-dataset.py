"""
Upload labeled dataset from Roboflow to S3
"""

import boto3
import os
import glob
import argparse
from pathlib import Path

def upload_labeled_dataset(dataset_path):
    s3 = boto3.client('s3')
    bucket = 'omni-inspector-models-472661249377'
    
    print("📤 Subiendo dataset etiquetado a S3...")
    print(f"   Origen: {dataset_path}")
    
    # Verificar estructura
    if not os.path.exists(dataset_path):
        print(f"❌ Error: No existe {dataset_path}")
        return
    
    # Buscar carpetas train/valid/test
    splits = ['train', 'valid', 'test']
    total_uploaded = 0
    
    for split in splits:
        split_path = os.path.join(dataset_path, split)
        if not os.path.exists(split_path):
            print(f"⚠️  No existe carpeta {split}, saltando...")
            continue
        
        print(f"\n📁 Subiendo {split}...")
        
        # Subir imágenes
        images_path = os.path.join(split_path, 'images')
        if os.path.exists(images_path):
            for img_file in glob.glob(os.path.join(images_path, '*.*')):
                filename = Path(img_file).name
                key = f'datasets/talos-v1/{split}/images/{filename}'
                try:
                    s3.upload_file(img_file, bucket, key)
                    print(f"   ✅ {filename}")
                    total_uploaded += 1
                except Exception as e:
                    print(f"   ❌ {filename}: {e}")
        
        # Subir labels
        labels_path = os.path.join(split_path, 'labels')
        if os.path.exists(labels_path):
            for label_file in glob.glob(os.path.join(labels_path, '*.txt')):
                filename = Path(label_file).name
                key = f'datasets/talos-v1/{split}/labels/{filename}'
                try:
                    s3.upload_file(label_file, bucket, key)
                except Exception as e:
                    print(f"   ❌ {filename}: {e}")
    
    # Subir data.yaml
    data_yaml = os.path.join(dataset_path, 'data.yaml')
    if os.path.exists(data_yaml):
        print(f"\n📄 Subiendo data.yaml...")
        try:
            s3.upload_file(data_yaml, bucket, 'datasets/talos-v1/data.yaml')
            print(f"   ✅ data.yaml")
        except Exception as e:
            print(f"   ❌ data.yaml: {e}")
    else:
        print(f"\n⚠️  No se encontró data.yaml, creando uno...")
        # Crear data.yaml básico
        yaml_content = f"""# Omni-Inspector Dataset
path: /opt/ml/input/data/training
train: train/images
val: valid/images
test: test/images

names:
  0: dent
  1: dirt
  2: rust
  3: scratch
  4: hole
  5: crack
  6: spoiled
  7: mold
"""
        # Guardar localmente
        with open('data.yaml', 'w') as f:
            f.write(yaml_content)
        
        # Subir a S3
        s3.upload_file('data.yaml', bucket, 'datasets/talos-v1/data.yaml')
        print(f"   ✅ data.yaml creado y subido")
        os.remove('data.yaml')
    
    print(f"\n✅ Dataset subido exitosamente!")
    print(f"   Total archivos: {total_uploaded}")
    print(f"   Bucket: s3://{bucket}/datasets/talos-v1/")
    print(f"\n📋 Próximo paso:")
    print(f"   python launch-sagemaker-training.py")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload labeled dataset to S3')
    parser.add_argument('--dataset-path', type=str, required=True, 
                        help='Path to Roboflow export folder')
    
    args = parser.parse_args()
    upload_labeled_dataset(args.dataset_path)
