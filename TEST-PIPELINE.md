# Test Pipeline - Quick Validation Guide

> Quick guide to test the complete AI pipeline (Phases 1-3)

## Prerequisites

1. **AWS Credentials**: Configured with access to S3, SageMaker, Bedrock
2. **Python 3.9+**: Installed on your system
3. **Test Image**: Any photo (preferably container/cargo damage)

## Setup

### 1. Install Dependencies

```bash
# Phase 1
cd forensic-detective
pip install -r requirements.txt

# Phase 2
cd ../yolo-detection
pip install -r requirements.txt

# Phase 3
cd ../nova-reasoning
pip install -r requirements.txt
```

### 2. Configure AWS

```bash
# Option 1: Environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1

# Option 2: AWS CLI profile
aws configure --profile omni-inspector
```

## Quick Test (Single Image)

### Test Phase 1: Forensic Analysis

```bash
cd forensic-detective

# Analyze a test image
python cli.py analyze ../talos-inspection-photos/20260207_091519.jpg \
  --output test_forensic.json

# Expected output:
# ✅ STATUS: AUTHENTIC
# 📁 FILE INFORMATION: Hash, size, dimensions
# 📍 GPS COORDINATES: Latitude, longitude
# 📷 CAMERA INFORMATION: Make, model, settings
# 🔍 TAMPERING ANALYSIS: ELA score, confidence
```

**Success Criteria:**
- ✅ No errors
- ✅ JSON file created
- ✅ Tampering score < 0.15 (authentic)

---

### Test Phase 2: YOLO Detection

```bash
cd ../yolo-detection

# Detect damage in image
python cli.py detect ../talos-inspection-photos/20260207_091519.jpg \
  --output test_yolo.json

# Expected output:
# 🎯 Detections: X damages found
# 📊 Severity: low/medium/high/critical
# ⏱️ Processing time: ~1s
```

**Success Criteria:**
- ✅ No errors
- ✅ JSON file created
- ✅ Detections found (if damage present)

**Note**: If SageMaker endpoint not deployed, this will use local YOLOv11 (slower but works)

---

### Test Phase 3: Nova Reasoning

```bash
cd ../nova-reasoning

# Analyze case with Nova
python cli.py analyze \
  --case-id TEST-001 \
  --forensic-report ../forensic-detective/test_forensic.json \
  --yolo-report ../yolo-detection/test_yolo.json \
  --image s3://your-bucket/test-image.jpg \
  --module claims \
  --output test_analysis.json

# Expected output:
# ┌─────────────────────┐
# │ Verdict: APPROVED   │
# └─────────────────────┘
# Confidence: 85%
# Fraud Score: 12%
# Risk Score: 3.5/10
```

**Success Criteria:**
- ✅ No errors
- ✅ JSON file created
- ✅ Verdict returned (APPROVED/REJECTED/REVIEW_REQUIRED)

**Note**: Requires AWS Bedrock access and image uploaded to S3

---

### Test Phase 3: Report Generation

```bash
# Generate PDF report
python cli.py report \
  --case-id TEST-001 \
  --analysis-report test_analysis.json \
  --module claims \
  --output test_report.pdf

# Expected output:
# ✓ Report saved to: test_report.pdf
```

**Success Criteria:**
- ✅ PDF file created
- ✅ Report contains all sections
- ✅ Verdict clearly displayed

---

## Complete Pipeline Test

Run all phases in sequence:

```bash
#!/bin/bash
# test-complete-pipeline.sh

# Configuration
TEST_IMAGE="../talos-inspection-photos/20260207_091519.jpg"
CASE_ID="TEST-$(date +%Y%m%d-%H%M%S)"
S3_BUCKET="omni-inspector-evidence-dev"

echo "🚀 Testing complete pipeline for case: $CASE_ID"

# Phase 1: Forensic
echo "📋 Phase 1: Forensic analysis..."
cd forensic-detective
python cli.py analyze "$TEST_IMAGE" --output forensic.json
if [ $? -ne 0 ]; then
    echo "❌ Phase 1 failed"
    exit 1
fi
echo "✅ Phase 1 complete"

# Upload to S3
echo "📤 Uploading to S3..."
python cli.py upload "$TEST_IMAGE" \
  --case-id "$CASE_ID" \
  --inspector-id "TEST-INS" \
  --bucket "$S3_BUCKET"
S3_URL="s3://$S3_BUCKET/evidence/$CASE_ID/$(date +%Y%m%d_%H%M%S)/original.jpg"

# Phase 2: YOLO
echo "🎯 Phase 2: YOLO detection..."
cd ../yolo-detection
python cli.py detect "$TEST_IMAGE" --output yolo.json
if [ $? -ne 0 ]; then
    echo "❌ Phase 2 failed"
    exit 1
fi
echo "✅ Phase 2 complete"

# Phase 3: Nova
echo "🧠 Phase 3: Nova reasoning..."
cd ../nova-reasoning
python cli.py analyze \
  --case-id "$CASE_ID" \
  --forensic-report ../forensic-detective/forensic.json \
  --yolo-report ../yolo-detection/yolo.json \
  --image "$S3_URL" \
  --module claims \
  --output analysis.json
if [ $? -ne 0 ]; then
    echo "❌ Phase 3 failed"
    exit 1
fi
echo "✅ Phase 3 complete"

# Generate report
echo "📄 Generating report..."
python cli.py report \
  --case-id "$CASE_ID" \
  --analysis-report analysis.json \
  --module claims \
  --output "report_$CASE_ID.pdf"
if [ $? -ne 0 ]; then
    echo "❌ Report generation failed"
    exit 1
fi
echo "✅ Report generated"

echo ""
echo "🎉 Complete pipeline test successful!"
echo "📊 Results:"
echo "   - Forensic: ../forensic-detective/forensic.json"
echo "   - YOLO: ../yolo-detection/yolo.json"
echo "   - Analysis: analysis.json"
echo "   - Report: report_$CASE_ID.pdf"
```

