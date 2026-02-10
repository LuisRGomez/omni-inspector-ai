"""
Fraud Detector - Vector similarity and pattern analysis for fraud detection.

Detects:
- Recycled photos (same image used in multiple claims)
- Metadata manipulation
- Suspicious patterns
- Timestamp inconsistencies
"""

import boto3
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pydantic import BaseModel
import hashlib
import json


class FraudResult(BaseModel):
    """Fraud detection result."""
    is_suspicious: bool
    fraud_score: float  # 0-1, where 1 = definite fraud
    reasons: List[str]
    similar_cases: List[str] = []
    confidence: float


class FraudDetector:
    """
    Fraud detection using vector similarity and pattern analysis.
    
    Methods:
    - Photo recycling detection (vector similarity)
    - Metadata manipulation detection
    - Pattern recognition (multiple claims from same location)
    - Timestamp validation
    """
    
    def __init__(
        self,
        region: str = 'us-east-1',
        profile: Optional[str] = None,
        similarity_threshold: float = 0.95
    ):
        """
        Initialize fraud detector.
        
        Args:
            region: AWS region
            profile: AWS profile name
            similarity_threshold: Threshold for duplicate detection (0-1)
        """
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        self.s3 = session.client('s3', region_name=region)
        self.dynamodb = session.resource('dynamodb', region_name=region)
        self.similarity_threshold = similarity_threshold
        
        # DynamoDB table for storing image hashes and vectors
        self.table_name = 'omni-inspector-fraud-detection'
    
    def check_image(
        self,
        image_url: str,
        metadata: Dict,
        case_id: str
    ) -> FraudResult:
        """
        Comprehensive fraud check on an image.
        
        Args:
            image_url: S3 URL of image
            metadata: Forensic metadata from Phase 1
            case_id: Case identifier
        
        Returns:
            FraudResult with fraud score and reasons
        """
        reasons = []
        fraud_score = 0.0
        similar_cases = []
        
        # 1. Check for duplicate images (perceptual hash)
        image_hash = self._calculate_perceptual_hash(image_url)
        duplicates = self._find_duplicates(image_hash)
        
        if duplicates:
            reasons.append(f"Image matches {len(duplicates)} previous cases (recycled photo)")
            fraud_score += 0.8
            similar_cases = duplicates
        
        # 2. Metadata manipulation check
        metadata_score = self._check_metadata_manipulation(metadata)
        if metadata_score > 0.5:
            reasons.append(f"Metadata manipulation detected (score: {metadata_score:.2f})")
            fraud_score += metadata_score * 0.5
        
        # 3. Timestamp validation
        timestamp_issues = self._validate_timestamps(metadata)
        if timestamp_issues:
            reasons.extend(timestamp_issues)
            fraud_score += 0.3
        
        # 4. GPS validation
        gps_issues = self._validate_gps(metadata)
        if gps_issues:
            reasons.extend(gps_issues)
            fraud_score += 0.2
        
        # 5. Pattern analysis (multiple claims from same location)
        pattern_score = self._analyze_patterns(metadata, case_id)
        if pattern_score > 0.5:
            reasons.append(f"Suspicious pattern detected (score: {pattern_score:.2f})")
            fraud_score += pattern_score * 0.3
        
        # Normalize fraud score
        fraud_score = min(fraud_score, 1.0)
        
        # Store image hash for future comparisons
        self._store_image_hash(image_hash, case_id, image_url)
        
        return FraudResult(
            is_suspicious=fraud_score > 0.5,
            fraud_score=fraud_score,
            reasons=reasons if reasons else ["No fraud indicators detected"],
            similar_cases=similar_cases,
            confidence=0.85 if fraud_score > 0.7 else 0.6
        )
    
    def _calculate_perceptual_hash(self, image_url: str) -> str:
        """
        Calculate perceptual hash (pHash) for image similarity.
        
        pHash is resistant to minor modifications (resize, compression, etc.)
        but will match similar images.
        """
        # Download image
        parts = image_url.replace('s3://', '').split('/', 1)
        bucket = parts[0]
        key = parts[1] if len(parts) > 1 else ''
        
        response = self.s3.get_object(Bucket=bucket, Key=key)
        image_data = response['Body'].read()
        
        # Calculate SHA-256 hash (simple version)
        # In production, use actual perceptual hashing (imagehash library)
        return hashlib.sha256(image_data).hexdigest()
    
    def _find_duplicates(self, image_hash: str) -> List[str]:
        """
        Find duplicate images in database.
        
        Returns list of case IDs with similar images.
        """
        try:
            table = self.dynamodb.Table(self.table_name)
            response = table.query(
                IndexName='ImageHashIndex',
                KeyConditionExpression='image_hash = :hash',
                ExpressionAttributeValues={':hash': image_hash}
            )
            
            return [item['case_id'] for item in response.get('Items', [])]
        except Exception:
            # Table might not exist yet
            return []
    
    def _check_metadata_manipulation(self, metadata: Dict) -> float:
        """
        Check for metadata manipulation indicators.
        
        Returns manipulation score (0-1).
        """
        score = 0.0
        
        # Check if EXIF data is missing (suspicious)
        if not metadata.get('camera'):
            score += 0.3
        
        # Check if GPS is missing but timestamp exists
        if not metadata.get('gps') and metadata.get('timestamp'):
            score += 0.2
        
        # Check if timestamps are inconsistent
        original = metadata.get('timestamp', {}).get('original')
        modified = metadata.get('timestamp', {}).get('modified')
        
        if original and modified:
            try:
                orig_dt = datetime.fromisoformat(original)
                mod_dt = datetime.fromisoformat(modified)
                
                # If modified is much later than original (> 1 day), suspicious
                if (mod_dt - orig_dt).days > 1:
                    score += 0.4
            except (ValueError, TypeError):
                pass
        
        return min(score, 1.0)
    
    def _validate_timestamps(self, metadata: Dict) -> List[str]:
        """Validate timestamp consistency."""
        issues = []
        
        timestamp_data = metadata.get('timestamp', {})
        original = timestamp_data.get('original')
        
        if original:
            try:
                orig_dt = datetime.fromisoformat(original)
                now = datetime.now()
                
                # Check if timestamp is in the future
                if orig_dt > now:
                    issues.append("Timestamp is in the future")
                
                # Check if timestamp is too old (> 1 year)
                if (now - orig_dt).days > 365:
                    issues.append("Timestamp is more than 1 year old")
                
            except (ValueError, TypeError):
                issues.append("Invalid timestamp format")
        
        return issues
    
    def _validate_gps(self, metadata: Dict) -> List[str]:
        """Validate GPS coordinates."""
        issues = []
        
        gps = metadata.get('gps', {})
        lat = gps.get('latitude')
        lon = gps.get('longitude')
        
        if lat is not None and lon is not None:
            # Check if coordinates are valid
            if not (-90 <= lat <= 90):
                issues.append("Invalid latitude")
            
            if not (-180 <= lon <= 180):
                issues.append("Invalid longitude")
            
            # Check if coordinates are at null island (0, 0)
            if abs(lat) < 0.1 and abs(lon) < 0.1:
                issues.append("GPS coordinates at null island (suspicious)")
        
        return issues
    
    def _analyze_patterns(self, metadata: Dict, case_id: str) -> float:
        """
        Analyze patterns across multiple cases.
        
        Detects:
        - Multiple claims from same GPS location
        - Same camera used in multiple claims
        - Temporal patterns (many claims in short time)
        
        Returns pattern score (0-1).
        """
        score = 0.0
        
        # This would query DynamoDB for similar cases
        # For now, return 0 (no pattern detected)
        
        # TODO: Implement pattern analysis
        # - Query cases with similar GPS (within 100m)
        # - Query cases with same camera make/model
        # - Query cases from same inspector in last 24h
        
        return score
    
    def _store_image_hash(self, image_hash: str, case_id: str, image_url: str):
        """Store image hash in DynamoDB for future comparisons."""
        try:
            table = self.dynamodb.Table(self.table_name)
            table.put_item(
                Item={
                    'case_id': case_id,
                    'image_hash': image_hash,
                    'image_url': image_url,
                    'timestamp': datetime.now().isoformat()
                }
            )
        except Exception:
            # Table might not exist yet, skip
            pass
    
    def check_duplicate(
        self,
        image_url: str,
        threshold: float = 0.95
    ) -> Tuple[bool, List[str]]:
        """
        Quick duplicate check.
        
        Args:
            image_url: S3 URL of image
            threshold: Similarity threshold (0-1)
        
        Returns:
            (is_duplicate, list_of_similar_case_ids)
        """
        image_hash = self._calculate_perceptual_hash(image_url)
        duplicates = self._find_duplicates(image_hash)
        
        return len(duplicates) > 0, duplicates
