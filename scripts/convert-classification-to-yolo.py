"""
Convertir datasets de clasificación (carpetas) a formato YOLO (detección)
"""

import os
import shutil
import argparse
from pathlib import Path
from PIL import Image

def convert_classification_to_yolo(input_path, output_path, class_mapping=None):
    """
    Convierte dataset de clasificación a formato YOLO
    
    Args:
        input_path: Ruta al dataset (carpetas por clase)
        output_path: Ruta de salida (formato YOLO)
        class_mapping: Mapeo de clases originales a nuevas clases
    """
    
    print(f"🔄 Convirtiendo dataset a formato YOLO...")
    print(f"   Input: {input_path}")
    print(f"   Output: {output_path}")
    
    # Mapeo por defecto
    if class_mapping is None:
        class_mapping = {
            # Fresh & Rotten Fruits (Mendeley)
            'fresh_apple': 'fresh',
            'rotten_apple': 'spoiled',
            'fresh_banana': 'fresh',
            'rotten_banana': 'spoiled',
            'fresh_orange': 'fresh',
            'rotten_orange': 'spoiled',
            'fresh_grape': 'fresh',
            'rotten_grape': 'spoiled',
            'fresh_guava': 'fresh',
            'rotten_guava': 'spoiled',
            'fresh_jujube': 'fresh',
            'rotten_jujube': 'spoiled',
            'fresh_pomegranate': 'fresh',
            'rotten_pomegranate': 'spoiled',
            'fresh_strawberry': 'fresh',
            'rotten_strawberry': 'spoiled',
            
            # Fruit Freshness (GitHub)
            'fresh_apple': 'fresh',
            'normal_apple': 'overripe',
            'rotten_apple': 'spoiled',
            'fresh_banana': 'fresh',
            'normal_banana': 'overripe',
            'rotten_banana': 'spoiled',
            'fresh_orange': 'fresh',
            'normal_orange': 'overripe',
            'rotten_orange': 'spoiled',
        }
    
    # Clases finales
    final_classes = {
        'fresh': 0,
        'overripe': 1,
        'spoiled': 2,
        'mold': 3,
        'bruise': 4,
        'dirt': 5
    }
    
    # Crear estructura YOLO
    splits = ['train', 'valid', 'test']
    for split in splits:
        os.makedirs(f'{output_path}/{split}/images', exist_ok=True)
        os.makedirs(f'{output_path}/{split}/labels', exist_ok=True)
    
    # Procesar carpetas
    total_images = 0
    
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            
            # Obtener clase de la carpeta
            folder_name = Path(root).name.lower()
            
            # Mapear a clase final
            mapped_class = class_mapping.get(folder_name, folder_name)
            
            # Obtener class_id
            class_id = final_classes.get(mapped_class, 0)
            
            # Determinar split (70% train, 20% valid, 10% test)
            if total_images % 10 < 7:
                split = 'train'
            elif total_images % 10 < 9:
                split = 'valid'
            else:
                split = 'test'
            
            # Copiar imagen
            src_img = os.path.join(root, file)
            dst_img = f'{output_path}/{split}/images/{Path(file).stem}_{total_images}{Path(file).suffix}'
            
            try:
                shutil.copy2(src_img, dst_img)
                
                # Crear label (imagen completa = 1 objeto)
                label_file = f'{output_path}/{split}/labels/{Path(file).stem}_{total_images}.txt'
                
                with open(label_file, 'w') as f:
                    # Cajita completa: centro (0.5, 0.5), tamaño (1.0, 1.0)
                    f.write(f'{class_id} 0.5 0.5 1.0 1.0\n')
                
                total_images += 1
                
                if total_images % 100 == 0:
                    print(f"   Procesadas: {total_images} imágenes...")
                
            except Exception as e:
                print(f"   ⚠️  Error con {file}: {e}")
    
    # Crear data.yaml
    yaml_content = f"""# Dataset convertido a YOLO
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
    
    with open(f'{output_path}/data.yaml', 'w') as f:
        f.write(yaml_content)
    
    print(f"\n✅ Conversión completa!")
    print(f"   Total imágenes: {total_images}")
    print(f"   Train: {len(os.listdir(f'{output_path}/train/images'))}")
    print(f"   Valid: {len(os.listdir(f'{output_path}/valid/images'))}")
    print(f"   Test: {len(os.listdir(f'{output_path}/test/images'))}")
    print(f"   Output: {output_path}")
    print(f"\n📋 Próximo paso:")
    print(f"   python upload-labeled-dataset.py --dataset-path {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert classification dataset to YOLO format')
    parser.add_argument('--input', type=str, required=True,
                        help='Path to classification dataset (folders by class)')
    parser.add_argument('--output', type=str, default='yolo-dataset',
                        help='Output path for YOLO dataset')
    
    args = parser.parse_args()
    convert_classification_to_yolo(args.input, args.output)
