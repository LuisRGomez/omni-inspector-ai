# Required Access & Credentials

Para que pueda trabajar de forma completamente autonoma y configurar todo, necesito los siguientes accesos:

## 1. AWS (Amazon Web Services) - CRITICO

### Acceso Requerido:
- **AWS Account ID**: Tu numero de cuenta AWS
- **IAM User Credentials**:
  - Access Key ID
  - Secret Access Key
  - Region preferida (recomiendo: us-east-1)
  
### Permisos Necesarios (IAM Policies):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*",
        "dynamodb:*",
        "kinesisvideo:*",
        "bedrock:*",
        "sagemaker:*",
        "cognito-idp:*",
        "iam:*",
        "cloudformation:*",
        "lambda:*",
        "apigateway:*",
        "location:*"
      ],
      "Resource": "*"
    }
  ]
}
```

### Como Obtenerlo:
1. Entra a AWS Console (aws.amazon.com)
2. Ve a IAM > Users > Create User
3. Nombre: "kiro-agent" o "omni-inspector-dev"
4. Attach policies: AdministratorAccess (para desarrollo)
5. Security credentials > Create access key
6. Guarda Access Key ID y Secret Access Key

---

## 2. GitHub - CRITICO

### Acceso Requerido:
- **Personal Access Token (PAT)** con permisos:
  - `repo` (full control)
  - `workflow` (GitHub Actions)
  - `admin:org` (si usas organizacion)
  - `delete_repo` (para limpieza)

### Como Obtenerlo:
1. GitHub.com > Settings > Developer settings
2. Personal access tokens > Tokens (classic)
3. Generate new token
4. Selecciona los scopes mencionados
5. Copia el token (solo se muestra una vez)

### Informacion Adicional:
- **GitHub Username**: Tu usuario
- **Repository Name**: Nombre deseado (ej: "omni-inspector-ai")
- **Organization** (opcional): Si quieres usar una org

---

## 3. SSH Server (Para el MCP SSH que instalamos)

### Acceso Requerido:
- **Host**: IP o dominio del servidor
- **Port**: Puerto SSH (default: 22)
- **Username**: Usuario SSH
- **Password** o **SSH Key**: Credenciales de acceso
- **Sudo Password** (opcional): Si necesitas ejecutar comandos con sudo

### Donde Configurarlo:
Ya esta configurado en `.kiro/settings/mcp.json`
Solo necesitas reemplazar los valores YOUR_HOST, YOUR_USER, YOUR_PASSWORD

---

## 4. Domain & DNS (Opcional pero Recomendado)

### Si tienes un dominio:
- **Domain Name**: ej: omni-inspector.com
- **DNS Provider**: Route53, Cloudflare, etc.
- **API Credentials**: Para configurar DNS automaticamente

---

## 5. Mobile Development (Para React Native)

### Apple Developer (iOS):
- **Apple ID**: Para desarrollo iOS
- **Team ID**: Si tienes cuenta de desarrollador
- **Certificates**: Para firmar apps

### Google Play (Android):
- **Google Play Console Access**: Para publicar en Play Store
- **Keystore**: Para firmar APKs

---

## 6. CI/CD & Monitoring (Opcional)

### GitHub Actions:
- Ya incluido con GitHub, no requiere acceso adicional

### Sentry (Error Tracking):
- **DSN**: Para monitoreo de errores en produccion

---

## 7. Email Service (Para notificaciones)

### Amazon SES:
- Ya incluido en AWS, solo necesita configuracion

### O alternativa:
- **SendGrid API Key**
- **Mailgun API Key**

---

## Formato de Entrega de Credenciales

Por favor, proporciona las credenciales en este formato:

```
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=123456789012

GITHUB_TOKEN=ghp_...
GITHUB_USERNAME=tu-usuario
GITHUB_REPO_NAME=omni-inspector-ai

SSH_HOST=192.168.1.100
SSH_USER=admin
SSH_PASSWORD=...
SSH_PORT=22
```

---

## Seguridad

- **NUNCA** compartas estas credenciales en repositorios publicos
- Las guardare en `.env` (que esta en .gitignore)
- Usare AWS Secrets Manager para produccion
- Rotare las credenciales periodicamente

---

## Prioridad de Accesos

### AHORA (Para empezar):
1. ✅ SSH Server (ya configurado, solo falta completar datos)
2. 🔴 AWS Credentials (CRITICO - sin esto no hay proyecto)
3. 🔴 GitHub Token (CRITICO - para version control)

### PRONTO (Semana 1-2):
4. 🟡 Domain/DNS (opcional pero profesional)
5. 🟡 Mobile Developer Accounts (para testing en dispositivos reales)

### DESPUES (Cuando estemos en produccion):
6. 🟢 Monitoring tools
7. 🟢 Email service

---

## Siguiente Paso

Una vez que me proporciones:
1. AWS Access Key + Secret
2. GitHub Token
3. SSH Server completado

Podre:
- Crear toda la infraestructura AWS automaticamente
- Configurar el repositorio GitHub
- Hacer el primer deploy
- Comenzar el desarrollo

**¿Estas listo para darme estos accesos?**
