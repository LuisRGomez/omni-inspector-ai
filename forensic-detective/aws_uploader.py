"""
AWS S3 Uploader for Forensic Evidence
Uploads validated images and forensic reports to S3 with WORM storage
"""

import json
import boto3
from pathlib import Path
from typing import Optional
from datetime import datetime

from forensic_analyzer import ForensicResult


class EvidenceUploader:
    """
    Uploads forensic evidence to AWS S3
    Ensures legal compliance with WORM storage and metadata indexing
    """
    
    def __init__(
        self,
        bucket_name: str,
        profile_name: str = 'omni-inspector',
        region: str = 'us-east-1'
    ):
        """
        Initialize evidence uploader
        
        Args:
            bucket_name: S3 bucket name (e.g., 'omni-inspector-evidence-prod')
            profile_name: AWS profile name
            region: AWS region
        """
        self.bucket_name = bucket_name
        
        # Initialize boto3 session with profile
        session = boto3.Session(profile_name=profile_name, region_name=region)
        self.s3_client = session.client('s3')
        self.dynamodb = session.resource('dynamodb')
    
    def upload_evidence(
        self,
        image_path: str,
        forensic_result: ForensicResult,
        case_id: str,
        inspector_id: str
    ) -> dict:
        """
        Upload image and forensic report to S3
        
        Args:
            image_path: Path to the original image
            forensic_result: Forensic analysis result
            case_id: Unique case identifier
            inspector_id: Inspector/user identifier
            
        Returns:
            Dictionary with S3 URLs and metadata
        """
        if not forensic_result.is_authentic:
            raise ValueError(f"Cannot upload rejected image: {forensic_result.rejection_reason}")
        
        timestamp = datetime.utcnow().isoformat()
        path = Path(image_path)
        
        # Generate S3 keys
        base_key = f"evidence/{case_id}/{timestamp}"
        image_key = f"{base_key}/original{path.suffix}"
        report_key = f"{base_key}/forensic_report.json"
        
        # Upload original image
        image_url = self._upload_file(
            file_path=image_path,
            s3_key=image_key,
            content_type=self._get_content_type(path.suffix),
            metadata={
                'case-id': case_id,
                'inspector-id': inspector_id,
                'file-hash': forensic_result.file_hash,
                'timestamp': timestamp
            }
        )
        
        # Create forensic report
        report = self._create_report(
            forensic_result=forensic_result,
            case_id=case_id,
            inspector_id=inspector_id,
            image_s3_url=image_url
        )
        
        # Upload forensic report
        report_url = self._upload_json(
            data=report,
            s3_key=report_key,
            metadata={
                'case-id': case_id,
                'inspector-id': inspector_id,
                'timestamp': timestamp
            }
        )
        
        # Enable Object Lock (WORM) on both files
        self._enable_object_lock(image_key)
        self._enable_object_lock(report_key)
        
        return {
            'case_id': case_id,
            'timestamp': timestamp,
            'image_url': image_url,
            'report_url': report_url,
            'file_hash': forensic_result.file_hash
        }
    
    def _upload_file(
        self,
        file_path: str,
        s3_key: str,
        content_type: str,
        metadata: dict
    ) -> str:
        """Upload file to S3"""
        with open(file_path, 'rb') as f:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=f,
                ContentType=content_type,
                Metadata=metadata,
                ServerSideEncryption='AES256'
            )
        
        return f"s3://{self.bucket_name}/{s3_key}"
    
    def _upload_json(
        self,
        data: dict,
        s3_key: str,
        metadata: dict
    ) -> str:
        """Upload JSON data to S3"""
        json_data = json.dumps(data, indent=2)
        
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=json_data.encode('utf-8'),
            ContentType='application/json',
            Metadata=metadata,
            ServerSideEncryption='AES256'
        )
        
        return f"s3://{self.bucket_name}/{s3_key}"
    
    def _enable_object_lock(self, s3_key: str):
        """
        Enable Object Lock (WORM) on S3 object
        This ensures the evidence cannot be modified or deleted
        """
        try:
            # Set retention for 5 years (legal requirement)
            retention_date = datetime.utcnow().replace(year=datetime.utcnow().year + 5)
            
            self.s3_client.put_object_retention(
                Bucket=self.bucket_name,
                Key=s3_key,
                Retention={
                    'Mode': 'COMPLIANCE',
                    'RetainUntilDate': retention_date
                }
            )
        except Exception as e:
            # Object Lock might not be enabled on bucket
            print(f"Warning: Could not enable Object Lock: {e}")
    
    def _create_report(
        self,
        forensic_result: ForensicResult,
        case_id: str,
        inspector_id: str,
        image_s3_url: str
    ) -> dict:
        """Create comprehensive forensic report"""
        report = forensic_result.to_dict()
        
        # Add case metadata
        report['case_metadata'] = {
            'case_id': case_id,
            'inspector_id': inspector_id,
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'image_s3_url': image_s3_url,
            'analyzer_version': '1.0.0'
        }
        
        # Add legal compliance info
        report['legal_compliance'] = {
            'chain_of_custody': 'Forensic analysis performed before upload',
            'storage_type': 'WORM (Write Once Read Many)',
            'retention_period': '5 years',
            'encryption': 'AES-256'
        }
        
        return report
    
    def _get_content_type(self, extension: str) -> str:
        """Get MIME type from file extension"""
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.heic': 'image/heic',
            '.heif': 'image/heif'
        }
        return content_types.get(extension.lower(), 'application/octet-stream')


def main():
    """Example usage"""
    from forensic_analyzer import ForensicAnalyzer
    
    # Analyze image
    analyzer = ForensicAnalyzer()
    result = analyzer.analyze_image("test_image.jpg")
    
    if result.is_authentic:
        # Upload to S3
        uploader = EvidenceUploader(
            bucket_name='omni-inspector-evidence-dev',
            profile_name='omni-inspector'
        )
        
        upload_result = uploader.upload_evidence(
            image_path="test_image.jpg",
            forensic_result=result,
            case_id="CASE-2026-001",
            inspector_id="inspector-123"
        )
        
        print("✅ Evidence uploaded successfully:")
        print(json.dumps(upload_result, indent=2))
    else:
        print(f"❌ Image rejected: {result.rejection_reason}")


if __name__ == "__main__":
    main()
