# Complete Test Suite for Forensic Detective Layer
# This script runs all tests and demonstrations

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  FORENSIC DETECTIVE - TEST SUITE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "forensic_analyzer.py")) {
    Write-Host "ERROR: Please run this script from the forensic-detective folder" -ForegroundColor Red
    Write-Host "  cd forensic-detective" -ForegroundColor Yellow
    Write-Host "  powershell -ExecutionPolicy Bypass -File run_tests.ps1" -ForegroundColor Yellow
    exit 1
}

# Step 1: Check Python
Write-Host "Step 1: Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Python not found" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 2: Install dependencies
Write-Host "Step 2: Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 3: Create test images
Write-Host "Step 3: Creating test images..." -ForegroundColor Yellow
python create_test_image.py
Write-Host ""

# Step 4: Run unit tests
Write-Host "Step 4: Running unit tests..." -ForegroundColor Yellow
pytest test_forensic_analyzer.py -v --tb=short
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK All unit tests passed" -ForegroundColor Green
} else {
    Write-Host "  WARNING: Some tests failed" -ForegroundColor Yellow
}
Write-Host ""

# Step 5: Test CLI with clean image
Write-Host "Step 5: Testing CLI with clean image..." -ForegroundColor Yellow
Write-Host "  Analyzing: test_clean_full.jpg" -ForegroundColor Gray
python cli.py analyze test_clean_full.jpg
Write-Host ""

# Step 6: Test CLI with tampered image
Write-Host "Step 6: Testing CLI with tampered image..." -ForegroundColor Yellow
Write-Host "  Analyzing: test_tampered.jpg" -ForegroundColor Gray
python cli.py analyze test_tampered.jpg
Write-Host ""

# Step 7: Test JSON output
Write-Host "Step 7: Testing JSON output..." -ForegroundColor Yellow
python cli.py analyze test_clean_full.jpg --json --output test_report.json
if (Test-Path "test_report.json") {
    Write-Host "  OK Report saved to test_report.json" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Report not created" -ForegroundColor Red
}
Write-Host ""

# Step 8: Check AWS configuration (optional)
Write-Host "Step 8: Checking AWS configuration..." -ForegroundColor Yellow
$awsCheck = aws sts get-caller-identity --profile omni-inspector 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK AWS configured correctly" -ForegroundColor Green
    Write-Host "  You can test S3 upload with:" -ForegroundColor Cyan
    Write-Host "    python cli.py upload test_clean_full.jpg --case-id TEST-001 --inspector-id YOUR-NAME" -ForegroundColor Gray
} else {
    Write-Host "  WARNING: AWS not configured (S3 upload will not work)" -ForegroundColor Yellow
    Write-Host "  This is OK for local testing" -ForegroundColor Gray
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TEST SUITE COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Test files created:" -ForegroundColor Yellow
Write-Host "  - test_clean_full.jpg (with GPS and camera info)" -ForegroundColor White
Write-Host "  - test_clean_no_gps.jpg (without GPS)" -ForegroundColor White
Write-Host "  - test_clean_no_camera.jpg (without camera info)" -ForegroundColor White
Write-Host "  - test_tampered.jpg (should be rejected)" -ForegroundColor White
Write-Host "  - test_report.json (analysis report)" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Try with your own photos:" -ForegroundColor White
Write-Host "     python cli.py analyze your_photo.jpg" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Upload to S3 (if AWS configured):" -ForegroundColor White
Write-Host "     python cli.py upload your_photo.jpg --case-id CASE-001 --inspector-id YOUR-NAME" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. View the JSON report:" -ForegroundColor White
Write-Host "     type test_report.json" -ForegroundColor Gray
Write-Host ""
