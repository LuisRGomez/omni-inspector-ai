# Complete Pipeline Test Script (PowerShell)
# Tests all 3 phases of Omni-Inspector AI

param(
    [string]$TestImage = "talos-inspection-photos\20260207_091519.jpg",
    [string]$S3Bucket = "omni-inspector-evidence-dev",
    [string]$Module = "claims"
)

$ErrorActionPreference = "Stop"

# Configuration
$CaseId = "TEST-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$InspectorId = "TEST-INS"

Write-Host "`n🚀 Testing complete pipeline for case: $CaseId`n" -ForegroundColor Cyan

# Check if test image exists
if (-not (Test-Path $TestImage)) {
    Write-Host "❌ Test image not found: $TestImage" -ForegroundColor Red
    exit 1
}

# Phase 1: Forensic Analysis
Write-Host "📋 Phase 1: Forensic analysis..." -ForegroundColor Yellow
Set-Location forensic-detective

try {
    python cli.py analyze "..\$TestImage" --output forensic.json
    if ($LASTEXITCODE -ne 0) { throw "Phase 1 failed" }
    Write-Host "✅ Phase 1 complete`n" -ForegroundColor Green
} catch {
    Write-Host "❌ Phase 1 failed: $_" -ForegroundColor Red
    Set-Location ..
    exit 1
}

# Upload to S3 (optional, comment out if S3 not configured)
Write-Host "📤 Uploading to S3..." -ForegroundColor Yellow
try {
    python cli.py upload "..\$TestImage" `
        --case-id $CaseId `
        --inspector-id $InspectorId `
        --bucket $S3Bucket
    
    $Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $S3Url = "s3://$S3Bucket/evidence/$CaseId/$Timestamp/original.jpg"
    Write-Host "✅ Uploaded to: $S3Url`n" -ForegroundColor Green
} catch {
    Write-Host "⚠️ S3 upload skipped (bucket not configured)`n" -ForegroundColor Yellow
    $S3Url = "s3://$S3Bucket/test/image.jpg"
}

Set-Location ..

# Phase 2: YOLO Detection
Write-Host "🎯 Phase 2: YOLO detection..." -ForegroundColor Yellow
Set-Location yolo-detection

try {
    python cli.py detect "..\$TestImage" --output yolo.json
    if ($LASTEXITCODE -ne 0) { throw "Phase 2 failed" }
    Write-Host "✅ Phase 2 complete`n" -ForegroundColor Green
} catch {
    Write-Host "❌ Phase 2 failed: $_" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Set-Location ..

# Phase 3: Nova Reasoning
Write-Host "🧠 Phase 3: Nova reasoning..." -ForegroundColor Yellow
Set-Location nova-reasoning

try {
    python cli.py analyze `
        --case-id $CaseId `
        --forensic-report "..\forensic-detective\forensic.json" `
        --yolo-report "..\yolo-detection\yolo.json" `
        --image $S3Url `
        --module $Module `
        --output analysis.json
    
    if ($LASTEXITCODE -ne 0) { throw "Phase 3 failed" }
    Write-Host "✅ Phase 3 complete`n" -ForegroundColor Green
} catch {
    Write-Host "❌ Phase 3 failed: $_" -ForegroundColor Red
    Write-Host "⚠️ Note: Phase 3 requires AWS Bedrock access and S3 upload" -ForegroundColor Yellow
    Set-Location ..
    exit 1
}

# Generate Report
Write-Host "📄 Generating report..." -ForegroundColor Yellow
try {
    $ReportFile = "report_$CaseId.pdf"
    python cli.py report `
        --case-id $CaseId `
        --analysis-report analysis.json `
        --module $Module `
        --output $ReportFile
    
    if ($LASTEXITCODE -ne 0) { throw "Report generation failed" }
    Write-Host "✅ Report generated: $ReportFile`n" -ForegroundColor Green
} catch {
    Write-Host "❌ Report generation failed: $_" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Set-Location ..

# Summary
Write-Host "`n🎉 Complete pipeline test successful!`n" -ForegroundColor Green
Write-Host "📊 Results:" -ForegroundColor Cyan
Write-Host "   - Case ID: $CaseId"
Write-Host "   - Forensic: forensic-detective\forensic.json"
Write-Host "   - YOLO: yolo-detection\yolo.json"
Write-Host "   - Analysis: nova-reasoning\analysis.json"
Write-Host "   - Report: nova-reasoning\report_$CaseId.pdf"
Write-Host ""

# Display analysis summary
Write-Host "📋 Analysis Summary:" -ForegroundColor Cyan
try {
    $Analysis = Get-Content "nova-reasoning\analysis.json" | ConvertFrom-Json
    Write-Host "   - Verdict: $($Analysis.verdict)" -ForegroundColor $(
        if ($Analysis.verdict -eq "APPROVED") { "Green" }
        elseif ($Analysis.verdict -eq "REJECTED") { "Red" }
        else { "Yellow" }
    )
    Write-Host "   - Confidence: $([math]::Round($Analysis.confidence * 100, 1))%"
    Write-Host "   - Fraud Score: $([math]::Round($Analysis.fraud_score * 100, 1))%"
    Write-Host "   - Risk Score: $($Analysis.risk_score)/10"
    Write-Host "   - Damages: $($Analysis.damages.Count)"
    Write-Host "   - Processing Time: $($Analysis.processing_time_ms)ms"
} catch {
    Write-Host "   (Could not parse analysis.json)" -ForegroundColor Yellow
}

Write-Host "`n✅ All tests passed!`n" -ForegroundColor Green