**Run the test:**
```bash
chmod +x test-complete-pipeline.sh
./test-complete-pipeline.sh
```

---

## Batch Test (Multiple Images)

Test with all Talos inspection photos:

```bash
cd yolo-detection

# Batch detection
python cli.py batch ../talos-inspection-photos \
  --output batch_results.json

# Expected output:
# Processing 8 images...
# ✓ 20260207_091519.jpg: 3 detections
# ✓ 20260207_091522.jpg: 2 detections
# ...
# Total: 8 images, 15 detections
```

---

## Fraud Detection Test

Test fraud detection with duplicate images:

```bash
cd nova-reasoning

# Check for fraud
python cli.py fraud-check \
  --case-id TEST-FRAUD-001 \
  --image s3://bucket/test-image.jpg \
  --forensic-report ../forensic-detective/forensic.json \
  --check-duplicates \
  --output fraud_report.json

# Expected output:
# ┌─────────────────────┐
# │ Status: CLEAN       │
# └─────────────────────┘
# Fraud Score: 12%
# Confidence: 85%
```

---

## OCR Test

Test OCR extraction:

```bash
cd nova-reasoning

# Extract container ID and seal number
python cli.py ocr \
  --image s3://bucket/container-photo.jpg \
  --extract container-id,seal-number,csc-plate \
  --output ocr_results.json

# Expected output:
# ┌─────────────────────────────────┐
# │ Field         │ Value           │
# ├─────────────────────────────────┤
# │ container-id  │ MSCU1234567     │
# │ seal-number   │ SEAL-789456     │
# │ csc-plate     │ CSC-2024-001    │
# └─────────────────────────────────┘
```

---

## Troubleshooting

### Error: "AWS credentials not found"
```bash
# Solution: Configure AWS credentials
aws configure --profile omni-inspector
```

### Error: "SageMaker endpoint not found"
```bash
# Solution: Deploy SageMaker endpoint or use local mode
cd yolo-detection
python setup_sagemaker.py
```

### Error: "Bedrock access denied"
```bash
# Solution: Enable Bedrock model access in AWS Console
# 1. Go to AWS Bedrock console
# 2. Click "Model access"
# 3. Enable "Amazon Nova Lite" and "Amazon Nova Pro"
```

### Error: "S3 bucket not found"
```bash
# Solution: Create S3 bucket
aws s3 mb s3://omni-inspector-evidence-dev
```

### Error: "Module not found"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

---

## Performance Benchmarks

Expected performance on standard hardware:

| Phase | Time | Notes |
|-------|------|-------|
| Phase 1 (Forensic) | 500ms | Local processing |
| Phase 2 (YOLO) | 1-2s | SageMaker endpoint |
| Phase 2 (YOLO Local) | 5-10s | Local YOLOv11 |
| Phase 3 (Nova) | 2-5s | Bedrock API call |
| Report (PDF) | 3-5s | Local generation |
| **Total** | **7-15s** | Complete pipeline |

---

## Success Checklist

After running tests, verify:

- [ ] Phase 1 produces valid JSON with metadata
- [ ] Phase 2 detects damages (if present)
- [ ] Phase 3 returns verdict and fraud score
- [ ] PDF report is generated correctly
- [ ] No AWS errors (credentials, permissions)
- [ ] Processing time < 15s per image
- [ ] All output files created

---

## Next Steps

Once tests pass:

1. **Deploy to production**: Setup production S3 buckets, SageMaker endpoints
2. **Build mobile app**: Phase 4 implementation
3. **Setup monitoring**: CloudWatch dashboards, alerts
4. **Load testing**: Test with 100+ concurrent requests

---

**Need Help?**
- Check [PHASE-1-COMPLETE.md](PHASE-1-COMPLETE.md) for Phase 1 details
- Check [PHASE-2-COMPLETE.md](PHASE-2-COMPLETE.md) for Phase 2 details
- Check [PHASE-3-COMPLETE.md](PHASE-3-COMPLETE.md) for Phase 3 details
- Review [PROGRESS-SUMMARY.md](PROGRESS-SUMMARY.md) for overview
