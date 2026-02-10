# Omni-Inspector AI - InsurTech & LegalTech Platform

> AI-powered forensic inspection platform for containers, vehicles, and cargo with legal-grade evidence collection.

## 🎯 Project Status

**Current Phase**: Phase 3 Complete - Nova Reasoning Layer ✅  
**Progress**: 60% (3 of 5 phases)  
**Next Action**: Test pipeline and start Phase 4

### ✅ Completed:
- **Phase 1**: Forensic Detective Layer (metadata, tampering detection) - 1,247 lines
- **Phase 2**: YOLO Detection Layer (damage detection, SageMaker) - 1,176 lines
- **Phase 3**: Nova Reasoning Layer (Bedrock, fraud detection, reports) - 1,456 lines
- **Total**: 3,879 lines of production Python code
- **Documentation**: 15+ markdown files (~20,000 words)

### 🔄 Next Phase:
- **Phase 4**: Mobile App (React Native) + Backend (Lambda, API Gateway, DynamoDB)
- **Timeline**: 4 weeks to MVP
- **Documentation**: [PHASE-4-PLAN.md](PHASE-4-PLAN.md)

---

## 📋 Quick Links

### 🇪🇸 Español
- [Resumen Ejecutivo (ES)](RESUMEN-EJECUTIVO-ES.md) - **⭐ EMPIEZA AQUÍ** - Resumen completo en español
- [Checklist Inmediato (ES)](CHECKLIST-INMEDIATO.md) - **🎯 QUÉ HACER HOY** - Acciones prioritarias

### 🇺🇸 English
- [Next Actions](NEXT-ACTIONS.md) - **🎯 WHAT TO DO NEXT** - Recommended steps
- [Progress Summary](PROGRESS-SUMMARY.md) - **⭐ START HERE** - Complete overview
- [Project Status](PROJECT-STATUS.md) - Current status and metrics
- [Test Pipeline](TEST-PIPELINE.md) - Quick testing guide
- [Executive Summary](EXECUTIVE-SUMMARY.md) - Vision, business model, roadmap
- [Project Plan](PROJECT-PLAN.md) - Technical roadmap and phases

### 📚 Phase Documentation
- [Phase 1 Complete](PHASE-1-COMPLETE.md) - Forensic Detective Layer
- [Phase 2 Complete](PHASE-2-COMPLETE.md) - YOLO Detection Layer
- [Phase 3 Complete](PHASE-3-COMPLETE.md) - Nova Reasoning Layer
- [Phase 4 Plan](PHASE-4-PLAN.md) - Mobile App & Backend (Next)

### 📖 Original Requirements
- [Project Definitions](definitions/definiciones.txt) - Original requirements

---

## 🏗️ Project Structure

```
omni-inspector-ai/
├── definitions/          # Project requirements and specifications
├── forensic-detective/   # Phase 1: Forensic validation ✅
│   ├── forensic_analyzer.py
│   ├── aws_uploader.py
│   └── cli.py
├── yolo-detection/       # Phase 2: Damage detection ✅
│   ├── yolo_detector.py
│   ├── setup_sagemaker.py
│   └── cli.py
├── nova-reasoning/       # Phase 3: AI reasoning ✅
│   ├── nova_analyzer.py
│   ├── fraud_detector.py
│   ├── report_generator.py
│   └── cli.py
├── ssh-mcp/             # SSH MCP server configuration
├── .kiro/               # Kiro IDE configuration
├── README.md            # This file
├── EXECUTIVE-SUMMARY.md # Business overview
├── PROJECT-PLAN.md      # Technical roadmap
├── PHASE-1-COMPLETE.md  # Phase 1 documentation
├── PHASE-2-COMPLETE.md  # Phase 2 documentation
└── PHASE-3-COMPLETE.md  # Phase 3 documentation
```

---

## 🚀 What We're Building

### Three Business Modules:

**🟢 Module A: Risk Underwriting**
- Pre-inspection to avoid insuring damaged goods
- AI detects pre-existing damage
- Blockchain-backed certificate

**🟡 Module B: Claims Processing**
- Fast claim settlement
- Fraud detection (recycled photos, fake metadata)
- Automatic damage estimation

**🔴 Module C: Legal Recovery**
- Evidence for lawsuits against third parties
- Container ID OCR (ISO 6346)
- Accident reconstruction for court

### Tech Stack:
- **Frontend**: React Native + Expo
- **Backend**: AWS Serverless (Kinesis, S3, Bedrock, SageMaker)
- **AI**: YOLOv11 + Amazon Nova Pro
- **Database**: DynamoDB (multi-tenant)

---

## 📦 Available Modules

### � Phase 1: Forensic Detective Layer ✅

Validates image authenticity before AI processing.

**Location:** `forensic-detective/`

**Features:**
- Metadata extraction (GPS, camera, timestamps)
- Tampering detection (ELA algorithm)
- SHA-256 hashing for integrity
- AWS S3 upload with WORM storage

**Documentation:** [PHASE-1-COMPLETE.md](PHASE-1-COMPLETE.md)

**Status:** ✅ Complete and tested

---

### 🎯 Phase 2: YOLO Detection Layer ✅

AI-powered damage detection using YOLOv11 on SageMaker.

**Location:** `yolo-detection/`

**Features:**
- 10 damage classes (dents, rust, holes, cracks, etc.)
- Severity scoring (low, medium, high, critical)
- SageMaker Serverless integration
- Batch processing support

**Documentation:** [PHASE-2-COMPLETE.md](PHASE-2-COMPLETE.md)

