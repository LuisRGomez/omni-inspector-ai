# AWS Infrastructure Initialization Script
# This script sets up the initial AWS infrastructure for Omni-Inspector AI

param(
    [Parameter(Mandatory=$true)]
    [string]$AccessKeyId,
    
    [Parameter(Mandatory=$true)]
    [string]$SecretAccessKey,
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-east-1"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AWS Infrastructure Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set AWS credentials
$env:AWS_ACCESS_KEY_ID = $AccessKeyId
$env:AWS_SECRET_ACCESS_KEY = $SecretAccessKey
$env:AWS_DEFAULT_REGION = $Region

# Test credentials
Write-Host "Testing AWS credentials..." -ForegroundColor Yellow
try {
    $identity = aws sts get-caller-identity --output json | ConvertFrom-Json
    Write-Host "OK Connected as: $($identity.Arn)" -ForegroundColor Green
    Write-Host "   Account ID: $($identity.Account)" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "ERROR: Failed to authenticate with AWS" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Create S3 bucket for evidence storage
Write-Host "Creating S3 bucket for evidence storage..." -ForegroundColor Yellow
$bucketName = "omni-inspector-evidence-$(Get-Random -Minimum 1000 -Maximum 9999)"
try {
    aws s3api create-bucket --bucket $bucketName --region $Region --create-bucket-configuration LocationConstraint=$Region 2>$null
    Write-Host "OK Bucket created: $bucketName" -ForegroundColor Green
    
    # Enable versioning
    aws s3api put-bucket-versioning --bucket $bucketName --versioning-configuration Status=Enabled
    Write-Host "OK Versioning enabled" -ForegroundColor Green
    
    # Enable encryption
    aws s3api put-bucket-encryption --bucket $bucketName --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }]
    }'
    Write-Host "OK Encryption enabled" -ForegroundColor Green
    
} catch {
    Write-Host "WARNING: Bucket creation failed (may already exist)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. GitHub repository will be created" -ForegroundColor White
Write-Host "  2. Initial code structure will be deployed" -ForegroundColor White
Write-Host "  3. Development can begin" -ForegroundColor White
Write-Host ""
