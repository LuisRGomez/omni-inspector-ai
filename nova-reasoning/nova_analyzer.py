"""
Nova Analyzer - Amazon Bedrock integration for multimodal AI analysis.

This module provides the core reasoning layer using Amazon Nova models
for damage assessment, fraud detection, and report generation.
"""

import json
import boto3
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
import base64
from io import BytesIO


class DamageAssessment(BaseModel):
    """Damage assessment result from Nova analysis."""
    damage_type: str
    severity: str  # low, medium, high, critical
    location: str
    confidence: float
    repair_cost_estimate: Optional[float] = None
    description: str


class AnalysisResult(BaseModel):
    """Complete analysis result from Nova."""
    case_id: str
    timestamp: str
    module: str  # underwriting, claims, legal
    verdict: str  # APPROVED, REJECTED, REVIEW_REQUIRED
    confidence: float
    damages: List[DamageAssessment]
    fraud_score: float = Field(ge=0.0, le=1.0)
    risk_score: float = Field(ge=0.0, le=10.0)
    reasoning: str
    recommendations: List[str]
    estimated_total_cost: Optional[float] = None
    processing_time_ms: int


class NovaAnalyzer:
    """
    Amazon Bedrock Nova analyzer for multimodal inspection analysis.
    
    Supports:
    - Amazon Nova Lite (fast, cost-effective)
    - Amazon Nova Pro (advanced reasoning)
    """
    
    def __init__(
        self,
        model: str = 'amazon.nova-lite-v1:0',
        region: str = 'us-east-1',
        profile: Optional[str] = None
    ):
        """
        Initialize Nova analyzer.
        
        Args:
            model: Bedrock model ID (nova-lite or nova-pro)
            region: AWS region
            profile: AWS profile name (optional)
        """
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        self.bedrock = session.client('bedrock-runtime', region_name=region)
        self.s3 = session.client('s3', region_name=region)
        self.model = model
        
        # Model configuration
        self.config = {
            'amazon.nova-lite-v1:0': {
                'max_tokens': 2048,
                'temperature': 0.3,
                'top_p': 0.9
            },
            'amazon.nova-pro-v1:0': {
                'max_tokens': 4096,
                'temperature': 0.2,
                'top_p': 0.95
            }
        }
    
    def analyze_case(
        self,
        case_id: str,
        forensic_data: Dict[str, Any],
        yolo_data: Dict[str, Any],
        image_url: str,
        module: str = 'claims'
    ) -> AnalysisResult:
        """
        Perform complete case analysis using Nova.
        
        Args:
            case_id: Unique case identifier
            forensic_data: Output from Phase 1 (forensic analysis)
            yolo_data: Output from Phase 2 (YOLO detections)
            image_url: S3 URL of the image
            module: Business module (underwriting, claims, legal)
        
        Returns:
            AnalysisResult with verdict and recommendations
        """
        start_time = datetime.now()
        
        # Download image from S3
        image_data = self._download_from_s3(image_url)
        
        # Build prompt based on module
        prompt = self._build_prompt(module, forensic_data, yolo_data)
        
        # Call Bedrock with multimodal input
        response = self._invoke_bedrock(prompt, image_data)
        
        # Parse response
        result = self._parse_response(
            case_id=case_id,
            module=module,
            response=response,
            forensic_data=forensic_data,
            yolo_data=yolo_data
        )
        
        # Calculate processing time
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        result.processing_time_ms = processing_time
        
        return result
    
    def _download_from_s3(self, s3_url: str) -> bytes:
        """Download image from S3."""
        # Parse S3 URL: s3://bucket/key
        parts = s3_url.replace('s3://', '').split('/', 1)
        bucket = parts[0]
        key = parts[1] if len(parts) > 1 else ''
        
        response = self.s3.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()
    
    def _build_prompt(
        self,
        module: str,
        forensic_data: Dict[str, Any],
        yolo_data: Dict[str, Any]
    ) -> str:
        """Build analysis prompt based on business module."""
        
        base_context = f"""
You are an expert forensic inspector analyzing container/cargo damage for insurance and legal purposes.

FORENSIC DATA:
- Image authentic: {forensic_data.get('is_authentic', False)}
- GPS: {forensic_data.get('gps', 'N/A')}
- Timestamp: {forensic_data.get('timestamp', 'N/A')}
- Camera: {forensic_data.get('camera', 'N/A')}
- Tampering score: {forensic_data.get('ela_score', 0.0)}

YOLO DETECTIONS:
- Total detections: {yolo_data.get('summary', {}).get('total_detections', 0)}
- Critical issues: {yolo_data.get('summary', {}).get('critical_issues', 0)}
- Overall severity: {yolo_data.get('summary', {}).get('overall_severity', 'unknown')}

DETECTED DAMAGES:
"""
        
        # Add YOLO detections
        for detection in yolo_data.get('detections', []):
            base_context += f"- {detection['class']}: {detection['confidence']:.2%} confidence, severity: {detection['severity']}\n"
        
        # Module-specific instructions
        module_prompts = {
            'underwriting': """
TASK: Pre-inspection for insurance underwriting
GOAL: Determine if the container/cargo has pre-existing damage that should prevent insurance issuance.

Analyze the image and data to:
1. Identify all pre-existing damage
2. Assess risk level (0-10 scale)
3. Recommend APPROVE or REJECT
4. Estimate repair costs if applicable
5. Provide reasoning for decision

Output JSON format:
{
  "verdict": "APPROVED|REJECTED|REVIEW_REQUIRED",
  "risk_score": 0-10,
  "damages": [...],
  "reasoning": "...",
  "recommendations": [...]
}
""",
            'claims': """
TASK: Claims validation and fraud detection
GOAL: Determine if the claim is legitimate and estimate settlement amount.

Analyze the image and data to:
1. Validate damage matches claim description
2. Detect fraud indicators (recycled photos, inconsistent metadata)
3. Estimate repair/replacement costs
4. Recommend APPROVE, REJECT, or REVIEW_REQUIRED
5. Calculate fraud score (0-1, where 1 = definite fraud)

Output JSON format:
{
  "verdict": "APPROVED|REJECTED|REVIEW_REQUIRED",
  "fraud_score": 0-1,
  "estimated_cost": 0,
  "damages": [...],
  "reasoning": "...",
  "recommendations": [...]
}
""",
            'legal': """
TASK: Legal evidence preparation
GOAL: Generate court-ready evidence package for lawsuit against third parties.

Analyze the image and data to:
1. Document all damages with precise descriptions
2. Extract container ID, seal numbers, CSC plates (OCR)
3. Determine causality (who is liable)
4. Assess if evidence is court-admissible
5. Provide detailed technical report

Output JSON format:
{
  "verdict": "COURT_READY|INSUFFICIENT_EVIDENCE",
  "container_id": "...",
  "seal_number": "...",
  "damages": [...],
  "causality": "...",
  "liability": "internal|external|shared",
  "reasoning": "...",
  "recommendations": [...]
}
"""
        }
        
        return base_context + module_prompts.get(module, module_prompts['claims'])
    
    def _invoke_bedrock(self, prompt: str, image_data: bytes) -> Dict[str, Any]:
        """Call Amazon Bedrock with multimodal input."""
        
        # Encode image to base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Build request body (Nova format)
        request_body = {
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {
                            'text': prompt
                        },
                        {
                            'image': {
                                'format': 'jpeg',
                                'source': {
                                    'bytes': image_base64
                                }
                            }
                        }
                    ]
                }
            ],
            'inferenceConfig': self.config.get(self.model, self.config['amazon.nova-lite-v1:0'])
        }
        
        # Invoke Bedrock
        response = self.bedrock.invoke_model(
            modelId=self.model,
            body=json.dumps(request_body)
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        return response_body
    
    def _parse_response(
        self,
        case_id: str,
        module: str,
        response: Dict[str, Any],
        forensic_data: Dict[str, Any],
        yolo_data: Dict[str, Any]
    ) -> AnalysisResult:
        """Parse Bedrock response into AnalysisResult."""
        
        # Extract text from Nova response
        content = response.get('output', {}).get('message', {}).get('content', [])
        text = ''
        for item in content:
            if 'text' in item:
                text += item['text']
        
        # Try to parse JSON from response
        try:
            # Find JSON in response (between { and })
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_text = text[json_start:json_end]
                parsed = json.loads(json_text)
            else:
                # Fallback: create basic response
                parsed = {
                    'verdict': 'REVIEW_REQUIRED',
                    'reasoning': text,
                    'damages': [],
                    'recommendations': []
                }
        except json.JSONDecodeError:
            # Fallback parsing
            parsed = {
                'verdict': 'REVIEW_REQUIRED',
                'reasoning': text,
                'damages': [],
                'recommendations': []
            }
        
        # Build damage assessments
        damages = []
        for damage_data in parsed.get('damages', []):
            if isinstance(damage_data, dict):
                damages.append(DamageAssessment(
                    damage_type=damage_data.get('type', 'unknown'),
                    severity=damage_data.get('severity', 'medium'),
                    location=damage_data.get('location', 'unknown'),
                    confidence=damage_data.get('confidence', 0.5),
                    repair_cost_estimate=damage_data.get('repair_cost', None),
                    description=damage_data.get('description', '')
                ))
        
        # Create result
        result = AnalysisResult(
            case_id=case_id,
            timestamp=datetime.now().isoformat(),
            module=module,
            verdict=parsed.get('verdict', 'REVIEW_REQUIRED'),
            confidence=parsed.get('confidence', 0.5),
            damages=damages,
            fraud_score=parsed.get('fraud_score', 0.0),
            risk_score=parsed.get('risk_score', 5.0),
            reasoning=parsed.get('reasoning', text),
            recommendations=parsed.get('recommendations', []),
            estimated_total_cost=parsed.get('estimated_cost', None),
            processing_time_ms=0  # Will be set by caller
        )
        
        return result
    
    def extract_ocr(self, image_url: str, extract_types: List[str]) -> Dict[str, str]:
        """
        Extract text using Nova OCR capabilities.
        
        Args:
            image_url: S3 URL of image
            extract_types: List of types to extract (container-id, seal-number, csc-plate, license-plate)
        
        Returns:
            Dictionary with extracted values
        """
        image_data = self._download_from_s3(image_url)
        
        prompt = f"""
Extract the following information from this image:
{', '.join(extract_types)}

For container IDs, follow ISO 6346 format (4 letters + 7 digits).
For seal numbers, extract alphanumeric codes.
For CSC plates, extract certification details.
For license plates, extract plate numbers.

Return JSON format:
{{
  "container_id": "...",
  "seal_number": "...",
  "csc_plate": "...",
  "license_plate": "..."
}}
"""
        
        response = self._invoke_bedrock(prompt, image_data)
        
        # Parse OCR results
        content = response.get('output', {}).get('message', {}).get('content', [])
        text = ''.join([item.get('text', '') for item in content if 'text' in item])
        
        try:
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                return json.loads(text[json_start:json_end])
        except json.JSONDecodeError:
            pass
        
        return {}