**Status:** ✅ Code complete, ready for deployment

---

### 🧠 Phase 3: Nova Reasoning Layer ✅

Amazon Bedrock integration for intelligent analysis and fraud detection.

**Location:** `nova-reasoning/`

**Features:**
- Multimodal analysis (Nova Lite/Pro)
- Fraud detection (recycled photos, metadata manipulation)
- Report generation (PDF + JSON)
- OCR (container IDs, seals, CSC plates)
- Three business modules (underwriting, claims, legal)

**Documentation:** [PHASE-3-COMPLETE.md](PHASE-3-COMPLETE.md)

**Status:** ✅ Complete and ready for integration

---

### 📡 SSH MCP - Remote Server Management

MCP server for executing SSH commands on remote servers using natural language.

**Location:** `ssh-mcp/`

**Documentation:**
- [README-SSH-MCP.md](ssh-mcp/README-SSH-MCP.md) - Complete guide
- [SSH-MCP-SETUP.md](ssh-mcp/SSH-MCP-SETUP.md) - Setup instructions
- [COMANDOS-UTILES.md](ssh-mcp/COMANDOS-UTILES.md) - Command examples

**Status:** ✅ Installed, ready to configure

---

## 📐 Project Rules

### Critical Rules (Auto-enforced):

1. **Each topic in its folder** - All related files in dedicated folders
2. **General docs in root** - Only project-wide docs at root level
3. **Configs in .kiro/** - Kiro settings in `.kiro/settings/`
4. **ALL SOURCE CODE IN ENGLISH** - Variables, functions, classes, comments
5. **Full Autonomy** - Agent can configure AWS, GitHub, servers, everything

See [.kiro/steering/organizacion-proyecto.md](.kiro/steering/organizacion-proyecto.md) for details.

---

## 🎬 Getting Started

### Step 1: Provide Access (REQUIRED)

Read [REQUIRED-ACCESS.md](REQUIRED-ACCESS.md) and provide:
1. AWS credentials (Access Key + Secret)
2. GitHub Personal Access Token
3. SSH server details (optional)

### Step 2: Automatic Setup

Once credentials are provided, the agent will:
- ✅ Create AWS infrastructure
- ✅ Setup GitHub repository
- ✅ Configure CI/CD pipeline
- ✅ Deploy initial environment

### Step 3: Development

- Mobile app development (React Native)
- AI model training (YOLOv11)
- Backend services (AWS Lambda)
- Integration testing

---

## 📊 Development Phases

- **Phase 1** ✅ (Complete): Forensic Detective - Metadata extraction, tampering detection
- **Phase 2** ✅ (Complete): YOLO Detection - Damage detection with SageMaker
- **Phase 3** ✅ (Complete): Nova Reasoning - Bedrock integration, fraud detection, reports
- **Phase 4** 🔄 (Next): Mobile App - React Native + Backend (Lambda, API Gateway)
- **Phase 5** (Pending): Production - Security hardening, deployment, monitoring

---

## 🔐 Security & Compliance

- S3 Object Lock (WORM) for legal evidence
- Multi-tenant architecture (DynamoDB)
- Encrypted at rest and in transit
- IAM roles with least privilege
- Audit logging (CloudTrail)

---

## 💡 Next Steps

### Phase 4: Mobile App & Backend (Current Priority)

**Mobile App (React Native + Expo):**
- [ ] Camera integration (4K capture)
- [ ] Real-time preview
- [ ] Offline mode support
- [ ] Case management UI
- [ ] Report viewing

**Backend (AWS Serverless):**
- [ ] API Gateway setup
- [ ] Lambda functions (orchestration)
- [ ] DynamoDB multi-tenant schema
- [ ] Cognito authentication
- [ ] S3 bucket policies

**Integration:**
- [ ] Connect mobile app to backend
- [ ] End-to-end testing
- [ ] Performance optimization

---

## 🚀 Quick Start

### Test the AI Pipeline

**Quick test (PowerShell):**
```powershell
# Run complete pipeline test
.\test-complete-pipeline.ps1

# Or with custom image
.\test-complete-pipeline.ps1 -TestImage "path\to\image.jpg" -Module "claims"
```

**Manual test (step by step):**
```bash
# 1. Install dependencies
cd forensic-detective && pip install -r requirements.txt
cd ../yolo-detection && pip install -r requirements.txt
cd ../nova-reasoning && pip install -r requirements.txt

# 2. Configure AWS credentials
aws configure --profile omni-inspector

# 3. Run complete analysis
cd forensic-detective
python cli.py analyze photo.jpg --output forensic.json

cd ../yolo-detection
python cli.py detect photo.jpg --output yolo.json

cd ../nova-reasoning
python cli.py analyze \
  --case-id TEST-001 \
  --forensic-report ../forensic-detective/forensic.json \
  --yolo-report ../yolo-detection/yolo.json \
  --image s3://bucket/photo.jpg \
  --module claims \
  --output analysis.json

# 4. Generate report
python cli.py report \
  --case-id TEST-001 \
  --analysis-report analysis.json \
  --module claims \
  --output final_report.pdf
```

**See [TEST-PIPELINE.md](TEST-PIPELINE.md) for detailed testing guide.**

---

## 📞 Support

For SSH MCP module, see documentation in `ssh-mcp/` folder.

For project questions, check:
- [EXECUTIVE-SUMMARY.md](EXECUTIVE-SUMMARY.md) - Business overview
- [PROJECT-PLAN.md](PROJECT-PLAN.md) - Technical details
- [definitions/](definitions/) - Original requirements
