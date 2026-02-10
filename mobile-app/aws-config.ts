// Configuración AWS para Omni Inspector
export const awsConfig = {
  // Región
  region: 'us-east-1',
  
  // S3 - Almacenamiento de fotos
  Storage: {
    bucket: 'omni-inspector-photos-prod',
    region: 'us-east-1',
  },
  
  // API Gateway - Endpoint para análisis
  API: {
    endpoint: 'https://efjyl1of9i.execute-api.us-east-1.amazonaws.com/prod',
    analyzeEndpoint: 'https://efjyl1of9i.execute-api.us-east-1.amazonaws.com/prod/analyze'
  },
  
  // Bedrock - Análisis con IA
  Bedrock: {
    region: 'us-east-1',
    modelId: 'us.amazon.nova-pro-v1:0'
  },
  
  // Credenciales (solo para desarrollo - en producción usar Cognito)
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID || '',
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || '',
  }
};
