"""
YOLO Detection Service
Detects damage in container/cargo images using YOLOv11 on SageMaker
"""

import json
import boto3
from typing import List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import numpy as np
from PIL import Image
import io


# Damage classes and severity mapping
DAMAGE_CLASSES = {
    'dent': 'medium',
    'rust': 'low',
    'hole': 'high',
    'crack': 'high',
    'broken_seal': 'high',
    'missing_part': 'medium',
    'container_id': 'info',
    'cargo_damage': 'high',
    'water_damage': 'medium',
    'fire_damage': 'critical'
}

SEVERITY_SCORES = {
    'info': 0,
    'low': 1,
    'medium': 2,
    'high': 3,
    'critical': 4
}


@dataclass
class Detection:
    """Single object detection result"""
    class_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    severity: str
    
    def to_dict(self):
        return {
            'class': self.class_name,
            'confidence': float(self.confidence),
            'bbox': list(self.bbox),
            'severity': self.severity
        }


@dataclass
class DetectionResult:
    """Complete detection result for an image"""
    image_url: str
    timestamp: datetime
    detections: List[Detection]
    image_dimensions: Tuple[int, int]
    inference_time_ms: float
    
    @property
    def total_detections(self) -> int:
        return len(self.detections)
    
    @property
    def critical_issues(self) -> int:
        return sum(1 for d in self.detections if d.severity in ['high', 'critical'])
    
    @property
    def overall_severity(self) -> str:
        """Calculate overall severity based on detections"""
        if not self.detections:
            return 'none'
        
        max_score = max(SEVERITY_SCORES[d.severity] for d in self.detections)
        
        for severity, score in SEVERITY_SCORES.items():
            if score == max_score:
                return severity
        
        return 'none'
    
    def to_dict(self):
        return {
            'image_url': self.image_url,
            'timestamp': self.timestamp.isoformat(),
            'detections': [d.to_dict() for d in self.detections],
            'image_dimensions': list(self.image_dimensions),
            'inference_time_ms': self.inference_time_ms,
            'summary': {
                'total_detections': self.total_detections,
                'critical_issues': self.critical_issues,
                'overall_severity': self.overall_severity
            }
        }


