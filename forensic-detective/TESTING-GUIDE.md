# Testing Guide - Forensic Detective Layer

## How to Test (No UI Required)

Since we don't have a UI yet, we can test the Forensic Detective layer using:
1. Command Line Interface (CLI)
2. Python scripts
3. Unit tests
4. Sample images

## Prerequisites

### 1. Install Python Dependencies

```bash
cd forensic-detective
pip install -r requirements.txt
```

### 2. Verify AWS Configuration

```bash
aws sts get-caller-identity --profile omni-inspector
```

Should return:
```json
{
    "UserId": "AIDAW4DGOJVQ5LRH46W36",
    "Account": "472661249377",
    "Arn": "arn:aws:iam::472661249377:user/omni-inspector-agent"
}
```

## Testing Methods

### Method 1: CLI Testing (Easiest)

#### Test with Any Photo from Your Phone

1. **Take a photo with your phone** (or use any existing photo)

2. **Transfer it to your computer** (e.g., `test_photo.jpg`)

3. **Run forensic analysis**:
```bash
cd forensic-detective
python cli.py analyze test_photo.jpg
```

Expected output:
```
============================================================
FORENSIC ANALYSIS REPORT
============================================================

✅ STATUS: AUTHENTIC

📁 FILE INFORMATION:
   Hash: sha256:abc123...
   Size: 2,458,624 bytes
   Dimensions: 4032x3024

📍 GPS COORDINATES:
   Latitude: -34.603722
   Longitude: -58.381592

📷 CAMERA INFORMATION:
   Make: Apple
   Model: iPhone 14 Pro
   ...
```

4. **Save report to file**:
```bash
python cli.py analyze test_photo.jpg --output report.json
```

5. **Upload to S3** (if photo is authentic):
```bash
python cli.py upload test_photo.jpg \
  --case-id TEST-001 \
  --inspector-id YOUR-NAME
```

### Method 2: Python Script Testing

Create a test script `test_my_photo.py`:

```python
from forensic_analyzer import ForensicAnalyzer
import json

# Analyze your photo
analyzer = ForensicAnalyzer()
result = analyzer.analyze_image("test_photo.jpg")

# Print results
print(json.dumps(result.to_dict(), indent=2))

# Check if authentic
if result.is_authentic:
    print("\n✅ Photo is authentic!")
    print(f"GPS: {result.gps.latitude}, {result.gps.longitude}")
    print(f"Camera: {result.camera.make} {result.camera.model}")
else:
    print(f"\n❌ Photo rejected: {result.rejection_reason}")
```

Run it:
```bash
python test_my_photo.py
```

### Method 3: Unit Tests

Run the automated test suite:

```bash
cd forensic-detective
pytest test_forensic_analyzer.py -v
```

Expected output:
```
test_analyzer_initialization PASSED
test_file_not_found PASSED
test_hash_calculation PASSED
test_basic_image_analysis PASSED
test_gps_coordinates_validation PASSED
test_timestamp_consistency PASSED
test_gps_coordinate_conversion PASSED
test_tampering_detection_clean_image PASSED
test_result_to_dict PASSED
test_future_timestamp_rejection PASSED
test_tampering_rejection PASSED

============ 11 passed in 2.34s ============
```

### Method 4: Interactive Python

```bash
cd forensic-detective
python
```

Then in Python:
```python
from forensic_analyzer import ForensicAnalyzer

# Create analyzer
analyzer = ForensicAnalyzer()

# Analyze image
result = analyzer.analyze_image("test_photo.jpg")

# Check results
print(f"Authentic: {result.is_authentic}")
print(f"GPS: {result.gps.latitude}, {result.gps.longitude}")
print(f"Camera: {result.camera.make} {result.camera.model}")
print(f"ELA Score: {result.tampering.ela_score}")
```

## Test Scenarios

### Scenario 1: Fresh Photo from Phone
- ✅ Should pass all checks
- ✅ Should extract GPS (if location enabled)
- ✅ Should extract camera info
- ✅ Low ELA score (< 0.15)

### Scenario 2: Screenshot
- ⚠️ May fail GPS check (no GPS in screenshots)
- ⚠️ Different camera info
- ✅ Should still analyze

### Scenario 3: Edited Photo (Photoshop)
- ❌ Should detect tampering
- ❌ High ELA score
- ❌ Rejected with reason

### Scenario 4: Downloaded Image
- ⚠️ May have no GPS
- ⚠️ May have modified timestamps
- ⚠️ Depends on source

## What to Look For

### ✅ Good Signs:
- `is_authentic: true`
- GPS coordinates present
- Camera make/model detected
- Original timestamp present
- ELA score < 0.15
- No suspicious regions

### ❌ Red Flags:
- `is_authentic: false`
- High ELA score (> 0.15)
- Suspicious regions detected
- Inconsistent timestamps
- Future timestamp

## Testing Without Real Photos

If you don't have photos handy, I can create a test image generator:

```python
# Create a simple test image
from PIL import Image
import piexif

# Create image
img = Image.new('RGB', (800, 600), color='blue')

# Add fake EXIF data
exif_dict = {
    "0th": {
        piexif.ImageIFD.Make: b"TestCamera",
        piexif.ImageIFD.Model: b"Test Model"
    }
}
exif_bytes = piexif.dump(exif_dict)

# Save with EXIF
img.save("test_generated.jpg", "JPEG", exif=exif_bytes)
```

## Troubleshooting

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "AWS credentials not found"
```bash
aws configure --profile omni-inspector
# Or check ~/.aws/credentials
```

### Error: "File not found"
```bash
# Make sure you're in the forensic-detective folder
cd forensic-detective
# And the image path is correct
ls test_photo.jpg
```

### Error: "No EXIF data"
- Some images don't have EXIF (screenshots, web images)
- This is normal, analyzer will still work
- Just won't have GPS/camera info

## Next Steps After Testing

Once you verify Phase 1 works:
1. ✅ Forensic analysis working
2. ✅ S3 upload working
3. 🔄 Ready for Phase 2 (YOLO detection)
4. 🔄 Ready for mobile app integration

## Quick Test Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run unit tests
pytest test_forensic_analyzer.py -v

# 3. Analyze a photo
python cli.py analyze your_photo.jpg

# 4. Upload to S3
python cli.py upload your_photo.jpg --case-id TEST-001 --inspector-id YOUR-NAME
```

## Expected Results

### For a typical phone photo:
- ✅ Analysis time: ~500ms
- ✅ GPS extracted: Yes (if location enabled)
- ✅ Camera info: Yes
- ✅ ELA score: 0.02-0.08 (clean)
- ✅ Status: AUTHENTIC

### For an edited photo:
- ⚠️ ELA score: 0.15-0.50 (suspicious)
- ❌ Status: REJECTED
- ❌ Reason: "Image tampering detected"
