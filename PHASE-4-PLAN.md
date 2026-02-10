# Phase 4: Mobile App & Backend - Implementation Plan

## Overview

Phase 4 builds the user-facing mobile application and serverless backend infrastructure. This connects all AI layers (Phases 1-3) into a production-ready system.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Mobile App (React Native)                │
│  • Camera (4K capture)                                      │
│  • Case management                                          │
│  • Offline mode                                             │
│  • Report viewing                                           │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS/REST API
┌────────────────────┴────────────────────────────────────────┐
│                    API Gateway + Lambda                     │
│  • Authentication (Cognito)                                 │
│  • Request routing                                          │
│  • Rate limiting                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                    Orchestration Lambda                     │
│  • Phase 1: Forensic validation                             │
│  • Phase 2: YOLO detection                                  │
│  • Phase 3: Nova reasoning                                  │
│  • Report generation                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                    Data Layer                               │
│  • DynamoDB (cases, users, reports)                         │
│  • S3 (images, evidence, reports)                           │
│  • Cognito (user management)                                │
└─────────────────────────────────────────────────────────────┘
```

## Components to Build

### 1. Mobile App (React Native + Expo)

**Tech Stack:**
- React Native 0.73+
- Expo SDK 50+
- React Navigation 6
- React Query (data fetching)
- Zustand (state management)
- Expo Camera (4K capture)

**Features:**
- 📸 Camera integration (4K, HDR)
- 📁 Case management (create, view, edit)
- 📊 Dashboard (statistics, recent cases)
- 📄 Report viewing (PDF, JSON)
- 🔒 Authentication (Cognito)
- 📴 Offline mode (local storage)
- 🌐 Multi-language (EN, ES, PT)

**Screens:**
1. Login/Register
2. Dashboard
3. New Inspection
4. Camera Capture
5. Case Details
6. Report Viewer
7. Settings

### 2. Backend (AWS Serverless)

**Infrastructure:**
- API Gateway (REST API)
- Lambda Functions (Node.js 20 or Python 3.12)
- DynamoDB (multi-tenant)
- S3 (evidence storage)
- Cognito (authentication)
- CloudWatch (monitoring)

**Lambda Functions:**

#### `inspection-orchestrator`
- Receives image from mobile app
- Triggers Phase 1 (forensic)
- Triggers Phase 2 (YOLO)
- Triggers Phase 3 (Nova)
- Returns complete analysis

#### `case-manager`
- CRUD operations for cases
- Multi-tenant isolation
- Query by inspector, date, status

#### `report-generator`
- Generates PDF reports
- Stores in S3
- Returns signed URL

#### `auth-handler`
- Cognito integration
- JWT validation
- User profile management

### 3. DynamoDB Schema

**Tables:**

#### `Cases`
```json
{
  "PK": "TENANT#<tenant_id>",
  "SK": "CASE#<case_id>",
  "case_id": "CASE-2026-001",
  "inspector_id": "INS-123",
  "module": "claims",
  "status": "completed",
  "created_at": "2026-02-09T10:00:00Z",
  "forensic_report": {...},
  "yolo_report": {...},
  "nova_report": {...},
  "verdict": "APPROVED",
  "fraud_score": 0.12,
  "estimated_cost": 15000
}
```

#### `Users`
```json
{
  "PK": "USER#<user_id>",
  "SK": "PROFILE",
  "user_id": "USR-123",
  "email": "inspector@company.com",
  "role": "inspector",
  "tenant_id": "TENANT-001",
  "created_at": "2026-01-01T00:00:00Z"
}
```

#### `Reports`
```json
{
  "PK": "CASE#<case_id>",
  "SK": "REPORT#<timestamp>",
  "report_id": "RPT-001",
  "format": "pdf",
  "s3_url": "s3://bucket/reports/...",
  "generated_at": "2026-02-09T10:30:00Z"
}
```

### 4. API Endpoints

#### Authentication
- `POST /auth/login` - Login with Cognito
- `POST /auth/register` - Register new user
- `POST /auth/refresh` - Refresh JWT token

#### Cases
- `POST /cases` - Create new case
- `GET /cases` - List cases (paginated)
- `GET /cases/{id}` - Get case details
- `PUT /cases/{id}` - Update case
- `DELETE /cases/{id}` - Delete case

#### Inspections
- `POST /inspections` - Start new inspection
- `POST /inspections/{id}/upload` - Upload image
- `GET /inspections/{id}/status` - Check processing status
- `GET /inspections/{id}/result` - Get analysis result

#### Reports
- `POST /reports` - Generate report
- `GET /reports/{id}` - Get report (signed URL)
- `GET /reports/{id}/download` - Download PDF

## Implementation Steps

### Step 1: Backend Infrastructure (Week 1)

**Day 1-2: AWS Setup**
```bash
# Create DynamoDB tables
aws dynamodb create-table --table-name omni-inspector-cases ...
aws dynamodb create-table --table-name omni-inspector-users ...

# Create S3 buckets
aws s3 mb s3://omni-inspector-evidence-prod
aws s3 mb s3://omni-inspector-reports-prod