class YOLODetector:
    """
    YOLO-based damage detector using AWS SageMaker
    """
    
    def __init__(
        self,
        endpoint_name: str = 'omni-inspector-yolo',
        confidence_threshold: float = 0.25,
        aws_profile: str = 'omni-inspector'
    ):
        """
        Initialize YOLO detector
        
        Args:
            endpoint_name: SageMaker endpoint name
            confidence_threshold: Minimum confidence for detections (0.0-1.0)
            aws_profile: AWS profile name
        """
        self.endpoint_name = endpoint_name
        self.confidence_threshold = confidence_threshold
        
        # Initialize AWS clients
        session = boto3.Session(profile_name=aws_profile)
        self.sagemaker_runtime = session.client('sagemaker-runtime')
        self.s3_client = session.client('s3')
    
    def detect_from_s3(self, s3_url: str) -> DetectionResult:
        """
        Detect damage in image from S3
        
        Args:
            s3_url: S3 URL (s3://bucket/key)
        
        Returns:
            DetectionResult with all detections
        """
        # Download image from S3
        image_data, dimensions = self._download_from_s3(s3_url)
        
        # Run detection
        start_time = datetime.now()
        detections = self._detect(image_data)
        inference_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return DetectionResult(
            image_url=s3_url,
            timestamp=datetime.now(),
            detections=detections,
            image_dimensions=dimensions,
            inference_time_ms=inference_time
        )
    
    def detect_from_file(self, file_path: str) -> DetectionResult:
        """
        Detect damage in local image file
        
        Args:
            file_path: Path to image file
        
        Returns:
            DetectionResult with all detections
        """
        # Load image
        image = Image.open(file_path)
        dimensions = image.size
        
        # Convert to bytes
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        image_data = buffer.getvalue()
        
        # Run detection
        start_time = datetime.now()
        detections = self._detect(image_data)
        inference_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return DetectionResult(
            image_url=f"file://{file_path}",
            timestamp=datetime.now(),
            detections=detections,
            image_dimensions=dimensions,
            inference_time_ms=inference_time
        )
    
    def _detect(self, image_data: bytes) -> List[Detection]:
        """
        Run YOLO detection on image data
        
        Args:
            image_data: Image bytes (JPEG)
        
        Returns:
            List of Detection objects
        """
        try:
            # Call SageMaker endpoint
            response = self.sagemaker_runtime.invoke_endpoint(
                EndpointName=self.endpoint_name,
                ContentType='application/x-image',
                Body=image_data
            )
            
            # Parse response
            result = json.loads(response['Body'].read().decode())
            
            # Convert to Detection objects
            detections = []
            for det in result.get('predictions', []):
                class_name = det['class']
                confidence = det['confidence']
                
                # Filter by confidence threshold
                if confidence < self.confidence_threshold:
                    continue
                
                # Get severity
                severity = DAMAGE_CLASSES.get(class_name, 'medium')
                
                # Create Detection object
                detection = Detection(
                    class_name=class_name,
                    confidence=confidence,
                    bbox=tuple(det['bbox']),
                    severity=severity
                )
                detections.append(detection)
            
            return detections
            
        except Exception as e:
            # If SageMaker endpoint not available, use local YOLO (fallback)
            print(f"SageMaker endpoint error: {e}")
            print("Falling back to local YOLO detection...")
            return self._detect_local(image_data)
    
    def _detect_local(self, image_data: bytes) -> List[Detection]:
        """
        Fallback: Run YOLO detection locally using ultralytics
        
        Args:
            image_data: Image bytes
        
        Returns:
            List of Detection objects
        """
        try:
            from ultralytics import YOLO
            
            # Load YOLOv11 model (will download if not cached)
            model = YOLO('yolov11n.pt')  # Nano model for speed
            
            # Load image
            image = Image.open(io.BytesIO(image_data))
            
            # Run inference
            results = model(image, conf=self.confidence_threshold)
            
            # Parse results
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get class name
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    
                    # Map to our damage classes (simplified for now)
                    # In production, we'd use a fine-tuned model
                    if class_name in DAMAGE_CLASSES:
                        severity = DAMAGE_CLASSES[class_name]
                    else:
                        # Skip non-damage classes
                        continue
                    
                    # Get bbox and confidence
                    bbox = box.xyxy[0].cpu().numpy().astype(int)
                    confidence = float(box.conf[0])
                    
                    detection = Detection(
                        class_name=class_name,
                        confidence=confidence,
                        bbox=tuple(bbox),
                        severity=severity
                    )
                    detections.append(detection)
            
            return detections
            
        except Exception as e:
            print(f"Local YOLO detection error: {e}")
            return []
    
    def _download_from_s3(self, s3_url: str) -> Tuple[bytes, Tuple[int, int]]:
        """
        Download image from S3
        
        Args:
            s3_url: S3 URL (s3://bucket/key)
        
        Returns:
            (image_data, dimensions)
        """
        # Parse S3 URL
        if not s3_url.startswith('s3://'):
            raise ValueError(f"Invalid S3 URL: {s3_url}")
        
        parts = s3_url[5:].split('/', 1)
        bucket = parts[0]
        key = parts[1] if len(parts) > 1 else ''
        
        # Download from S3
        response = self.s3_client.get_object(Bucket=bucket, Key=key)
        image_data = response['Body'].read()
        
        # Get dimensions
        image = Image.open(io.BytesIO(image_data))
        dimensions = image.size
        
        return image_data, dimensions
    
    def save_result(self, result: DetectionResult, output_path: str):
        """
        Save detection result to JSON file
        
        Args:
            result: DetectionResult object
            output_path: Path to save JSON file
        """
        with open(output_path, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
    
    def upload_result_to_s3(
        self,
        result: DetectionResult,
        bucket: str,
        key: str
    ) -> str:
        """
        Upload detection result to S3
        
        Args:
            result: DetectionResult object
            bucket: S3 bucket name
            key: S3 key (path)
        
        Returns:
            S3 URL of uploaded result
        """
        # Convert to JSON
        json_data = json.dumps(result.to_dict(), indent=2)
        
        # Upload to S3
        self.s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=json_data.encode('utf-8'),
            ContentType='application/json'
        )
        
        return f"s3://{bucket}/{key}"


if __name__ == '__main__':
    # Example usage
    detector = YOLODetector()
    
    # Test with local image
    result = detector.detect_from_file('test_image.jpg')
    
    print(f"Found {result.total_detections} detections")
    print(f"Critical issues: {result.critical_issues}")
    print(f"Overall severity: {result.overall_severity}")
    
    for detection in result.detections:
        print(f"  {detection.class_name}: {detection.confidence:.2f} ({detection.severity})")
