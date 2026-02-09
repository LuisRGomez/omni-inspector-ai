"""
Create a test image with EXIF data for testing
"""

from PIL import Image
import piexif
from datetime import datetime
import random


def create_test_image(filename="test_image.jpg", with_gps=True, with_camera=True):
    """
    Create a test image with EXIF metadata
    
    Args:
        filename: Output filename
        with_gps: Include GPS coordinates
        with_camera: Include camera information
    """
    # Create a simple image
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height))
    
    # Create a gradient pattern
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            r = int((x / width) * 255)
            g = int((y / height) * 255)
            b = 128
            pixels[x, y] = (r, g, b)
    
    # Create EXIF data
    exif_dict = {
        "0th": {},
        "Exif": {},
        "GPS": {}
    }
    
    # Add camera info
    if with_camera:
        exif_dict["0th"][piexif.ImageIFD.Make] = b"TestCamera Inc."
        exif_dict["0th"][piexif.ImageIFD.Model] = b"TestCam 3000"
        exif_dict["Exif"][piexif.ExifIFD.LensModel] = b"50mm f/1.8"
        exif_dict["Exif"][piexif.ExifIFD.ISOSpeedRatings] = 200
        exif_dict["Exif"][piexif.ExifIFD.FNumber] = (18, 10)  # f/1.8
        exif_dict["Exif"][piexif.ExifIFD.ExposureTime] = (1, 125)  # 1/125s
    
    # Add timestamps
    now = datetime.now().strftime("%Y:%m:%d %H:%M:%S").encode('utf-8')
    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = now
    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = now
    
    # Add GPS coordinates (Buenos Aires, Argentina)
    if with_gps:
        # Latitude: -34.6037° S
        lat_deg = 34
        lat_min = 36
        lat_sec = 13
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = (
            (lat_deg, 1), (lat_min, 1), (lat_sec, 1)
        )
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = b'S'
        
        # Longitude: -58.3816° W
        lon_deg = 58
        lon_min = 22
        lon_sec = 54
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = (
            (lon_deg, 1), (lon_min, 1), (lon_sec, 1)
        )
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = b'W'
        
        # Altitude: 25m
        exif_dict["GPS"][piexif.GPSIFD.GPSAltitude] = (25, 1)
    
    # Convert to bytes
    exif_bytes = piexif.dump(exif_dict)
    
    # Save image with EXIF
    img.save(filename, "JPEG", quality=95, exif=exif_bytes)
    
    print(f"✅ Test image created: {filename}")
    print(f"   Size: {width}x{height}")
    print(f"   GPS: {'Yes' if with_gps else 'No'}")
    print(f"   Camera Info: {'Yes' if with_camera else 'No'}")


def create_tampered_image(filename="tampered_image.jpg"):
    """
    Create a tampered image (with visible editing)
    """
    # Create base image
    img = Image.new('RGB', (1920, 1080), color='blue')
    
    # Add a "pasted" white rectangle (simulating tampering)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([500, 300, 800, 600], fill='white')
    
    # Save without proper compression (will show high ELA)
    img.save(filename, "JPEG", quality=100)
    
    print(f"✅ Tampered image created: {filename}")
    print(f"   This should be detected as tampered")


def main():
    """Create test images"""
    print("Creating test images...\n")
    
    # 1. Clean image with full metadata
    create_test_image("test_clean_full.jpg", with_gps=True, with_camera=True)
    print()
    
    # 2. Clean image without GPS
    create_test_image("test_clean_no_gps.jpg", with_gps=False, with_camera=True)
    print()
    
    # 3. Clean image without camera info
    create_test_image("test_clean_no_camera.jpg", with_gps=True, with_camera=False)
    print()
    
    # 4. Tampered image
    create_tampered_image("test_tampered.jpg")
    print()
    
    print("="*60)
    print("Test images created successfully!")
    print("="*60)
    print("\nNow you can test with:")
    print("  python cli.py analyze test_clean_full.jpg")
    print("  python cli.py analyze test_tampered.jpg")
    print()


if __name__ == "__main__":
    main()
