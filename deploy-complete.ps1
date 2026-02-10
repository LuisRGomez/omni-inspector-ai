# Deploy completo de Omni Inspector
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEPLOY COMPLETO - OMNI INSPECTOR" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Continue"

# 1. Adjuntar políticas al rol
Write-Host "1. Configurando permisos IAM..." -ForegroundColor Yellow
aws iam attach-role-policy --role-name OmniInspectorLambdaRole --policy-arn "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole" 2>$null
aws iam attach-role-policy --role-name OmniInspectorLambdaRole --policy-arn "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess" 2>$null
aws iam attach-role-policy --role-name OmniInspectorLambdaRole --policy-arn "arn:aws:iam::aws:policy/AmazonBedrockFullAccess" 2>$null
Write-Host "   Permisos configurados!" -ForegroundColor Green

# 2. Esperar propagación
Write-Host ""
Write-Host "2. Esperando propagación de permisos (10s)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
Write-Host "   Listo!" -ForegroundColor Green

# 3. Crear zip de Lambda
Write-Host ""
Write-Host "3. Empaquetando Lambda..." -ForegroundColor Yellow
if (Test-Path "lambda-function.zip") {
    Remove-Item "lambda-function.zip" -Force
}
Compress-Archive -Path "lambda-bedrock-analyzer.py" -DestinationPath "lambda-function.zip" -Force
Write-Host "   Lambda empaquetada!" -ForegroundColor Green

# 4. Verificar si Lambda existe
Write-Host ""
Write-Host "4. Verificando Lambda existente..." -ForegroundColor Yellow
$lambdaExists = aws lambda get-function --function-name omni-inspector-bedrock-analyzer --region us-east-1 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   Lambda existe, actualizando..." -ForegroundColor Yellow
    aws lambda update-function-code `
        --function-name omni-inspector-bedrock-analyzer `
        --zip-file fileb://lambda-function.zip `
        --region us-east-1
    Write-Host "   Lambda actualizada!" -ForegroundColor Green
} else {
    Write-Host "   Lambda no existe, creando..." -ForegroundColor Yellow
    aws lambda create-function `
        --function-name omni-inspector-bedrock-analyzer `
        --runtime python3.11 `
        --role arn:aws:iam::472661249377:role/OmniInspectorLambdaRole `
        --handler lambda-bedrock-analyzer.lambda_handler `
        --zip-file fileb://lambda-function.zip `
        --timeout 60 `
        --memory-size 512 `
        --region us-east-1
    Write-Host "   Lambda creada!" -ForegroundColor Green
}

# 5. Crear/Verificar API Gateway
Write-Host ""
Write-Host "5. Configurando API Gateway..." -ForegroundColor Yellow

# Verificar si API existe
$apiList = aws apigateway get-rest-apis --region us-east-1 | ConvertFrom-Json
$existingApi = $apiList.items | Where-Object { $_.name -eq "OmniInspectorAPI" }

if ($existingApi) {
    $apiId = $existingApi.id
    Write-Host "   API Gateway existe: $apiId" -ForegroundColor Green
} else {
    Write-Host "   Creando API Gateway..." -ForegroundColor Yellow
    $apiResult = aws apigateway create-rest-api --name OmniInspectorAPI --region us-east-1 | ConvertFrom-Json
    $apiId = $apiResult.id
    Write-Host "   API Gateway creada: $apiId" -ForegroundColor Green
    
    # Obtener root resource
    $resources = aws apigateway get-resources --rest-api-id $apiId --region us-east-1 | ConvertFrom-Json
    $rootId = $resources.items[0].id
    
    # Crear recurso /analyze
    $analyzeResource = aws apigateway create-resource `
        --rest-api-id $apiId `
        --parent-id $rootId `
        --path-part analyze `
        --region us-east-1 | ConvertFrom-Json
    $analyzeId = $analyzeResource.id
    
    # Crear método POST
    aws apigateway put-method `
        --rest-api-id $apiId `
        --resource-id $analyzeId `
        --http-method POST `
        --authorization-type NONE `
        --region us-east-1
    
    # Integrar con Lambda
    $lambdaArn = "arn:aws:lambda:us-east-1:472661249377:function:omni-inspector-bedrock-analyzer"
    aws apigateway put-integration `
        --rest-api-id $apiId `
        --resource-id $analyzeId `
        --http-method POST `
        --type AWS_PROXY `
        --integration-http-method POST `
        --uri "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/$lambdaArn/invocations" `
        --region us-east-1
    
    # Dar permiso a API Gateway para invocar Lambda
    aws lambda add-permission `
        --function-name omni-inspector-bedrock-analyzer `
        --statement-id apigateway-invoke `
        --action lambda:InvokeFunction `
        --principal apigateway.amazonaws.com `
        --source-arn "arn:aws:execute-api:us-east-1:472661249377:$apiId/*/*" `
        --region us-east-1
    
    # Deploy API
    aws apigateway create-deployment `
        --rest-api-id $apiId `
        --stage-name prod `
        --region us-east-1
    
    Write-Host "   API Gateway configurada completamente!" -ForegroundColor Green
}

# 6. Mostrar endpoint
$apiEndpoint = "https://$apiId.execute-api.us-east-1.amazonaws.com/prod/analyze"
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEPLOY COMPLETADO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Lambda Function:" -ForegroundColor Yellow
Write-Host "  omni-inspector-bedrock-analyzer" -ForegroundColor White
Write-Host ""
Write-Host "API Endpoint:" -ForegroundColor Yellow
Write-Host "  $apiEndpoint" -ForegroundColor White
Write-Host ""
Write-Host "S3 Bucket:" -ForegroundColor Yellow
Write-Host "  omni-inspector-photos-prod" -ForegroundColor White
Write-Host ""
Write-Host "Siguiente paso: Actualizar mobile-app/aws-config.ts con el endpoint" -ForegroundColor Cyan
Write-Host ""

# Guardar endpoint en archivo
$apiEndpoint | Out-File -FilePath "api-endpoint.txt" -Encoding UTF8
Write-Host "Endpoint guardado en: api-endpoint.txt" -ForegroundColor Green
Write-Host ""
