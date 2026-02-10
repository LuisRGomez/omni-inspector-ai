"""
Combinar múltiples datasets YOLO + fotos de Talos
"""

import os
import shutil
import glob
import argparse
from pathlib import Path

def combine_multiple_datasets(dataset_paths, talos_photos_path, output_path='combined-dataset'):
    print("🔄 Combinando múltiples datasets...")
    print(f"   Datasets: {dataset_paths}")
    print(f"   Fotos Talos: {talos_photos_path}")
    print(f"   Output: {output_path}")
    
    # Crear estructura de output
    os.makedirs(output_path, exist_ok=True)
    
    splits = ['train', 'valid', 'test']
    for split in splits:
        os.makedirs(os.path.join(output_path, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_path, split, 'labels'), exist_ok=True)
    
    total_images = 0
    
    # 1. Copiar datasets públicos
    for dataset_path in dataset_paths.split(','):
        dataset_path = dataset_path.strip()
        print(f"\n📁 Procesando: {dataset_path}")
        
        for split in splits:
            split_path = os.path.join(dataset_path, split)
            if not os.path.exists(split_path):
                continue
            
            # Copiar imágenes
            images_src = os.path.join(split_path, 'images')
            images_dst = os.path.join(output_path, split, 'images')
            
            if os.path.exists(images_src):
                for img_file in glob.glob(os.path.join(images_src, '*.*')):
                    filename = Path(img_file).name
                    # Agregar prefijo para evitar colisiones
                    dst_name = f"{Path(dataset_path).name}_{filename}"
                    shutil.copy2(img_file, os.path.join(images_dst, dst_name))
                    total_images += 1
                    
                    if total_images % 1000 == 0:
                        print(f"   Copiadas: {total_images} imágenes...")
            
            # Copiar labels
            labels_src = os.path.join(split_path, 'labels')
            labels_dst = os.path.join(output_path, split, 'labels')
            
            if os.path.exists(labels_src):
                for label_file in glob.glob(os.path.join(labels_src, '*.txt')):
                    filename = Path(label_file).name
                    dst_name = f"{Path(dataset_path).name}_{filename}"
                    shutil.copy2(label_file, os.path.join(labels_dst, dst_name))
    
    print(f"\n   ✅ {total_images} imágenes de datasets públicos")
    
    # 2. Agregar fotos de Talos (sin labels por ahora)
    if talos_photos_path and os.path.exists(talos_photos_path):
        print(f"\n📁 Agregando fotos de Talos...")
        talos_photos = glob.glob(os.path.join(talos_photos_path, '*.jpg'))
        
        # Distribuir: 70% train, 20% valid, 10% test
        train_count = int(len(talos_photos) * 0.7)
        valid_count = int(len(talos_photos) * 0.2)
        
        for i, photo in enumerate(talos_photos):
            if i < train_count:
                split = 'train'
            elif i < train_count + valid_count:
                split = 'valid'
            else:
                split = 'test'
            
            dst = os.path.join(output_path, split, 'images', f"talos_{Path(photo).name}")
            shutil.copy2(photo, dst)
            
            # Crear label vacío (sin anotaciones)
            label_file = os.path.join(output_path, split, 'labels', 
                                       f"talos_{Path(photo).stem}.txt")
            with open(label_file, 'w') as f:
                f.write('')  # Vacío por ahora
        
        print(f"   ✅ {len(talos_photos)} fotos de Talos")
        print(f"   ⚠️  Nota: Fotos de Talos sin etiquetar (labels vacíos)")
        print(f"   💡 Recomendación: Etiquétalas en Roboflow y re-combina")
    
    # 3. Copiar o crear data.yaml
    yaml_content = f"""# Dataset combinado
path: /opt/ml/input/data/training
train: train/images
val: valid/images
test: test/images

names:
  0: fresh
  1: overripe
  2: spoiled
  3: mold
  4: bruise
  5: dirt
"""
    
    with open(os.path.join(output_path, 'data.yaml'), 'w') as f:
        f.write(yaml_content)
    
    # Estadísticas finales
    train_imgs = len(os.listdir(os.path.join(output_path, 'train', 'images')))
    valid_imgs = len(os.listdir(os.path.join(output_path, 'valid', 'images')))
    test_imgs = len(os.listdir(os.path.join(output_path, 'test', 'images')))
    
    print(f"\n✅ Datasets combinados!")
    print(f"   Train: {train_imgs} imágenes")
    print(f"   Valid: {valid_imgs} imágenes")
    print(f"   Test: {test_imgs} imágenes")
    print(f"   Total: {train_imgs + valid_imgs + test_imgs} imágenes")
    print(f"   Output: {output_path}")
    print(f"\n📋 Próximo paso:")
    print(f"   python upload-labeled-dataset.py --dataset-path {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine multiple YOLO datasets + Talos photos')
    parser.add_argument('--datasets', type=str, required=True,
                        help='Comma-separated list of dataset paths (e.g., "mendeley-yolo,github-yolo")')
    parser.add_argument('--talos-photos', type=str, required=True,
                        help='Path to Talos photos folder')
    parser.add_argument('--output', type=str, default='combined-dataset',
                        help='Output folder for combined dataset')
    
    args = parser.parse_args()
    combine_multiple_datasets(args.datasets, args.talos_photos, args.output)
