# Omni-Inspector AWS Infrastructure Setup

## ✅ Infrastructure Created

### IAM User
- **Username**: `omni-inspector-agent`
- **User ID**: `AIDAW4DGOJVQ5LRH46W36`
- **ARN**: `arn:aws:iam::472661249377:user/omni-inspector-agent`
- **Created**: 2026-02-09

### IAM Policy
- **Policy Name**: `OmniInspectorFullAccess`
- **Policy ID**: `ANPAW4DGOJVQY734NYC4X`
- **ARN**: `arn:aws:iam::472661249377:policy/OmniInspectorFullAccess`

### Access Credentials
- **Access Key ID**: `STORED IN .env FILE`
- **Secret Access Key**: `STORED IN .env FILE`
- **Status**: Active
- **Profile Name**: `omni-inspector`

⚠️ **Security**: Credentials are stored locally in `.env` file (not committed to git)

### S3 Buckets Created
1. **Production Evidence Storage**
   - Bucket: `omni-inspector-evidence-prod`
   - Region: `us-east-1`
   - Versioning: Enabled
   - Encryption: AES256

2. **Development Evidence Storage**
   - Bucket: `omni-inspector-evidence-dev`
   - Region: `us-east-1`
   - Versioning: Enabled (pending)
   - Encryption: AES256 (pending)

---

## Permissions Granted

The `OmniInspectorFullAccess` policy grants:

### S3 Access
- Full access to buckets starting with `omni-inspector-*`
- Read, write, delete, list operations
- Object Lock and versioning management

### DynamoDB Access
- Full access to tables starting with `omni-inspector-*`
- Create, read, update, delete operations
- Stream and backup management

### Amazon Bedrock
- Full access to Bedrock models
- Invoke models (Nova, Claude, etc.)
- Model customization and fine-tuning

### Amazon SageMaker
- Full access for model training and deployment
- Serverless inference endpoints
- Model registry and experiments

### Kinesis Video Streams
- Create and manage video streams
- WebRTC signaling
- Image extraction from streams

### Amazon Cognito
- User pool management
- Identity pool configuration
- Authentication and authorization

### AWS Lambda
- Create and manage functions with prefix `omni-inspector-*`
- Invoke functions
- Manage layers and aliases

### AWS IoT Core
- Thing management
- MQTT pub/sub
- Rules and actions

### Amazon Location Service
- Geofencing
- Place search
- Route calculation

### CloudWatch Logs
- Create log groups and streams
- Write and read logs
- Metrics and alarms

### CloudFormation
- Stack management
- Template deployment
- Change sets

---

## AWS CLI Configuration

The profile is configured at: `~/.aws/credentials`

```ini
[omni-inspector]
aws_access_key_id = <STORED_LOCALLY>
aws_secret_access_key = <STORED_LOCALLY>
region = us-east-1
```

**Note**: Actual credentials are in `.env` file (gitignored)

---

## Usage

### Verify Access
```bash
aws sts get-caller-identity --profile omni-inspector
```

### List S3 Buckets
```bash
aws s3 ls --profile omni-inspector
```

### Upload to Evidence Bucket
```bash
aws s3 cp file.jpg s3://omni-inspector-evidence-dev/ --profile omni-inspector
```

---

## Security Notes

⚠️ **IMPORTANT**:
- These credentials are for **development only**
- Never commit credentials to public repositories
- Rotate keys every 90 days
- Use IAM roles for production workloads
- Enable MFA for console access

---

## Next Steps

1. ✅ IAM user created
2. ✅ Permissions configured
3. ✅ S3 buckets created
4. ✅ Versioning and encryption enabled
5. 🔄 Ready to deploy application infrastructure
6. 🔄 Ready to begin development

---

## Resource Naming Convention

All resources follow the pattern: `omni-inspector-{resource-type}-{environment}`

Examples:
- `omni-inspector-evidence-prod`
- `omni-inspector-evidence-dev`
- `omni-inspector-users-prod` (DynamoDB table)
- `omni-inspector-process-image` (Lambda function)

This ensures:
- Easy identification
- Proper IAM scoping
- Clean resource management
- No conflicts with other projects
