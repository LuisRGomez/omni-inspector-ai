@echo off
echo ========================================
echo Desplegando Lambda para Bedrock
echo ========================================
echo.

echo Paso 1: Creando rol IAM...
aws iam create-role --role-name OmniInspectorLambdaRole --assume-role-policy-document "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"

echo.
echo Paso 2: Adjuntando políticas...
aws iam attach-role-policy --role-name OmniInspectorLambdaRole --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name OmniInspectorLambdaRole --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
aws iam attach-role-policy --role-name OmniInspectorLambdaRole --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

echo.
echo Esperando 10 segundos para que el rol se propague...
timeout /t 10 /nobreak

echo.
echo Paso 3: Empaquetando Lambda...
powershell Compress-Archive -Path lambda-bedrock-analyzer.py -DestinationPath lambda-function.zip -Force

echo.
echo Paso 4: Creando función Lambda...
aws lambda create-function ^
  --function-name omni-inspector-bedrock-analyzer ^
  --runtime python3.11 ^
  --role arn:aws:iam::472661249377:role/OmniInspectorLambdaRole ^
  --handler lambda-bedrock-analyzer.lambda_handler ^
  --zip-file fileb://lambda-function.zip ^
  --timeout 60 ^
  --memory-size 512 ^
  --region us-east-1

echo.
echo ========================================
echo Lambda desplegada!
echo ========================================
echo.
echo Nombre: omni-inspector-bedrock-analyzer
echo Region: us-east-1
echo.
pause
