# GitHub Repository Initialization Script
# This script creates and configures the GitHub repository

param(
    [Parameter(Mandatory=$true)]
    [string]$GithubToken,
    
    [Parameter(Mandatory=$true)]
    [string]$Username,
    
    [Parameter(Mandatory=$false)]
    [string]$RepoName = "omni-inspector-ai"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GitHub Repository Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$headers = @{
    Authorization = "token $GithubToken"
    Accept = "application/vnd.github.v3+json"
}

# Check if repository exists
Write-Host "Checking if repository exists..." -ForegroundColor Yellow
try {
    $checkRepo = Invoke-RestMethod -Uri "https://api.github.com/repos/$Username/$RepoName" -Headers $headers -Method Get -ErrorAction SilentlyContinue
    Write-Host "Repository already exists: $($checkRepo.html_url)" -ForegroundColor Yellow
    $repoExists = $true
} catch {
    $repoExists = $false
}

# Create repository if it doesn't exist
if (-not $repoExists) {
    Write-Host "Creating new repository..." -ForegroundColor Yellow
    
    $body = @{
        name = $RepoName
        description = "AI-powered forensic inspection platform for InsurTech & LegalTech"
        private = $false
        auto_init = $false
        has_issues = $true
        has_projects = $true
        has_wiki = $true
    } | ConvertTo-Json
    
    try {
        $repo = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Headers $headers -Method Post -Body $body -ContentType "application/json"
        Write-Host "OK Repository created: $($repo.html_url)" -ForegroundColor Green
        Write-Host "   Clone URL: $($repo.clone_url)" -ForegroundColor Gray
    } catch {
        Write-Host "ERROR: Failed to create repository" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Using existing repository" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GitHub Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Repository: https://github.com/$Username/$RepoName" -ForegroundColor Cyan
Write-Host ""
