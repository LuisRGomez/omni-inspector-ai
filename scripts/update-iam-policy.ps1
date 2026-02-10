# Update IAM policy for omni-inspector-agent
# Adds SageMaker and IAM role management permissions

$ErrorActionPreference = "Stop"

Write-Host "Updating IAM policy for omni-inspector-agent..." -ForegroundColor Cyan
Write-Host ""

# Get policy ARN
$policyName = "OmniInspectorFullAccess"
$accountId = (aws sts get-caller-identity --profile vscuser --query Account --output text)
$policyArn = "arn:aws:iam::${accountId}:policy/${policyName}"

Write-Host "Policy ARN: $policyArn" -ForegroundColor Gray
Write-Host ""

# Create new policy version
Write-Host "Creating new policy version..." -ForegroundColor Yellow

aws iam create-policy-version `
    --profile vscuser `
    --policy-arn $policyArn `
    --policy-document file://../aws-config/omni-inspector-policy.json `
    --set-as-default

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Policy updated successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "New permissions added:" -ForegroundColor Cyan
    Write-Host "  • iam:GetRole" -ForegroundColor White
    Write-Host "  • iam:CreateRole" -ForegroundColor White
    Write-Host "  • iam:AttachRolePolicy" -ForegroundColor White
    Write-Host "  • iam:ListAttachedRolePolicies" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "❌ Failed to update policy" -ForegroundColor Red
    exit 1
}
