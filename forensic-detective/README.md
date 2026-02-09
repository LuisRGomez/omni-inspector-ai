# Forensic Detective Layer

## Overview

The Forensic Detective is the first layer of analysis that validates photo authenticity before AI processing. It uses pure mathematics and forensic techniques to detect tampering, extract metadata, and ensure legal validity.

## Purpose

- Detect photo manipulation (Photoshop, cloning, healing brush)
- Extract and validate GPS, timestamp, camera model
- Ensure chain of custody for legal evidence
- Reject tampered photos before expensive AI processing

## Technology Stack

- **Python 3.11+**
- **ExifTool**: Metadata extraction
- **PIL/Pillow**: Image processing
- **ELA (Error Level Analysis)**: Tampering detection
- **hashlib**: File integrity hashing

## Features

### 1. Metadata Extraction
- GPS coordinates (latitude, longitude, altitude)
- Timestamp (original, modified, digitized)
- Camera make and model
- Lens information
- ISO, aperture, shutter speed
- Image dimensions and format

### 2. Tampering Detection (ELA)
- Detects cloned regions
- Identifies healing brush usage
- Finds copy-paste manipulations
- Highlights compression inconsistencies

### 3. Integrity Verification
- SHA-256 hash generation
- File signature validation
- Format consistency checks

### 4. Legal Compliance
- Immutable metadata logging
- Chain of custody tracking
- Timestamp verification
- Geolocation validation

## Installation

```bash
cd forensic-detective
pip install -r requirements.txt
```

## Usage

```python
from forensic_detective import ForensicAnalyzer

analyzer = ForensicAnalyzer()
result = analyzer.analyze_image("path/to/image.jpg")

if result.is_authentic:
    print("Photo is authentic")
    print(f"GPS: {result.gps_coordinates}")
    print(f"Timestamp: {result.timestamp}")
else:
    print(f"Photo rejected: {result.rejection_reason}")
```

## Output Format

```json
{
  "is_authentic": true,
  "file_hash": "sha256:abc123...",
  "metadata": {
    "gps": {
      "latitude": -34.6037,
      "longitude": -58.3816,
      "altitude": 25.0
    },
    "timestamp": {
      "original": "2026-02-09T10:30:00Z",
      "modified": "2026-02-09T10:30:00Z"
    },
    "camera": {
      "make": "Apple",
      "model": "iPhone 14 Pro",
      "lens": "Main Camera"
    }
  },
  "tampering_analysis": {
    "ela_score": 0.02,
    "suspicious_regions": [],
    "is_tampered": false
  },
  "rejection_reason": null
}
```

## Integration with AWS

Photos that pass forensic analysis are uploaded to S3 with:
- Original file
- Forensic report (JSON)
- ELA analysis image
- SHA-256 hash for verification

## Next Steps

After forensic validation:
1. Photo is uploaded to S3 (WORM storage)
2. Metadata is indexed in DynamoDB
3. Photo proceeds to Layer 2 (YOLO detection)
4. Results are combined for final report
