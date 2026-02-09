"""
Batch analyzer for multiple images
Analyzes all images in a folder and generates a summary report
"""

import os
import sys
from pathlib import Path
from forensic_analyzer import ForensicAnalyzer
import json

def analyze_folder(folder_path, ela_threshold=0.20):
    """Analyze all images in a folder"""
    
    analyzer = ForensicAnalyzer(ela_threshold=ela_threshold)
    results = []
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"❌ Folder not found: {folder_path}")
        return
    
    image_files = []
    for ext in image_extensions:
        image_files.extend(folder.glob(f'*{ext}'))
        image_files.extend(folder.glob(f'*{ext.upper()}'))
    
    if not image_files:
        print(f"❌ No images found in: {folder_path}")
        return
    
    print(f"\n{'='*70}")
    print(f"BATCH FORENSIC ANALYSIS")
    print(f"{'='*70}")
    print(f"Folder: {folder_path}")
    print(f"Images found: {len(image_files)}")
    print(f"ELA Threshold: {ela_threshold}")
    print(f"{'='*70}\n")
    
    # Analyze each image
    for i, image_path in enumerate(image_files, 1):
        print(f"[{i}/{len(image_files)}] Analyzing: {image_path.name}")
        
        try:
            result = analyzer.analyze_image(str(image_path))
            
            # Summary
            status = "✅ AUTHENTIC" if result.is_authentic else "❌ REJECTED"
            print(f"  Status: {status}")
            print(f"  ELA Score: {result.tampering.ela_score:.4f}")
            print(f"  Size: {result.file_size:,} bytes")
            print(f"  Dimensions: {result.image_dimensions[0]}x{result.image_dimensions[1]}")
            
            if result.gps.is_valid():
                print(f"  GPS: {result.gps.latitude:.6f}, {result.gps.longitude:.6f}")
            else:
                print(f"  GPS: Not available")
            
            if result.camera.make:
                print(f"  Camera: {result.camera.make} {result.camera.model}")
            else:
                print(f"  Camera: Not available")
            
            if not result.is_authentic:
                print(f"  Reason: {result.rejection_reason}")
            
            print()
            
            # Store result
            results.append({
                'filename': image_path.name,
                'path': str(image_path),
                'authentic': result.is_authentic,
                'ela_score': result.tampering.ela_score,
                'has_gps': result.gps.is_valid(),
                'has_camera_info': bool(result.camera.make),
                'size': result.file_size,
                'dimensions': f"{result.image_dimensions[0]}x{result.image_dimensions[1]}",
                'rejection_reason': result.rejection_reason if not result.is_authentic else None
            })
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}\n")
            results.append({
                'filename': image_path.name,
                'path': str(image_path),
                'error': str(e)
            })
    
    # Summary statistics
    print(f"{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    
    total = len(results)
    authentic = sum(1 for r in results if r.get('authentic', False))
    rejected = sum(1 for r in results if 'authentic' in r and not r['authentic'])
    errors = sum(1 for r in results if 'error' in r)
    
    with_gps = sum(1 for r in results if r.get('has_gps', False))
    with_camera = sum(1 for r in results if r.get('has_camera_info', False))
    
    print(f"Total images: {total}")
    print(f"✅ Authentic: {authentic} ({authentic/total*100:.1f}%)")
    print(f"❌ Rejected: {rejected} ({rejected/total*100:.1f}%)")
    if errors > 0:
        print(f"⚠️  Errors: {errors}")
    print(f"\n📍 With GPS: {with_gps} ({with_gps/total*100:.1f}%)")
    print(f"📷 With Camera Info: {with_camera} ({with_camera/total*100:.1f}%)")
    
    if rejected > 0:
        print(f"\nRejection reasons:")
        reasons = {}
        for r in results:
            if not r.get('authentic', True) and 'rejection_reason' in r:
                reason = r['rejection_reason']
                reasons[reason] = reasons.get(reason, 0) + 1
        
        for reason, count in reasons.items():
            print(f"  - {reason}: {count}")
    
    print(f"{'='*70}\n")
    
    # Save detailed report
    report_path = 'batch_analysis_report.json'
    with open(report_path, 'w') as f:
        json.dump({
            'folder': str(folder_path),
            'ela_threshold': ela_threshold,
            'total_images': total,
            'authentic': authentic,
            'rejected': rejected,
            'errors': errors,
            'with_gps': with_gps,
            'with_camera_info': with_camera,
            'results': results
        }, f, indent=2)
    
    print(f"📄 Detailed report saved to: {report_path}")
    
    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python batch_analyze.py <folder_path> [ela_threshold]")
        print("Example: python batch_analyze.py ../talos-inspection-photos")
        print("Example: python batch_analyze.py ../talos-inspection-photos 0.25")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    ela_threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.20
    
    analyze_folder(folder_path, ela_threshold)