# Setup Cognito
aws cognito-idp create-user-pool --pool-name omni-inspector-users
```

**Day 3-4: Lambda Functions**
- Implement orchestration Lambda
- Implement case manager Lambda
- Implement report generator Lambda
- Deploy with SAM or CDK

**Day 5: API Gateway**
- Create REST API
- Configure routes
- Setup CORS
- Add authentication

### Step 2: Mobile App (Week 2-3)

**Day 1-2: Project Setup**
```bash
npx create-expo-app omni-inspector-mobile
cd omni-inspector-mobile
npm install @react-navigation/native @react-navigation/stack
npm install react-query zustand
npm install expo-camera expo-file-system
```

**Day 3-5: Core Screens**
- Login/Register screen
- Dashboard screen
- Camera capture screen
- Case list screen

**Day 6-7: API Integration**
- Setup API client (Axios)
- Implement authentication flow
- Connect to backend endpoints

**Day 8-10: Offline Mode**
- Local storage (AsyncStorage)
- Queue system for uploads
- Sync when online

### Step 3: Integration & Testing (Week 4)

**Day 1-2: End-to-End Testing**
- Test complete inspection flow
- Test offline mode
- Test report generation

**Day 3-4: Performance Optimization**
- Image compression
- Lazy loading
- Caching strategies

**Day 5: Documentation**
- API documentation
- Mobile app user guide
- Deployment guide

## Mobile App Screens

### 1. Login Screen
```typescript
// Features:
- Email/password login
- Cognito integration
- Remember me option
- Forgot password
```

### 2. Dashboard
```typescript
// Features:
- Recent cases (last 10)
- Statistics (total cases, pending, completed)
- Quick actions (new inspection, view reports)
- Notifications
```

### 3. New Inspection
```typescript
// Features:
- Select module (underwriting, claims, legal)
- Enter case details
- Add notes
- Start camera
```

### 4. Camera Capture
```typescript
// Features:
- 4K capture
- HDR mode
- Grid overlay
- Flash control
- Gallery preview
```

### 5. Case Details
```typescript
// Features:
- View forensic data
- View YOLO detections
- View Nova analysis
- Generate report
- Share report
```

## Cost Estimation

### AWS Services (Monthly, 1,000 inspections)

**Lambda:**
- Orchestration: 1,000 invocations × 10s = $0.20
- Case manager: 5,000 invocations × 1s = $0.10
- Report generator: 1,000 invocations × 5s = $0.10
- **Total Lambda**: $0.40

**API Gateway:**
- 10,000 requests = $0.035
- **Total API Gateway**: $0.04

**DynamoDB:**
- 10,000 writes = $1.25
- 50,000 reads = $0.25
- Storage (1GB) = $0.25
- **Total DynamoDB**: $1.75

**S3:**
- Storage (100GB) = $2.30
- Requests (10,000) = $0.05
- **Total S3**: $2.35

**Cognito:**
- 1,000 MAU = Free (under 50,000)
- **Total Cognito**: $0.00

**AI Services (from Phases 1-3):**
- Forensic + YOLO + Nova = $2.60

**Total Monthly Cost**: ~$7.14 (1,000 inspections)
**Cost per Inspection**: ~$0.007

## Security

### Authentication
- ✅ Cognito JWT tokens
- ✅ Token refresh mechanism
- ✅ Secure storage (Keychain/Keystore)

### API Security
- ✅ HTTPS only
- ✅ API key validation
- ✅ Rate limiting (100 req/min)
- ✅ CORS configuration

### Data Security
- ✅ S3 encryption (AES-256)
- ✅ DynamoDB encryption at rest
- ✅ Multi-tenant isolation
- ✅ IAM least privilege

### Mobile Security
- ✅ Certificate pinning
- ✅ Secure storage (expo-secure-store)
- ✅ Biometric authentication (optional)
- ✅ Jailbreak/root detection

## Performance Targets

- **API Response Time**: < 200ms (excluding AI processing)
- **Image Upload**: < 5s (4K image)
- **Complete Analysis**: < 15s (all 3 phases)
- **Report Generation**: < 5s
- **App Launch**: < 2s
- **Offline Mode**: Full functionality

## Monitoring

### CloudWatch Metrics
- Lambda invocations
- API Gateway requests
- Error rates
- Latency (p50, p95, p99)
- DynamoDB throttles

### Alerts
- High error rate (> 5%)
- Slow API response (> 1s)
- Lambda timeouts
- DynamoDB capacity exceeded
- Cost anomalies

### Mobile Analytics
- Crash reports (Sentry)
- User sessions
- Feature usage
- Performance metrics

## Deployment

### Backend
```bash
# Using AWS SAM
sam build
sam deploy --guided

# Or using CDK
cdk deploy --all
```

### Mobile App
```bash
# Development build
expo start

# Production build (iOS)
eas build --platform ios

# Production build (Android)
eas build --platform android

# Submit to stores
eas submit --platform all
```

## Success Criteria

- ✅ Mobile app runs on iOS and Android
- ✅ Complete inspection flow works end-to-end
- ✅ Offline mode functional
- ✅ Reports generated correctly
- ✅ Multi-tenant isolation working
- ✅ Performance targets met
- ✅ Security audit passed
- ✅ Documentation complete

## Timeline

- **Week 1**: Backend infrastructure (Lambda, API Gateway, DynamoDB)
- **Week 2-3**: Mobile app development
- **Week 4**: Integration, testing, optimization
- **Total**: ~4 weeks for MVP

## Next Steps

1. ✅ Create Phase 4 folder structure
2. ✅ Setup AWS infrastructure (SAM/CDK)
3. ✅ Implement Lambda functions
4. ✅ Create API Gateway
5. ✅ Build mobile app
6. ✅ Integration testing
7. ✅ Deploy to production

---

**Status**: Ready to begin
**Dependencies**: Phase 1 ✅, Phase 2 ✅, Phase 3 ✅
**Next Action**: Create backend infrastructure

