"""
CLI for YOLO Detection Service
"""

import argparse
import sys
import json
from pathlib import Path
from yolo_detector import YOLODetector


def print_result(result):
    """Print detection result in human-readable format"""
    print("=" * 70)
    print("YOLO DETECTION REPORT")
    print("=" * 70)
    print()
    print(f"📁 Image: {result.image_url}")
    print(f"📐 Dimensions: {result.image_dimensions[0]}x{result.image_dimensions[1]}")
    print(f"⏱️  Inference Time: {result.inference_time_ms:.0f}ms")
    print()
    
    if result.total_detections == 0:
        print("✅ No damage detected")
    else:
        print(f"🔍 DETECTIONS: {result.total_detections}")
        print(f"⚠️  Critical Issues: {result.critical_issues}")
        print(f"📊 Overall Severity: {result.overall_severity.upper()}")
        print()
        
        # Group by severity
        by_severity = {}
        for det in result.detections:
            if det.severity not in by_severity:
                by_severity[det.severity] = []
            by_severity[det.severity].append(det)
        
        # Print by severity (critical first)
        for severity in ['critical', 'high', 'medium', 'low', 'info']:
            if severity in by_severity:
                print(f"\n{severity.upper()}:")
                for det in by_severity[severity]:
                    print(f"  • {det.class_name}: {det.confidence:.2%}")
                    print(f"    Location: {det.bbox}")
    
    print()
    print("=" * 70)


def cmd_detect(args):
    """Detect damage in single image"""
    detector = YOLODetector(
        endpoint_name=args.endpoint,
        confidence_threshold=args.confidence
    )
    
    # Detect from S3 or local file
    if args.image.startswith('s3://'):
        result = detector.detect_from_s3(args.image)
    else:
        result = detector.detect_from_file(args.image)
    
    # Print result
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print_result(result)
    
    # Save to file if requested
    if args.output:
        detector.save_result(result, args.output)
        print(f"\n📄 Report saved to: {args.output}")


def cmd_batch(args):
    """Batch detection on multiple images"""
    detector = YOLODetector(
        endpoint_name=args.endpoint,
        confidence_threshold=args.confidence
    )
    
    # Get list of images
    if args.folder.startswith('s3://'):
        # TODO: List S3 objects
        print("S3 batch detection not yet implemented")
        return
    else:
        # Local folder
        folder = Path(args.folder)
        images = list(folder.glob('*.jpg')) + list(folder.glob('*.jpeg')) + list(folder.glob('*.png'))
    
    if not images:
        print(f"No images found in {args.folder}")
        return
    
    print(f"Processing {len(images)} images...")
    print()
    
    results = []
    for i, image_path in enumerate(images, 1):
        print(f"[{i}/{len(images)}] {image_path.name}...", end=' ')
        
        try:
            result = detector.detect_from_file(str(image_path))
            results.append(result)
            
            if result.total_detections > 0:
                print(f"✅ {result.total_detections} detections ({result.overall_severity})")
            else:
                print("✅ Clean")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Summary
    print()
    print("=" * 70)
    print("BATCH SUMMARY")
    print("=" * 70)
    print(f"Total images: {len(results)}")
    print(f"With detections: {sum(1 for r in results if r.total_detections > 0)}")
    print(f"Critical issues: {sum(r.critical_issues for r in results)}")
    print()
    
    # Save batch report
    if args.output:
        batch_report = {
            'total_images': len(results),
            'results': [r.to_dict() for r in results]
        }
        with open(args.output, 'w') as f:
            json.dump(batch_report, f, indent=2)
        print(f"📄 Batch report saved to: {args.output}")


def cmd_test(args):
    """Test SageMaker endpoint connectivity"""
    print("Testing YOLO detector...")
    print()
    
    try:
        detector = YOLODetector(endpoint_name=args.endpoint)
        print(f"✅ Detector initialized")
        print(f"   Endpoint: {args.endpoint}")
        print(f"   Confidence threshold: {detector.confidence_threshold}")
        print()
        print("Note: Actual endpoint test requires an image")
        print("Use: python cli.py detect <image_path>")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='YOLO Detection CLI - Detect damage in container/cargo images'
    )
    
    # Global options
    parser.add_argument(
        '--endpoint',
        default='omni-inspector-yolo',
        help='SageMaker endpoint name'
    )
    parser.add_argument(
        '--confidence',
        type=float,
        default=0.25,
        help='Confidence threshold (0.0-1.0)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Detect command
    detect_parser = subparsers.add_parser('detect', help='Detect damage in single image')
    detect_parser.add_argument('image', help='Image path or S3 URL')
    detect_parser.add_argument('--json', action='store_true', help='Output as JSON')
    detect_parser.add_argument('--output', help='Save report to file')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch detection on folder')
    batch_parser.add_argument('folder', help='Folder path or S3 prefix')
    batch_parser.add_argument('--output', help='Save batch report to file')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test endpoint connectivity')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == 'detect':
        cmd_detect(args)
    elif args.command == 'batch':
        cmd_batch(args)
    elif args.command == 'test':
        cmd_test(args)


if __name__ == '__main__':
    main()
