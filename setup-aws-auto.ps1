# Setup AWS Automatizado - Omni-Inspector AI
# Este script verifica y configura AWS para las Fases 2 y 3

param(
    [switch]$SkipCredentials,
    [switch]$SkipBedrock,
    [switch]$SkipSageMaker
)

$ErrorActionPreference = "Continue"

Write-Host "`n🚀 Setup AWS Automatizado - Omni-Inspector AI`n" -ForegroundColor Cyan

# Función para verificar comando
function Test-Command {
    param($Command)
    try {
        & $Command 2>&1 | Out-Null
        return $true
    } catch {
        return $false
    }
}

# ============================================================
# PASO 1: Verificar Credenciales AWS
# ============================================================

if (-not $SkipCredentials) {
    Write-Host "📋 Paso 1: Verificando credenciales AWS..." -ForegroundColor Yellow
    
    try {
        $identity = aws sts get-caller-identity 2>&1 | ConvertFrom-Json
        
        if ($identity.Account) {
            Write-Host "✅ Credenciales AWS válidas" -ForegroundColor Green
            Write-Host "   Account: $($identity.Account)" -ForegroundColor Gray
            Write-Host "   User: $($identity.Arn)" -ForegroundColor Gray
        } else {
            throw "No se pudo obtener identidad"
        }
    } catch {
        Write-Host "❌ Error en credenciales AWS" -ForegroundColor Red
        Write-Host "`n⚠️  ACCIÓN REQUERIDA:" -ForegroundColor Yellow
        Write-Host "   1. Ve a AWS Console → Security Credentials"
        Write-Host "   2. Crea un nuevo Access Key"
        Write-Host "   3. Ejecuta: aws configure"
        Write-Host "   4. Ingresa tus credenciales`n"
        
        $configure = Read-Host "¿Quieres configurar credenciales ahora? (s/n)"
        if ($configure -eq 's') {
            aws configure
            
            # Verificar nuevamente
            try {
                $identity = aws sts get-caller-identity | ConvertFrom-Json
                Write-Host "✅ Credenciales configuradas correctamente" -ForegroundColor Green
            } catch {
                Write-Host "❌ Error al configurar credenciales. Verifica e intenta de nuevo." -ForegroundColor Red
                exit 1
            }
        } else {
            Write-Host "`n⚠️  Configura credenciales y ejecuta este script nuevamente.`n" -ForegroundColor Yellow
            exit 1
        }
    }
    
    Write-Host ""
}

# ============================================================
# PASO 2: Verificar Acceso a Bedrock
# ============================================================

if (-not $SkipBedrock) {
    Write-Host "📋 Paso 2: Verificando acceso a Amazon Bedrock..." -ForegroundColor Yellow
    
    try {
        $models = aws bedrock list-foundation-models --region us-east-1 2>&1 | ConvertFrom-Json
        
        if ($models.modelSummaries) {
            # Buscar modelos Nova
            $novaModels = $models.modelSummaries | Where-Object { $_.modelId -like "*nova*" }
            
            if ($novaModels.Count -gt 0) {
                Write-Host "✅ Acceso a Bedrock confirmado" -ForegroundColor Green
                Write-Host "   Modelos Nova disponibles: $($novaModels.Count)" -ForegroundColor Gray
                
                foreach ($model in $novaModels) {
                    Write-Host "   - $($model.modelId)" -ForegroundColor Gray
                }
            } else {
                Write-Host "⚠️  Bedrock accesible pero modelos Nova no habilitados" -ForegroundColor Yellow
                Write-Host "`n⚠️  ACCIÓN REQUERIDA:" -ForegroundColor Yellow
                Write-Host "   1. Ve a: https://console.aws.amazon.com/bedrock/"
                Write-Host "   2. Click en 'Model access' (menú izquierdo)"
                Write-Host "   3. Click en 'Manage model access'"
                Write-Host "   4. Habilita: Amazon Nova Lite y Amazon Nova Pro"
                Write-Host "   5. Click 'Save changes'"
                Write-Host "   6. Espera 2-5 minutos`n"
                
                $open = Read-Host "¿Abrir Bedrock Console en navegador? (s/n)"
                if ($open -eq 's') {
                    Start-Process "https://console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess"
                }
            }
        } else {
            throw "No se pudieron listar modelos"
        }
    } catch {
        Write-Host "❌ Error al acceder a Bedrock" -ForegroundColor Red
        Write-Host "   Error: $_" -ForegroundColor Gray
        Write-Host "`n⚠️  POSIBLES CAUSAS:" -ForegroundColor Yellow
        Write-Host "   1. Bedrock no disponible en tu región (usa us-east-1)"
        Write-Host "   2. Permisos IAM insuficientes"
        Write-Host "   3. Cuenta AWS requiere aprobación manual`n"
    }
    
    Write-Host ""
}

# ============================================================
# PASO 3: Verificar SageMaker
# ============================================================

