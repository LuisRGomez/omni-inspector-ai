# Nova Reasoning Layer

> Amazon Bedrock integration for multimodal AI analysis, fraud detection, and report generation.

## Overview

Phase 3 of Omni-Inspector AI implements the reasoning layer using Amazon Nova models via Bedrock. This layer receives:
- **Forensic data** from Phase 1 (metadata, tampering analysis)
- **YOLO detections** from Phase 2 (damage locations, severity)
- **Original images** from S3

And produces:
- **Fraud analysis** (recycled photos, suspicious patterns)
- **Damage assessment** (severity, cost estimation)
- **Business reports** (underwriting, claims, legal)

## Features

### ✅ Multimodal Analysis
- Combines image, metadata, and detection data
- Contextual understanding of damage
- Causality analysis

### ✅ Fraud Detection
- Photo recycling detection (vector similarity)
- Metadata manipulation detection
- Suspicious pattern recognition
- Timestamp inconsistencies

### ✅ Report Generation
- **Module A (Underwriting)**: Pre-existing damage report
- **Module B (Claims)**: Claim validation and estimation
- **Module C (Legal)**: Evidence report for lawsuits

### ✅ OCR Capabilities
- Container ID extraction (ISO 6346)
- CSC plate reading
- Seal number recognition
- License plate detection

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Phase 1: Forensic Detective              │
│  • Metadata extraction                                      │
│  • Tampering detection                                      │
│  • S3 upload (WORM)                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                    Phase 2: YOLO Detection                  │
│  • Damage detection (10 classes)                            │
│  • Bounding boxes + confidence                              │
│  • Severity scoring                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                    Phase 3: Nova Reasoning ← YOU ARE HERE   │
│  • Multimodal analysis (Nova Pro)                           │
│  • Fraud detection (vector similarity)                      │
│  • Report generation                                        │
│  • OCR (container IDs, seals)                               │
└─────────────────────────────────────────────────────────────┘
```

## Installation

```bash
cd nova-reasoning
pip install -r requirements.txt
```

## Configuration

Set AWS credentials:
```bash
# Option 1: Environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1

# Option 2: AWS CLI profile
aws configure --profile omni-inspector
```

## Usage

### CLI Commands

#### Analyze Single Case
```bash
python cli.py analyze \
  --case-id CASE-2026-001 \
  --forensic-report s3://bucket/case-001/forensic_report.json \
  --yolo-report s3://bucket/case-001/detection_report.json \
  --image s3://bucket/case-001/original.jpg \
  --module underwriting
```

#### Fraud Detection
```bash
python cli.py fraud-check \
  --case-id CASE-2026-001 \
  --image s3://bucket/case-001/original.jpg \
  --check-duplicates
```

#### OCR Extraction
```bash
python cli.py ocr \
  --image s3://bucket/case-001/container.jpg \
  --extract container-id,seal-number
```

#### Generate Report
```bash
python cli.py report \
  --case-id CASE-2026-001 \
  --module claims \
  --output report.pdf
```

### Python API

```python
from nova_reasoning import NovaAnalyzer, FraudDetector, ReportGenerator

# Initialize
analyzer = NovaAnalyzer(model='amazon.nova-pro-v1:0')

# Analyze case
result = analyzer.analyze_case(
    case_id='CASE-2026-001',
    forensic_data=forensic_report,
    yolo_data=yolo_report,
    image_url='s3://bucket/image.jpg'
)

# Check for fraud
fraud_detector = FraudDetector()
fraud_result = fraud_detector.check_image(
    image_url='s3://bucket/image.jpg',
    metadata=forensic_report['metadata']
)

if fraud_result.is_suspicious:
    print(f"⚠️ Fraud detected: {fraud_result.reason}")

# Generate report
report_gen = ReportGenerator()
report = report_gen.generate(
    case_data=result,
    module='underwriting'  # or 'claims', 'legal'
)

