"""
Combine public dataset with Talos photos
"""

import os
import shutil
import glob
import argparse
from pathlib import Path

def combine_datasets(public_dataset_path, talos_photos_path, output_path='combined-dataset'):
    print("🔄 Combinando datasets...")
    print(f"   Dataset público: {public_dataset_path}")
    print(f"   Fotos Talos: {talos_photos_path}")
    print(f"   Output: {output_path}")
    
    # Crear estructura de output
    os.makedirs(output_path, exist_ok=True)
    
    splits = ['train', 'valid', 'test']
    for split in splits:
        os.makedirs(os.path.join(output_path, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_path, split, 'labels'), exist_ok=True)
    
    # 1. Copiar dataset público
    print("\n📁 Copiando dataset público...")
    total_public = 0
    
    for split in splits:
        split_path = os.path.join(public_dataset_path, split)
        if not os.path.exists(split_path):
            continue
        
        # Copiar imágenes
        images_src = os.path.join(split_path, 'images')
        images_dst = os.path.join(output_path, split, 'images')
        
        if os.path.exists(images_src):
            for img_file in glob.glob(os.path.join(images_src, '*.*')):
                shutil.copy2(img_file, images_dst)
                total_public += 1
        
        # Copiar labels
        labels_src = os.path.join(split_path, 'labels')
        labels_dst = os.path.join(output_path, split, 'labels')
        
        if os.path.exists(labels_src):
            for label_file in glob.glob(os.path.join(labels_src, '*.txt')):
                shutil.copy2(label_file, labels_dst)
    
    print(f"   ✅ {total_public} imágenes del dataset público")
    
    # 2. Agregar fotos de Talos (sin labels por ahora)
    print("\n📁 Agregando fotos de Talos...")
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
        
        dst = os.path.join(output_path, split, 'images', Path(photo).name)
        shutil.copy2(photo, dst)
        
        # Crear label vacío (sin anotaciones)
        label_file = os.path.join(output_path, split, 'labels', 
                                   Path(photo).stem + '.txt')
        with open(label_file, 'w') as f:
            f.write('')  # Vacío por ahora
    
    print(f"   ✅ {len(talos_photos)} fotos de Talos")
    print(f"   ⚠️  Nota: Fotos de Talos sin etiquetar (labels vacíos)")
    print(f"   💡 Recomendación: Etiquétalas en Roboflow primero")
    
    # 3. Copiar data.yaml
    data_yaml_src = os.path.join(public_dataset_path, 'data.yaml')
    data_yaml_dst = os.path.join(output_path, 'data.yaml')
    
    if os.path.exists(data_yaml_src):
        shutil.copy2(data_yaml_src, data_yaml_dst)
        print(f"\n✅ data.yaml copiado")
    else:
        print(f"\n⚠️  No se encontró data.yaml en dataset público")
    
    print(f"\n✅ Datasets combinados!")
    print(f"   Total imágenes: {total_public + len(talos_photos)}")
    print(f"   Output: {output_path}")
    print(f"\n📋 Próximo paso:")
    print(f"   python upload-labeled-dataset.py --dataset-path {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine public dataset with Talos photos')
    parser.add_argument('--public-dataset', type=str, required=True,
                        help='Path to public dataset (Roboflow export)')
    parser.add_argument('--talos-photos', type=str, required=True,
                        help='Path to Talos photos folder')
    parser.add_argument('--output', type=str, default='combined-dataset',
                        help='Output folder for combined dataset')
    
    args = parser.parse_args()
    combine_datasets(args.public_dataset, args.talos_photos, args.output)
