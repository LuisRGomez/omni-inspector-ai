"""
Forensic Detective - Image Authenticity Analyzer
Detects tampering, extracts metadata, ensures legal validity
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass, asdict

import piexif
from PIL import Image
import numpy as np


@dataclass
class GPSCoordinates:
    """GPS coordinates extracted from image"""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    
    def is_valid(self) -> bool:
        """Check if GPS data is present and valid"""
        return self.latitude is not None and self.longitude is not None


@dataclass
class CameraInfo:
    """Camera information from EXIF"""
    make: Optional[str] = None
    model: Optional[str] = None
    lens: Optional[str] = None
    iso: Optional[int] = None
    aperture: Optional[float] = None
    shutter_speed: Optional[str] = None


@dataclass
class TimestampInfo:
    """Timestamp information"""
    original: Optional[datetime] = None
    modified: Optional[datetime] = None
    digitized: Optional[datetime] = None
    
    def is_consistent(self) -> bool:
        """Check if timestamps are consistent (not backdated)"""
        if not self.original or not self.modified:
            return False
        return self.modified >= self.original


@dataclass
class TamperingAnalysis:
    """Results of tampering detection"""
    ela_score: float
    suspicious_regions: List[Tuple[int, int, int, int]]  # (x, y, width, height)
    is_tampered: bool
    confidence: float


@dataclass
class ForensicResult:
    """Complete forensic analysis result"""
    is_authentic: bool
    file_hash: str
    file_size: int
    image_dimensions: Tuple[int, int]
    gps: GPSCoordinates
    camera: CameraInfo
    timestamp: TimestampInfo
    tampering: TamperingAnalysis
    rejection_reason: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        # Convert datetime objects to ISO format strings
        if self.timestamp.original:
            result['timestamp']['original'] = self.timestamp.original.isoformat()
        if self.timestamp.modified:
            result['timestamp']['modified'] = self.timestamp.modified.isoformat()
        if self.timestamp.digitized:
            result['timestamp']['digitized'] = self.timestamp.digitized.isoformat()
        return result


class ForensicAnalyzer:
    """
    Main forensic analyzer class
    Validates image authenticity using multiple techniques
    """
    
    def __init__(self, ela_threshold: float = 0.15):
        """
        Initialize forensic analyzer
        
        Args:
            ela_threshold: Threshold for ELA tampering detection (0.0-1.0)
        """
        self.ela_threshold = ela_threshold
    
    def analyze_image(self, image_path: str) -> ForensicResult:
        """
        Perform complete forensic analysis on an image
        
        Args:
            image_path: Path to the image file
            
        Returns:
            ForensicResult with all analysis data
        """
        path = Path(image_path)
        
        if not path.exists():
            return self._create_rejection_result("File not found")
        
        try:
            # Calculate file hash
            file_hash = self._calculate_hash(path)
            file_size = path.stat().st_size
            
            # Open image
            image = Image.open(path)
            dimensions = image.size
            
            # Extract EXIF data
            exif_data = self._extract_exif(image)
            
            # Extract GPS coordinates
            gps = self._extract_gps(exif_data)
            
            # Extract camera info
            camera = self._extract_camera_info(exif_data)
            
            # Extract timestamps
            timestamp = self._extract_timestamps(exif_data)
            
            # Perform ELA tampering detection
            tampering = self._detect_tampering(image)
            
            # Validate authenticity
            is_authentic, rejection_reason = self._validate_authenticity(
                gps, timestamp, tampering
            )
            
            return ForensicResult(
                is_authentic=is_authentic,
                file_hash=file_hash,
                file_size=file_size,
                image_dimensions=dimensions,
                gps=gps,
                camera=camera,
                timestamp=timestamp,
                tampering=tampering,
                rejection_reason=rejection_reason
            )
            
        except Exception as e:
            return self._create_rejection_result(f"Analysis error: {str(e)}")
    
    def _calculate_hash(self, path: Path) -> str:
        """Calculate SHA-256 hash of file"""
        sha256 = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return f"sha256:{sha256.hexdigest()}"
    
    def _extract_exif(self, image: Image.Image) -> Dict:
        """Extract EXIF data from image"""
        try:
            exif_dict = piexif.load(image.info.get('exif', b''))
            return exif_dict
        except:
            return {}
    
    def _extract_gps(self, exif_data: Dict) -> GPSCoordinates:
        """Extract GPS coordinates from EXIF"""
        gps_data = exif_data.get('GPS', {})
        
        if not gps_data:
            return GPSCoordinates()
        
        try:
            # Extract latitude
            lat = gps_data.get(piexif.GPSIFD.GPSLatitude)
            lat_ref = gps_data.get(piexif.GPSIFD.GPSLatitudeRef, b'N')
            
            # Extract longitude
            lon = gps_data.get(piexif.GPSIFD.GPSLongitude)
            lon_ref = gps_data.get(piexif.GPSIFD.GPSLongitudeRef, b'E')
            
            # Extract altitude
            alt = gps_data.get(piexif.GPSIFD.GPSAltitude)
            
            if lat and lon:
                latitude = self._convert_gps_coordinate(lat, lat_ref)
                longitude = self._convert_gps_coordinate(lon, lon_ref)
                altitude = float(alt[0] / alt[1]) if alt else None
                
                return GPSCoordinates(
                    latitude=latitude,
                    longitude=longitude,
                    altitude=altitude
                )
        except:
            pass
        
        return GPSCoordinates()
    
    def _convert_gps_coordinate(self, coord: Tuple, ref: bytes) -> float:
        """Convert GPS coordinate from EXIF format to decimal degrees"""
        degrees = coord[0][0] / coord[0][1]
        minutes = coord[1][0] / coord[1][1]
        seconds = coord[2][0] / coord[2][1]
        
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        
        if ref in [b'S', b'W']:
            decimal = -decimal
        
        return decimal
    
    def _extract_camera_info(self, exif_data: Dict) -> CameraInfo:
        """Extract camera information from EXIF"""
        exif_ifd = exif_data.get('Exif', {})
        image_ifd = exif_data.get('0th', {})
        
        return CameraInfo(
            make=image_ifd.get(piexif.ImageIFD.Make, b'').decode('utf-8', errors='ignore').strip(),
            model=image_ifd.get(piexif.ImageIFD.Model, b'').decode('utf-8', errors='ignore').strip(),
            lens=exif_ifd.get(piexif.ExifIFD.LensModel, b'').decode('utf-8', errors='ignore').strip(),
            iso=exif_ifd.get(piexif.ExifIFD.ISOSpeedRatings),
            aperture=self._parse_aperture(exif_ifd.get(piexif.ExifIFD.FNumber)),
            shutter_speed=self._parse_shutter_speed(exif_ifd.get(piexif.ExifIFD.ExposureTime))
        )
    
    def _parse_aperture(self, f_number) -> Optional[float]:
        """Parse aperture value from EXIF"""
        if f_number:
            return float(f_number[0] / f_number[1])
        return None
    
    def _parse_shutter_speed(self, exposure_time) -> Optional[str]:
        """Parse shutter speed from EXIF"""
        if exposure_time:
            numerator, denominator = exposure_time
            if numerator == 1:
                return f"1/{denominator}"
            else:
                return f"{numerator}/{denominator}"
        return None
    
    def _extract_timestamps(self, exif_data: Dict) -> TimestampInfo:
        """Extract timestamp information from EXIF"""
        exif_ifd = exif_data.get('Exif', {})
        
        def parse_datetime(dt_bytes):
            if not dt_bytes:
                return None
            try:
                dt_str = dt_bytes.decode('utf-8')
                return datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
            except:
                return None
        
        return TimestampInfo(
            original=parse_datetime(exif_ifd.get(piexif.ExifIFD.DateTimeOriginal)),
            modified=parse_datetime(exif_ifd.get(piexif.ExifIFD.DateTimeDigitized)),
            digitized=parse_datetime(exif_ifd.get(piexif.ExifIFD.DateTimeDigitized))
        )
    
    def _detect_tampering(self, image: Image.Image) -> TamperingAnalysis:
        """
        Detect image tampering using Error Level Analysis (ELA)
        
        ELA works by re-saving the image at a known quality level and
        comparing the difference. Tampered regions show different error levels.
        """
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save at quality 95
        import io
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=95)
        buffer.seek(0)
        
        # Reload the compressed image
        compressed = Image.open(buffer)
        
        # Calculate difference
        original_array = np.array(image, dtype=np.float32)
        compressed_array = np.array(compressed, dtype=np.float32)
        
        # Calculate absolute difference
        diff = np.abs(original_array - compressed_array)
        
        # Normalize to 0-1 range
        if diff.max() > 0:
            diff = diff / diff.max()
        
        # Calculate ELA score (average difference)
        ela_score = float(np.mean(diff))
        
        # Find suspicious regions (areas with high difference)
        threshold = self.ela_threshold
        suspicious_mask = np.mean(diff, axis=2) > threshold
        
        # Find bounding boxes of suspicious regions
        suspicious_regions = self._find_suspicious_regions(suspicious_mask)
        
        # Determine if image is tampered
        is_tampered = ela_score > self.ela_threshold or len(suspicious_regions) > 0
        confidence = min(ela_score / self.ela_threshold, 1.0) if is_tampered else 1.0 - ela_score
        
        return TamperingAnalysis(
            ela_score=ela_score,
            suspicious_regions=suspicious_regions,
            is_tampered=is_tampered,
            confidence=confidence
        )
    
    def _find_suspicious_regions(self, mask: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Find bounding boxes of suspicious regions in the mask"""
        # Simple implementation - can be improved with connected components
        regions = []
        
        # Find rows and columns with suspicious pixels
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if np.any(rows) and np.any(cols):
            y_min, y_max = np.where(rows)[0][[0, -1]]
            x_min, x_max = np.where(cols)[0][[0, -1]]
            
            regions.append((int(x_min), int(y_min), int(x_max - x_min), int(y_max - y_min)))
        
        return regions
    
    def _validate_authenticity(
        self,
        gps: GPSCoordinates,
        timestamp: TimestampInfo,
        tampering: TamperingAnalysis
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate overall image authenticity
        
        Returns:
            (is_authentic, rejection_reason)
        """
        # Check for tampering
        if tampering.is_tampered:
            return False, f"Image tampering detected (ELA score: {tampering.ela_score:.3f})"
        
        # Check timestamp consistency
        if not timestamp.is_consistent():
            return False, "Inconsistent timestamps detected"
        
        # Check if timestamp is in the future
        if timestamp.original and timestamp.original > datetime.now():
            return False, "Timestamp is in the future"
        
        # All checks passed
        return True, None
    
    def _create_rejection_result(self, reason: str) -> ForensicResult:
        """Create a rejection result"""
        return ForensicResult(
            is_authentic=False,
            file_hash="",
            file_size=0,
            image_dimensions=(0, 0),
            gps=GPSCoordinates(),
            camera=CameraInfo(),
            timestamp=TimestampInfo(),
            tampering=TamperingAnalysis(
                ela_score=0.0,
                suspicious_regions=[],
                is_tampered=False,
                confidence=0.0
            ),
            rejection_reason=reason
        )


def main():
    """Example usage"""
    analyzer = ForensicAnalyzer()
    
    # Example: analyze an image
    result = analyzer.analyze_image("test_image.jpg")
    
    print(json.dumps(result.to_dict(), indent=2))
    
    if result.is_authentic:
        print("\n✅ Image is authentic and ready for AI processing")
    else:
        print(f"\n❌ Image rejected: {result.rejection_reason}")


if __name__ == "__main__":
    main()
