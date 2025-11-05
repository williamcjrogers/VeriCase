# VeriCase Deployments Organized by GitHub Repository

## Overview
This document organizes all VeriCase deployments by their respective GitHub repositories, providing a clear overview of deployment targets, configurations, and status.

---

## 🚀 Repository 1: `VeriCase` (Main Backend/API)
**GitHub URL:** https://github.com/williamcjrogers/VeriCase.git  
**Local Path:** `c:\Users\William\Documents\Projects\vericase-docs-rapid-plus-ts`  
**Primary Purpose:** Main API backend, document processing, and core functionality

### Deployment Targets

#### 🟢 Production: AWS EKS (Primary)
- **Type:** Kubernetes (EKS)
- **Region:** eu-west-2
- **Account ID:** 526015377510
- **Status:** ✅ Active
- **Configuration Files:**
  - `vericase-k8s.yaml` - Main Kubernetes deployment
  - `kubernetes-configmap-aws.yaml` - AWS configuration
  - `deploy-to-aws.sh` - Deployment script
- **Services:**
  - API: `526015377510.dkr.ecr.eu-west-2.amazonaws.com/vericase-api:latest`
  - Worker: `526015377510.dkr.ecr.eu-west-2.amazonaws.com/vericase-worker:latest`
- **Infrastructure:**
  - EKS Cluster with 3 API replicas + 2 Worker replicas
  - RDS PostgreSQL database
  - ElastiCache Redis
  - OpenSearch cluster
  - S3 bucket: `vericase-docs-prod-526015377510`

#### 🟡 Staging: Railway.app
- **Type:** Container Platform
- **Port:** 8010
- **Status:** ⚠️ Configured (Ready for deployment)
- **Configuration Files:**
  - `railway.json` - Railway configuration
  - `RAILWAY_DEPLOYMENT_GUIDE.md` - Deployment instructions
- **Features:**
  - Auto-deploy from GitHub
  - PostgreSQL + Redis included
  - Cost: ~$6-10/month

#### 🔵 Development: Docker Compose
- **Type:** Local Development
- **Status:** ✅ Active
- **Configuration Files:**
  - `docker-compose.yml` - Local development setup
  - `Dockerfile` - Main application container
  - `api/Dockerfile` - API specific container
  - `worker/Dockerfile` - Worker specific container

### Key Features Deployed
- ✅ FastAPI backend with full REST API
- ✅ Document management with folders
- ✅ PST email processing
- ✅ AI-powered classification and insights
- ✅ User authentication and management
- ✅ File sharing and collaboration
- ✅ Search and filtering
- ✅ Version control
- ✅ Watermarking
- ✅ Correspondence management

---

## 🖥️ Repository 2: `VeriCaseWR` (Desktop Application)
**GitHub URL:** https://github.com/williamcjrogers/VeriCaseWR.git  
**Local Path:** `c:\Users\William\OneDrive - Vericase LTD\Software\VeriCase\Vericase-DESKTOP-46BMPM4`  
**Primary Purpose:** Windows desktop application

### Deployment Targets

#### 🟢 Production: Windows Installer
- **Type:** Desktop Application
- **Status:** ✅ Active
- **Package:** `vericase-hotfix-pack.zip`
- **Target:** Windows desktop environments
- **Distribution:** Direct download/enterprise deployment

### Key Features
- ✅ Desktop interface for VeriCase
- ✅ Local file integration
- ✅ Hotfix packages available
- ✅ Enterprise deployment ready

---

## 🌐 Repository 3: `VeriCase-Website-New` (Frontend Website)
**GitHub URL:** https://github.com/williamcjrogers/VeriCase-Website-New.git  
**Local Path:** `c:\Users\William\OneDrive - Vericase LTD\Documents\website\Latest\VeriCase-Website-NewV1\VeriCase-Website-New`  
**Primary Purpose:** React frontend website

### Deployment Targets

#### 🟡 Staging: Development Server
- **Type:** React Development
- **Status:** ⚠️ In Development
- **Technology:** React.js
- **Configuration:** `.env.development`
- **Key Components:**
  - `frontend/src/pages/Login.jsx`
  - `frontend/src/context/AuthContext.jsx`
  - `frontend/src/App.js`
  - `frontend/src/components/sections/Navigation.jsx`

