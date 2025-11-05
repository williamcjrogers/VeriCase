# VeriCase Deployment Quick Reference

## 🚀 Quick Access to All Deployments

### 📋 Repository Overview
| Repository | Purpose | GitHub URL | Status |
|------------|---------|------------|--------|
| **VeriCase** | Main Backend/API | https://github.com/williamcjrogers/VeriCase.git | ✅ Production |
| **VeriCaseWR** | Desktop Application | https://github.com/williamcjrogers/VeriCaseWR.git | ✅ Production |
| **VeriCase-Website-New** | Frontend Website | https://github.com/williamcjrogers/VeriCase-Website-New.git | ⚠️ Development |

---

## 🎯 One-Click Deployment Commands

### Main Repository (VeriCase)
```bash
# AWS EKS Production
./deploy-to-aws.sh

# Railway.app Staging
git add . && git commit -m "Deploy" && git push origin main

# Local Development
docker-compose up -d
```

### Desktop Repository (VeriCaseWR)
```bash
# Navigate and build
cd "VeriCase-DESKTOP-46BMPM4"
# Build using your preferred method
```

### Website Repository (VeriCase-Website-New)
```bash
# Development Server
cd frontend && npm install && npm start

# Production Build
cd frontend && npm run build

# Deploy to Vercel
npm i -g vercel && vercel --prod
```

---

## 🛠️ Deployment Scripts

### Interactive Menu (Recommended)
```bash
# Linux/Mac
./deploy-by-github.sh

# Windows
deploy-by-github.bat
```

### Individual Scripts
- `deploy-to-aws.sh` - AWS EKS deployment
- `deploy-to-aws.ps1` - PowerShell version for AWS
- `docker-compose.yml` - Local development

---

## 📊 Current Status

### 🟢 Production (Live)
- **AWS EKS:** 5 pods running (3 API + 2 Workers)
- **Desktop App:** Windows installer available
- **Infrastructure:** RDS, ElastiCache, OpenSearch, S3

### 🟡 Staging (Ready)
- **Railway.app:** Configured, ready for deploy
- **React Website:** Development server active

### 🔵 Development (Active)
- **Docker Compose:** Local environment ready
- **All Repositories:** Git synced and ready

---

## 🔗 Key URLs & Endpoints

### Production
- **AWS Load Balancer:** (Check AWS console for URL)
- **ECR Registry:** `526015377510.dkr.ecr.eu-west-2.amazonaws.com`

### Staging
- **Railway.app:** `https://vericase-api-production.up.railway.app`
- **Railway Dashboard:** https://railway.app

### Development
- **Local API:** `http://localhost:8010`
- **Local UI:** `http://localhost:3000` (React)

---

## 💰 Cost Summary

| Service | Monthly Cost | Environment |
|---------|--------------|-------------|
| AWS EKS | $200-500 | Production |
| Railway.app | $6-10 | Staging |
| Desktop App | One-time | Production |
| Website Hosting | $10-50 | Future |

---

## 📁 Important Files by Repository

### VeriCase (Main)
```
vericase-docs-rapid-plus-ts/
├── deploy-to-aws.sh          # AWS deployment
├── deploy-to-aws.ps1         # PowerShell AWS deploy
├── railway.json               # Railway config
├── vericase-k8s.yaml          # Kubernetes config
├── docker-compose.yml         # Local dev
├── Dockerfile                 # Container build
└── RAILWAY_DEPLOYMENT_GUIDE.md # Railway instructions
```

### VeriCaseWR (Desktop)
```
VeriCase-DESKTOP-46BMPM4/
└── vericase-hotfix-pack.zip   # Current release
```

### VeriCase-Website-New (Frontend)
```
VeriCase-Website-New/
├── frontend/
│   ├── src/
│   │   ├── pages/Login.jsx
│   │   ├── context/AuthContext.jsx
│   │   └── App.js
│   └── .env.development       # Dev config
```

---

## 🚨 Quick Troubleshooting

### AWS Deployment Issues
```bash
# Check EKS status
kubectl get pods -n vericase

# Check logs
kubectl logs -f deployment/vericase-api

# Restart deployment
kubectl rollout restart deployment/vericase-api
```

### Railway Issues
- Check Railway dashboard for build logs
- Verify `railway.json` configuration
- Ensure GitHub webhook is active

### Local Development Issues
```bash
# Reset Docker environment
docker-compose down -v
docker-compose up -d --build

# Check logs
docker-compose logs -f api
```

---

## 📞 Support & Documentation

### Documentation Files
- `GITHUB_DEPLOYMENTS_SUMMARY.md` - Complete overview
- `AWS_DEPLOYMENT_GUIDE.md` - AWS specific guide
- `RAILWAY_DEPLOYMENT_GUIDE.md` - Railway specific guide
- `DEPLOYMENT_GUIDE.md` - General deployment guide

### Quick Commands Reference
```bash
# Check all repository status
git status

# Pull latest changes
git pull origin main

# Push changes (triggers Railway deploy)
git add . && git commit -m "Update" && git push origin main

# Run deployment menu
./deploy-by-github.sh  # or deploy-by-github.bat on Windows
```

---

## 🔄 Next Steps

### Immediate
1. ✅ Review deployment summary
2. ✅ Run deployment menu script
3. ⏳ Deploy to Railway for staging
4. ⏳ Set up CI/CD pipelines

### This Week
1. Deploy React website to production
2. Set up monitoring and alerts
3. Create backup strategies
4. Test all deployment targets

### This Month
1. Optimize costs based on usage
2. Implement auto-scaling
3. Set up multi-region deployment
4. Create disaster recovery procedures

---

*Last Updated: November 5, 2025*  
*For detailed information, see GITHUB_DEPLOYMENTS_SUMMARY.md*
