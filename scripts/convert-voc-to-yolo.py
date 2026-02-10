"""
Convertir dataset Pascal VOC (XML) a formato YOLO
"""

import os
import xml.etree.ElementTree as ET
import shutil
from pathlib import Path
import argparse

def convert_voc_to_yolo(voc_path, output_path):
    """
    Convierte dataset Pascal VOC a formato YOLO
    
    Args:
        voc_path: Ruta al dataset VOC (con carpetas Annotations y JPEGImages)
        output_path: Ruta de salida (formato YOLO)
    """
    
    print(f"🔄 Convirtiendo dataset VOC a YOLO...")
    print(f"   Input: {voc_path}")
    print(f"   Output: {output_path}")
    
    # Mapeo de clases VOC a clases finales
    class_mapping = {
        'fresh_apple': 'fresh',
        'fresh_banana': 'fresh',
        'fresh_orange': 'fresh',
        'fresh_grape': 'fresh',
        'normal_apple': 'overripe',
        'normal_banana': 'overripe',
        'normal_orange': 'overripe',
        'rotten_apple': 'spoiled',
        'rotten_banana': 'spoiled',
        'rotten_orange': 'spoiled',
        'rotten_grape': 'spoiled',
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
    
    # Obtener todas las anotaciones
    annotations_path = os.path.join(voc_path, 'Annotations')
    images_path = os.path.join(voc_path, 'JPEGImages')
    
    xml_files = sorted([f for f in os.listdir(annotations_path) if f.endswith('.xml')])
    
    print(f"   Encontradas {len(xml_files)} anotaciones")
    
    total_images = 0
    class_counts = {}
    
    for idx, xml_file in enumerate(xml_files):
        try:
            # Parsear XML
            tree = ET.parse(os.path.join(annotations_path, xml_file))
            root = tree.getroot()
            
            # Obtener dimensiones de imagen
            size = root.find('size')
            img_width = int(size.find('width').text)
            img_height = int(size.find('height').text)
            
            # Obtener nombre de imagen
            filename = root.find('filename').text
            
            # Determinar split (70% train, 20% valid, 10% test)
            if idx % 10 < 7:
                split = 'train'
            elif idx % 10 < 9:
                split = 'valid'
            else:
                split = 'test'
            
            # Copiar imagen
            src_img = os.path.join(images_path, filename)
            if not os.path.exists(src_img):
                print(f"   ⚠️  Imagen no encontrada: {filename}")
                continue
            
            dst_img = f'{output_path}/{split}/images/{filename}'
            shutil.copy2(src_img, dst_img)
            
            # Crear archivo de labels
            label_file = f'{output_path}/{split}/labels/{Path(filename).stem}.txt'
            
            with open(label_file, 'w') as f:
                # Procesar cada objeto
                for obj in root.findall('object'):
                    class_name = obj.find('name').text.lower()
                    
                    # Mapear a clase final
                    mapped_class = class_mapping.get(class_name, class_name)
                    class_id = final_classes.get(mapped_class, 0)
                    
                    # Contar clases
                    if mapped_class not in class_counts:
                        class_counts[mapped_class] = 0
                    class_counts[mapped_class] += 1
                    
                    # Obtener bounding box
                    bbox = obj.find('bndbox')
                    xmin = float(bbox.find('xmin').text)
                    ymin = float(bbox.find('ymin').text)
                    xmax = float(bbox.find('xmax').text)
                    ymax = float(bbox.find('ymax').text)
                    
                    # Convertir a formato YOLO (normalizado)
                    x_center = ((xmin + xmax) / 2) / img_width
                    y_center = ((ymin + ymax) / 2) / img_height
                    width = (xmax - xmin) / img_width
                    height = (ymax - ymin) / img_height
                    
                    # Escribir en formato YOLO
                    f.write(f'{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n')
            
            total_images += 1
            
            if total_images % 500 == 0:
                print(f"   Procesadas: {total_images} imágenes...")
        
        except Exception as e:
            print(f"   ⚠️  Error con {xml_file}: {e}")
    
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
    
    print(f"\n📊 Distribución de clases:")
    for class_name, count in sorted(class_counts.items()):
        print(f"   {class_name}: {count}")
    
    print(f"\n📋 Próximo paso:")
    print(f"   python scripts/upload-labeled-dataset.py --dataset-path {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Pascal VOC dataset to YOLO format')
    parser.add_argument('--input', type=str, required=True,
                        help='Path to VOC dataset (with Annotations and JPEGImages folders)')
    parser.add_argument('--output', type=str, default='yolo-dataset',
                        help='Output path for YOLO dataset')
    
    args = parser.parse_args()
    convert_voc_to_yolo(args.input, args.output)