# Save report
report.save_pdf('report.pdf')
report.save_json('report.json')
```

## Business Modules

### Module A: Underwriting (Alta de Riesgo)

**Purpose**: Detect pre-existing damage before issuing insurance

**Input**:
- Container/cargo photos
- Inspection metadata
- YOLO damage detections

**Output**:
```json
{
  "case_id": "CASE-2026-001",
  "module": "underwriting",
  "recommendation": "REJECT",
  "reason": "Pre-existing damage detected",
  "damages": [
    {
      "type": "dent",
      "severity": "medium",
      "location": "front_left_panel",
      "confidence": 0.95
    }
  ],
  "risk_score": 8.5,
  "certificate": "blockchain_hash_here"
}
```

### Module B: Claims (Siniestros)

**Purpose**: Validate claims and detect fraud

**Input**:
- Claim photos
- Policy data
- Historical inspections

**Output**:
```json
{
  "case_id": "CLAIM-2026-001",
  "module": "claims",
  "verdict": "APPROVED",
  "fraud_score": 0.12,
  "estimated_cost": 15000,
  "damages": [
    {
      "type": "hole",
      "severity": "high",
      "repair_cost": 12000
    }
  ],
  "processing_time": "2.3s"
}
```

### Module C: Legal Recovery (Recupero)

**Purpose**: Generate evidence for lawsuits

**Input**:
- Accident photos
- Container IDs
- Damage analysis

**Output**:
```json
{
  "case_id": "LEGAL-2026-001",
  "module": "legal",
  "evidence_package": {
    "container_id": "MSCU1234567",
    "seal_number": "SEAL-789456",
    "damages": [...],
    "causality": "Third-party collision",
    "liability": "external",
    "court_ready": true
  }
}
```

## Models

### Amazon Nova Lite
- **Use**: Fast analysis, OCR, simple reasoning
- **Cost**: $0.00006/1K input tokens
- **Speed**: ~500ms per request
- **Best for**: Real-time mobile app responses

### Amazon Nova Pro
- **Use**: Complex reasoning, fraud detection, report generation
- **Cost**: $0.0008/1K input tokens
- **Speed**: ~2s per request
- **Best for**: Backend batch processing

## Fraud Detection

### Vector Similarity Search
```python
# Check if image was used before
fraud_detector.check_duplicate(
    image_url='s3://bucket/new_claim.jpg',
    threshold=0.95  # 95% similarity = fraud
)
```

### Metadata Analysis
- GPS coordinate validation
- Timestamp consistency
- Camera fingerprinting
- EXIF manipulation detection

### Pattern Recognition
- Multiple claims from same location
- Suspicious damage patterns
- Recycled photos across cases

## Performance

- **Analysis Time**: 2-5 seconds per case
- **Fraud Check**: 1-2 seconds
- **OCR**: 500ms per image
- **Report Generation**: 3-5 seconds

## Cost Estimation

### Per Case Analysis
- **Nova Pro**: ~$0.002 (2,000 tokens)
- **S3 reads**: ~$0.0001
- **Total**: **~$0.002 per case**

### Monthly (1,000 cases)
- **Nova Pro**: ~$2.00
- **S3**: ~$0.10
- **Total**: **~$2.10/month**

## Security

- ✅ AWS IAM roles for Bedrock access
- ✅ S3 encryption (AES-256)
- ✅ HTTPS for all API calls
- ✅ No credentials in code
- ✅ Audit logging (CloudTrail)

## Testing

```bash
# Run tests
pytest test_nova_reasoning.py -v

# Test with real images
python cli.py test --image test_image.jpg
```

## Integration

### End-to-End Pipeline
```python
from forensic_detective import ForensicAnalyzer, AWSUploader
from yolo_detection import YOLODetector
from nova_reasoning import NovaAnalyzer, ReportGenerator

# Phase 1: Forensic
forensic = ForensicAnalyzer()
forensic_result = forensic.analyze_image('photo.jpg')

if forensic_result.is_authentic:
    # Upload to S3
    uploader = AWSUploader()
    s3_url = uploader.upload_evidence('photo.jpg', case_id='CASE-001')
    
    # Phase 2: YOLO
    yolo = YOLODetector()
    yolo_result = yolo.detect_from_s3(s3_url)
    
    # Phase 3: Nova
    nova = NovaAnalyzer()
    analysis = nova.analyze_case(
        case_id='CASE-001',
        forensic_data=forensic_result,
        yolo_data=yolo_result,
        image_url=s3_url
    )
    
    # Generate report
    report_gen = ReportGenerator()
    report = report_gen.generate(analysis, module='claims')
    report.save_pdf('final_report.pdf')
    
    print(f"✅ Complete analysis: {analysis.verdict}")
```

## Next Steps

- [ ] Deploy to production
- [ ] Mobile app integration
- [ ] Real-time streaming analysis
- [ ] Multi-language support
- [ ] Custom model fine-tuning

## Documentation

- [Amazon Bedrock Docs](https://docs.aws.amazon.com/bedrock/)
- [Nova Models Guide](https://aws.amazon.com/bedrock/nova/)
- [API Reference](API.md)

---

**Status**: Ready for implementation
**Phase**: 3 of 5
**Dependencies**: Phase 1 ✅, Phase 2 ✅