if (-not $SkipSageMaker) {
    Write-Host "📋 Paso 3: Verificando SageMaker..." -ForegroundColor Yellow
    
    try {
        # Verificar si existe el endpoint
        $endpoints = aws sagemaker list-endpoints --region us-east-1 2>&1 | ConvertFrom-Json
        
        $omniEndpoint = $endpoints.Endpoints | Where-Object { $_.EndpointName -like "*omni-inspector*" }
        
        if ($omniEndpoint) {
            Write-Host "✅ Endpoint SageMaker encontrado" -ForegroundColor Green
            Write-Host "   Nombre: $($omniEndpoint.EndpointName)" -ForegroundColor Gray
            Write-Host "   Estado: $($omniEndpoint.EndpointStatus)" -ForegroundColor Gray
            
            if ($omniEndpoint.EndpointStatus -ne "InService") {
                Write-Host "⚠️  Endpoint no está en servicio" -ForegroundColor Yellow
            }
        } else {
            Write-Host "⚠️  No se encontró endpoint de Omni-Inspector" -ForegroundColor Yellow
            Write-Host "`n⚠️  ACCIÓN REQUERIDA:" -ForegroundColor Yellow
            Write-Host "   Ejecuta el script de setup de SageMaker:`n"
            Write-Host "   cd yolo-detection" -ForegroundColor Cyan
            Write-Host "   python setup_sagemaker.py`n" -ForegroundColor Cyan
            
            $setup = Read-Host "¿Ejecutar setup de SageMaker ahora? (s/n)"
            if ($setup -eq 's') {
                Write-Host "`n🚀 Ejecutando setup de SageMaker..." -ForegroundColor Cyan
                Write-Host "⏱️  Esto puede tomar 20-30 minutos...`n" -ForegroundColor Yellow
                
                Set-Location yolo-detection
                python setup_sagemaker.py
                Set-Location ..
                
                Write-Host "`n✅ Setup de SageMaker completado" -ForegroundColor Green
            }
        }
    } catch {
        Write-Host "❌ Error al verificar SageMaker" -ForegroundColor Red
        Write-Host "   Error: $_" -ForegroundColor Gray
    }
    
    Write-Host ""
}

# ============================================================
# PASO 4: Verificar Buckets S3
# ============================================================

Write-Host "📋 Paso 4: Verificando buckets S3..." -ForegroundColor Yellow

try {
    $buckets = aws s3 ls 2>&1
    
    $evidenceBucket = $buckets | Select-String "omni-inspector-evidence"
    $modelsBucket = $buckets | Select-String "omni-inspector-models"
    
    if ($evidenceBucket) {
        Write-Host "✅ Bucket de evidencia encontrado" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Bucket de evidencia no encontrado" -ForegroundColor Yellow
        
        $create = Read-Host "¿Crear bucket de evidencia? (s/n)"
        if ($create -eq 's') {
            $accountId = (aws sts get-caller-identity | ConvertFrom-Json).Account
            $bucketName = "omni-inspector-evidence-$accountId"
            
            aws s3 mb "s3://$bucketName" --region us-east-1
            Write-Host "✅ Bucket creado: $bucketName" -ForegroundColor Green
        }
    }
    
    if ($modelsBucket) {
        Write-Host "✅ Bucket de modelos encontrado" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Bucket de modelos no encontrado (se creará con setup_sagemaker.py)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error al verificar buckets S3" -ForegroundColor Red
}

Write-Host ""

# ============================================================
# RESUMEN
# ============================================================

Write-Host "📊 Resumen de Configuración`n" -ForegroundColor Cyan

Write-Host "Estado de Servicios:" -ForegroundColor White
Write-Host "  [ ] Credenciales AWS" -ForegroundColor Gray
Write-Host "  [ ] Amazon Bedrock (Nova)" -ForegroundColor Gray
Write-Host "  [ ] SageMaker Endpoint" -ForegroundColor Gray
Write-Host "  [ ] Buckets S3`n" -ForegroundColor Gray

Write-Host "Próximos Pasos:" -ForegroundColor White
Write-Host "  1. Habilitar modelos Nova en Bedrock Console" -ForegroundColor Gray
Write-Host "  2. Ejecutar: cd yolo-detection; python setup_sagemaker.py" -ForegroundColor Gray
Write-Host "  3. Probar pipeline: .\test-complete-pipeline.ps1`n" -ForegroundColor Gray

Write-Host "Documentación:" -ForegroundColor White
Write-Host "  - SETUP-AWS-COMPLETO.md (guía detallada)" -ForegroundColor Gray
Write-Host "  - TEST-RESULTS.md (resultados de pruebas)" -ForegroundColor Gray
Write-Host "  - NEXT-ACTIONS.md (próximos pasos)`n" -ForegroundColor Gray

Write-Host "✅ Verificación completada`n" -ForegroundColor Green
