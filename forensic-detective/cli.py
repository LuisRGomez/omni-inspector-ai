"""
Command Line Interface for Forensic Detective
"""

import argparse
import json
import sys
from pathlib import Path

from forensic_analyzer import ForensicAnalyzer
from aws_uploader import EvidenceUploader


def analyze_command(args):
    """Analyze an image"""
    analyzer = ForensicAnalyzer(ela_threshold=args.ela_threshold)
    result = analyzer.analyze_image(args.image)
    
    # Print result
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print_human_readable(result)
    
    # Save report if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"\n📄 Report saved to: {args.output}")
    
    # Exit with appropriate code
    sys.exit(0 if result.is_authentic else 1)


def upload_command(args):
    """Analyze and upload to S3"""
    # First analyze
    analyzer = ForensicAnalyzer(ela_threshold=args.ela_threshold)
    result = analyzer.analyze_image(args.image)
    
    if not result.is_authentic:
        print(f"❌ Image rejected: {result.rejection_reason}")
        sys.exit(1)
    
    # Upload to S3
    uploader = EvidenceUploader(
        bucket_name=args.bucket,
        profile_name=args.profile,
        region=args.region
    )
    
    try:
        upload_result = uploader.upload_evidence(
            image_path=args.image,
            forensic_result=result,
            case_id=args.case_id,
            inspector_id=args.inspector_id
        )
        
        print("✅ Evidence uploaded successfully:")
        print(f"   Case ID: {upload_result['case_id']}")
        print(f"   Image URL: {upload_result['image_url']}")
        print(f"   Report URL: {upload_result['report_url']}")
        print(f"   File Hash: {upload_result['file_hash']}")
        
        sys.exit(0)
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        sys.exit(1)


def print_human_readable(result):
    """Print result in human-readable format"""
    print("\n" + "="*60)
    print("FORENSIC ANALYSIS REPORT")
    print("="*60)
    
    # Status
    if result.is_authentic:
        print("\n✅ STATUS: AUTHENTIC")
    else:
        print(f"\n❌ STATUS: REJECTED")
        print(f"   Reason: {result.rejection_reason}")
    
    # File info
    print(f"\n📁 FILE INFORMATION:")
    print(f"   Hash: {result.file_hash}")
    print(f"   Size: {result.file_size:,} bytes")
    print(f"   Dimensions: {result.image_dimensions[0]}x{result.image_dimensions[1]}")
    
    # GPS
    if result.gps.is_valid():
        print(f"\n📍 GPS COORDINATES:")
        print(f"   Latitude: {result.gps.latitude:.6f}")
        print(f"   Longitude: {result.gps.longitude:.6f}")
        if result.gps.altitude:
            print(f"   Altitude: {result.gps.altitude:.1f}m")
    
    # Camera
    if result.camera.make or result.camera.model:
        print(f"\n📷 CAMERA INFORMATION:")
        if result.camera.make:
            print(f"   Make: {result.camera.make}")
        if result.camera.model:
            print(f"   Model: {result.camera.model}")
        if result.camera.lens:
            print(f"   Lens: {result.camera.lens}")
        if result.camera.iso:
            print(f"   ISO: {result.camera.iso}")
        if result.camera.aperture:
            print(f"   Aperture: f/{result.camera.aperture:.1f}")
        if result.camera.shutter_speed:
            print(f"   Shutter: {result.camera.shutter_speed}s")
    
    # Timestamp
    if result.timestamp.original:
        print(f"\n🕐 TIMESTAMP:")
        print(f"   Original: {result.timestamp.original}")
        if result.timestamp.modified:
            print(f"   Modified: {result.timestamp.modified}")
    
    # Tampering
    print(f"\n🔍 TAMPERING ANALYSIS:")
    print(f"   ELA Score: {result.tampering.ela_score:.4f}")
    print(f"   Tampered: {'Yes' if result.tampering.is_tampered else 'No'}")
    print(f"   Confidence: {result.tampering.confidence:.2%}")
    if result.tampering.suspicious_regions:
        print(f"   Suspicious Regions: {len(result.tampering.suspicious_regions)}")
    
    print("\n" + "="*60 + "\n")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Forensic Detective - Image Authenticity Analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze an image
  python cli.py analyze photo.jpg
  
  # Analyze with custom ELA threshold
  python cli.py analyze photo.jpg --ela-threshold 0.20
  
  # Save report to file
  python cli.py analyze photo.jpg --output report.json
  
  # Analyze and upload to S3
  python cli.py upload photo.jpg --case-id CASE-001 --inspector-id INS-123
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze an image')
    analyze_parser.add_argument('image', help='Path to image file')
    analyze_parser.add_argument(
        '--ela-threshold',
        type=float,
        default=0.15,
        help='ELA tampering threshold (0.0-1.0, default: 0.15)'
    )
    analyze_parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )
    analyze_parser.add_argument(
        '--output',
        '-o',
        help='Save report to file'
    )
    analyze_parser.set_defaults(func=analyze_command)
    
    # Upload command
    upload_parser = subparsers.add_parser('upload', help='Analyze and upload to S3')
    upload_parser.add_argument('image', help='Path to image file')
    upload_parser.add_argument('--case-id', required=True, help='Case identifier')
    upload_parser.add_argument('--inspector-id', required=True, help='Inspector identifier')
    upload_parser.add_argument(
        '--bucket',
        default='omni-inspector-evidence-dev',
        help='S3 bucket name'
    )
    upload_parser.add_argument(
        '--profile',
        default='omni-inspector',
        help='AWS profile name'
    )
    upload_parser.add_argument(
        '--region',
        default='us-east-1',
        help='AWS region'
    )
    upload_parser.add_argument(
        '--ela-threshold',
        type=float,
        default=0.15,
        help='ELA tampering threshold'
    )
    upload_parser.set_defaults(func=upload_command)
    
    # Parse and execute
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
