"""
Unit tests for Forensic Analyzer
"""

import pytest
from pathlib import Path
from PIL import Image
import piexif
from datetime import datetime

from forensic_analyzer import (
    ForensicAnalyzer,
    GPSCoordinates,
    CameraInfo,
    TimestampInfo,
    TamperingAnalysis
)


class TestForensicAnalyzer:
    """Test suite for ForensicAnalyzer"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance"""
        return ForensicAnalyzer(ela_threshold=0.15)
    
    @pytest.fixture
    def sample_image_path(self, tmp_path):
        """Create a sample test image"""
        img = Image.new('RGB', (800, 600), color='blue')
        img_path = tmp_path / "test_image.jpg"
        img.save(img_path, 'JPEG', quality=95)
        return str(img_path)
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initializes correctly"""
        assert analyzer.ela_threshold == 0.15
    
    def test_file_not_found(self, analyzer):
        """Test handling of non-existent file"""
        result = analyzer.analyze_image("nonexistent.jpg")
        assert not result.is_authentic
        assert "File not found" in result.rejection_reason
    
    def test_hash_calculation(self, analyzer, sample_image_path):
        """Test SHA-256 hash calculation"""
        path = Path(sample_image_path)
        file_hash = analyzer._calculate_hash(path)
        assert file_hash.startswith("sha256:")
        assert len(file_hash) == 71  # "sha256:" + 64 hex chars
    
    def test_basic_image_analysis(self, analyzer, sample_image_path):
        """Test basic image analysis"""
        result = analyzer.analyze_image(sample_image_path)
        
        assert result.file_hash.startswith("sha256:")
        assert result.file_size > 0
        assert result.image_dimensions == (800, 600)
    
    def test_gps_coordinates_validation(self):
        """Test GPS coordinates validation"""
        # Valid GPS
        gps_valid = GPSCoordinates(latitude=-34.6037, longitude=-58.3816)
        assert gps_valid.is_valid()
        
        # Invalid GPS (missing data)
        gps_invalid = GPSCoordinates(latitude=-34.6037)
        assert not gps_invalid.is_valid()
        
        # Empty GPS
        gps_empty = GPSCoordinates()
        assert not gps_empty.is_valid()
    
    def test_timestamp_consistency(self):
        """Test timestamp consistency validation"""
        now = datetime.now()
        
        # Consistent timestamps
        ts_valid = TimestampInfo(
            original=datetime(2026, 1, 1, 10, 0, 0),
            modified=datetime(2026, 1, 1, 10, 0, 0)
        )
        assert ts_valid.is_consistent()
        
        # Inconsistent timestamps (modified before original)
        ts_invalid = TimestampInfo(
            original=datetime(2026, 1, 2, 10, 0, 0),
            modified=datetime(2026, 1, 1, 10, 0, 0)
        )
        assert not ts_invalid.is_consistent()
    
    def test_gps_coordinate_conversion(self, analyzer):
        """Test GPS coordinate conversion"""
        # Buenos Aires coordinates in EXIF format
        # -34.6037° S, -58.3816° W
        lat_tuple = ((34, 1), (36, 1), (13, 1))  # 34° 36' 13"
        lon_tuple = ((58, 1), (22, 1), (54, 1))  # 58° 22' 54"
        
        lat = analyzer._convert_gps_coordinate(lat_tuple, b'S')
        lon = analyzer._convert_gps_coordinate(lon_tuple, b'W')
        
        assert -35 < lat < -34
        assert -59 < lon < -58
    
    def test_tampering_detection_clean_image(self, analyzer, sample_image_path):
        """Test tampering detection on clean image"""
        image = Image.open(sample_image_path)
        tampering = analyzer._detect_tampering(image)
        
        assert isinstance(tampering.ela_score, float)
        assert 0 <= tampering.ela_score <= 1
        assert isinstance(tampering.suspicious_regions, list)
    
    def test_result_to_dict(self, analyzer, sample_image_path):
        """Test conversion of result to dictionary"""
        result = analyzer.analyze_image(sample_image_path)
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert 'is_authentic' in result_dict
        assert 'file_hash' in result_dict
        assert 'gps' in result_dict
        assert 'camera' in result_dict
        assert 'timestamp' in result_dict
        assert 'tampering' in result_dict
    
    def test_future_timestamp_rejection(self, analyzer):
        """Test rejection of images with future timestamps"""
        future_date = datetime(2030, 1, 1, 10, 0, 0)
        timestamp = TimestampInfo(original=future_date, modified=future_date)
        tampering = TamperingAnalysis(
            ela_score=0.05,
            suspicious_regions=[],
            is_tampered=False,
            confidence=0.95
        )
        
        is_authentic, reason = analyzer._validate_authenticity(
            GPSCoordinates(),
            timestamp,
            tampering
        )
        
        assert not is_authentic
        assert "future" in reason.lower()
    
    def test_tampering_rejection(self, analyzer):
        """Test rejection of tampered images"""
        tampering = TamperingAnalysis(
            ela_score=0.25,
            suspicious_regions=[(100, 100, 50, 50)],
            is_tampered=True,
            confidence=0.85
        )
        
        is_authentic, reason = analyzer._validate_authenticity(
            GPSCoordinates(),
            TimestampInfo(),
            tampering
        )
        
        assert not is_authentic
        assert "tampering" in reason.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