#### 🟢 Production: (Planned)
- **Type:** Static Hosting (Vercel/Netlify/AWS S3)
- **Status:** 🔄 Planning Phase
- **Backend Integration:** Will connect to Railway/AWS API

### Key Features
- ✅ Modern React interface
- ✅ Authentication context
- ✅ Responsive navigation
- ✅ Login system
- ✅ Integration ready for API backend

---

## 📊 Deployment Summary Matrix

| Repository | Primary Target | Status | Cost | Technology |
|------------|----------------|--------|------|------------|
| `VeriCase` | AWS EKS | ✅ Production | $$ | Kubernetes/FastAPI |
| `VeriCase` | Railway.app | ⚠️ Staging | $ | Docker/FastAPI |
| `VeriCaseWR` | Windows Desktop | ✅ Production | $ | .NET/Desktop |
| `VeriCase-Website-New` | Development | ⚠️ In Dev | $ | React.js |

---

## 🔗 Integration Points

### API Endpoints (Main Repository)
- **Production AWS:** Load balancer endpoint
- **Staging Railway:** `https://vericase-api-production.up.railway.app`
- **Local:** `http://localhost:8010`

### Frontend Connections
- **Website Repo** → **API Repo** via REST API
- **Desktop App** → **API Repo** via REST API
- **Mobile (Future)** → **API Repo** via REST API

### Data Flow
```
Frontend (React) → API (FastAPI) → Database (PostgreSQL)
                    ↓
                 Workers (Celery) → Storage (S3)
                    ↓
                 Search (OpenSearch)
```

---

## 🚦 Deployment Status by Environment

### 🟢 Production (Live)
- **AWS EKS Cluster:** Running with 5 pods total
- **Database:** RDS PostgreSQL active
- **Storage:** S3 bucket configured
- **Search:** OpenSearch cluster active
- **Desktop App:** Installer available

### 🟡 Staging (Ready)
- **Railway.app:** Configured, ready for deploy
- **React Website:** Development server active

### 🔵 Development (Active)
- **Docker Compose:** Local development ready
- **Git Repositories:** All synced and ready

---

## 🛠️ Deployment Scripts & Automation

### AWS Deployment
```bash
# Main deployment script
./deploy-to-aws.sh

# PowerShell alternative
./deploy-to-aws.ps1
```

### Railway Deployment
```bash
# Push to trigger auto-deploy
git push origin main
```

### Local Development
```bash
# Start all services
docker-compose up -d
```

---

## 💰 Cost Analysis

### Monthly Costs
- **AWS EKS:** ~$200-500/month (production)
- **Railway:** ~$6-10/month (staging)
- **Desktop App:** One-time development cost
- **Website Hosting:** ~$10-50/month (when deployed)

### Cost Optimization Opportunities
1. Use Railway for smaller deployments
2. Implement auto-scaling on AWS
3. Use reserved instances for predictable workloads
4. Optimize S3 storage with lifecycle policies

---

## 🔄 CI/CD Pipeline Status

### Repository: `VeriCase`
- **GitHub Actions:** ⚠️ Not configured
- **Auto-deploy:** ✅ Railway ready
- **Manual deploy:** ✅ AWS script ready

### Repository: `VeriCaseWR`
- **Build pipeline:** ⚠️ Manual builds only
- **Release management:** ⚠️ Manual zip creation

### Repository: `VeriCase-Website-New`
- **GitHub Actions:** ⚠️ Not configured
- **Auto-deploy:** 🔄 Planning phase

---

## 📋 Next Steps & Recommendations

### Immediate Actions
1. **Set up GitHub Actions** for all repositories
2. **Deploy to Railway** for staging environment
3. **Configure CI/CD** for automated testing
4. **Deploy React website** to production hosting

### Medium Term
1. **Implement monitoring** across all deployments
2. **Set up backup strategies** for databases
3. **Create disaster recovery** procedures
4. **Optimize costs** based on usage patterns

### Long Term
1. **Multi-region deployment** for high availability
2. **Edge computing** for better performance
3. **Advanced monitoring** and alerting
4. **Automated scaling** based on demand

---

## 📞 Contact & Support

**Repository Owner:** williamcjrogers  
**Primary Contact:** William Rogers  
**Last Updated:** November 5, 2025

---

*This document provides a comprehensive overview of all VeriCase deployments organized by GitHub repository. For detailed deployment instructions, refer to the specific deployment guides in each repository.*
