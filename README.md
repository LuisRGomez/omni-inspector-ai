# Omni-Inspector AI - InsurTech & LegalTech Platform

> AI-powered forensic inspection platform for containers, vehicles, and cargo with legal-grade evidence collection.

## 🎯 Project Status

**Current Phase**: AWS Configuration in Progress
**Priority**: HIGH
**Next Action**: Awaiting GitHub token

### ✅ Completed:
- AWS credentials configured
- Project structure created
- Technical analysis completed

### 🔄 In Progress:
- Waiting for GitHub token

---

## 📋 Quick Links

- [Executive Summary](EXECUTIVE-SUMMARY.md) - Vision, business model, roadmap
- [Project Plan](PROJECT-PLAN.md) - Technical roadmap and phases
- [Required Access](REQUIRED-ACCESS.md) - **⚠️ READ THIS FIRST** - Credentials needed
- [Project Definitions](definitions/definiciones.txt) - Original requirements

---

## 🏗️ Project Structure

```
omni-inspector-ai/
├── definitions/          # Project requirements and specifications
├── ssh-mcp/             # SSH MCP server configuration and tools
├── .kiro/               # Kiro IDE configuration
│   ├── settings/
│   │   └── mcp.json     # MCP servers configuration
│   └── steering/
│       └── organizacion-proyecto.md  # Project organization rules
├── README.md            # This file
├── EXECUTIVE-SUMMARY.md # Business overview
├── PROJECT-PLAN.md      # Technical roadmap
└── REQUIRED-ACCESS.md   # Credentials checklist
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

- **Phase 1** (Week 1-2): Foundation - AWS setup, basic app
- **Phase 2** (Week 3-6): Core features - Video streaming, damage detection
- **Phase 3** (Week 7-10): AI integration - Bedrock, fraud detection
- **Phase 4** (Week 11-14): Business logic - All three modules
- **Phase 5** (Week 15-16): Production - Security, deployment

---

## 🔐 Security & Compliance

- S3 Object Lock (WORM) for legal evidence
- Multi-tenant architecture (DynamoDB)
- Encrypted at rest and in transit
- IAM roles with least privilege
- Audit logging (CloudTrail)

---

## 💡 Next Steps

1. **NOW**: Read [REQUIRED-ACCESS.md](REQUIRED-ACCESS.md)
2. **NOW**: Provide AWS + GitHub credentials
3. **THEN**: Agent begins automatic setup
4. **THEN**: First MVP in 2 weeks

---

## 📞 Support

For SSH MCP module, see documentation in `ssh-mcp/` folder.

For project questions, check:
- [EXECUTIVE-SUMMARY.md](EXECUTIVE-SUMMARY.md) - Business overview
- [PROJECT-PLAN.md](PROJECT-PLAN.md) - Technical details
- [definitions/](definitions/) - Original requirements
