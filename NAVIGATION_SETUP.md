# VeriCase Navigation Setup

## ✅ Completed Setup

Your VeriCase platform now has a unified navigation structure that matches your website (veri-case.com).

### 🌐 Landing Page
**URL:** http://localhost:8010/ui/landing.html

This is your main entry point with two options:
1. **File Server** → Redirects to `index.html` (existing document management)
2. **Analysis Software** → Redirects to `analysis.html` (case management interface)

### 📁 File Server
**URL:** http://localhost:8010/ui/index.html

Your existing document management system with:
- Upload/download documents
- Folder management
- User authentication
- Shared documents
- Copilot Hub integration

### 🔍 Analysis Software
**URL:** http://localhost:8010/ui/analysis.html

New case management interface with:
- Login authentication (uses same `/auth/login` API)
- Case tracking
- Evidence linking
- Issue management
- Chronology tools
- Claims analysis
- Expert reports

**Note:** Currently shows "Coming Soon - Phase 2" placeholder content. Ready for full case management API integration.

---

## 🔗 Website Integration

### Your Website (veri-case.com)
Update these buttons to point to your deployed URLs:

```html
<!-- Hero Section Buttons -->
<button onclick="window.location.href='https://your-domain.com/ui/landing.html'">
  Login to Files
</button>

<button onclick="window.location.href='https://your-domain.com/ui/landing.html'">
  Access File Server
</button>

<!-- Navigation Links -->
<a href="https://your-domain.com/ui/landing.html">Login</a>
<a href="https://your-domain.com/ui/landing.html">File Server</a>
```

### Navigation Flow
```
veri-case.com
    ↓
/ui/landing.html (Choose workspace)
    ↓
    ├── File Server (/ui/index.html)
    │   └── Document management, upload, search
    │
    └── Analysis Software (/ui/analysis.html)
        └── Case management, chronology, AI analysis
```

---

## 🚀 Next Steps

### Phase 1: Database Setup (Ready to Start)
```bash
# Initialize Alembic
docker-compose exec api alembic init alembic

# Generate migration
docker-compose exec api alembic revision --autogenerate -m "Add legal domain models"

# Apply migration
docker-compose exec api alembic upgrade head
```

### Phase 2: Case Management API (15-30 min)
Add these endpoints to `api/app/api/routes.py`:
```python
@router.post("/api/cases")
@router.get("/api/cases/{case_id}")
@router.get("/api/cases/{case_id}/evidence")
@router.get("/api/cases/{case_id}/issues")
@router.post("/api/evidence")
@router.post("/api/issues")
```

### Phase 3: Build Case Management UI (1-2 hours)
Replace placeholder content in `analysis.html` with:
- Case list/grid
- Evidence linking interface
- Issue tracker
- Chronology builder

### Phase 4: PST Email Extraction (30 min)
Implement PST processing using `readpst` command:
```python
subprocess.run(["readpst", "-S", "-o", "/tmp/pst", pst_file_path])
# Parse resulting .eml files
```

### Phase 5: Deploy to AWS
Push to your existing EKS infrastructure:
```bash
# Build and tag Docker image
docker build -t vericase-api:latest ./api

# Push to ECR
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin <ECR_URI>
docker tag vericase-api:latest <ECR_URI>/vericase-api:latest
docker push <ECR_URI>/vericase-api:latest

# Update EKS deployment
kubectl set image deployment/vericase-api vericase-api=<ECR_URI>/vericase-api:latest
```

---

## 📊 Current Status

### ✅ Completed
- [x] Three codebases merged (vericase-docs-rapid-plus-ts, vericase-integrated, VeriCase_Builder_Pack)
- [x] Database models added (Company, Case, Evidence, Issue, Claim, ChronologyItem, etc.)
- [x] Docker containers rebuilt with AI dependencies (sentence-transformers, alembic)
- [x] Landing page created with navigation to both systems
- [x] Analysis software page created with Phase 2 placeholder
- [x] Authentication integrated (both pages use same login API)

### 🔄 In Progress
- [ ] Alembic migration generation (next immediate step)
- [ ] Case management API endpoints

### 📋 Pending
- [ ] Full case management UI implementation
- [ ] PST email extraction feature
- [ ] Vector search / semantic analysis
- [ ] Schedule integration (Primavera P6 / MS Project)
- [ ] Report generation (Scott Schedules, court bundles)

---

## 🔐 Authentication

Both systems share the same authentication:
- **API Endpoint:** `POST /auth/login`
- **Token Storage:** localStorage
- **Session:** Shared between File Server and Analysis

Users can seamlessly switch between:
- File Server (document upload/management)
- Analysis Software (case management/chronology)

---

## 🎯 URLs Summary

| Page | URL | Purpose |
|------|-----|---------|
| Landing | /ui/landing.html | Choose File Server or Analysis |
| File Server | /ui/index.html | Document management (existing) |
| Analysis | /ui/analysis.html | Case management (new) |
| Copilot Hub | /ui/copilot.html | AI assistant (existing) |
| Account | /ui/account.html | User settings (existing) |
| Admin | /ui/admin.html | User management (existing) |

---

## 💡 Design Notes

### Landing Page
- Dark theme matching your website
- Clean two-card layout
- Clear distinction between File Server and Analysis
- Professional construction/legal aesthetic

### Analysis Page
- Light theme matching File Server (consistency)
- Sidebar navigation for case management sections
- Feature cards explaining capabilities
- "Coming Soon" badges for Phase 2 features
- Links back to File Server for current functionality

### Consistency
Both pages use:
- Same authentication system
- Same Inter font family
- Same color scheme principles
- Same button styles and interactions

---

## 🚀 Ready to Deploy

Your system is now:
1. ✅ Running locally at http://localhost:8010
2. ✅ Unified navigation structure in place
3. ✅ Database models ready for migration
4. ✅ AI dependencies installed (sentence-transformers)
5. ✅ Multi-tenant architecture (Company model)
6. ✅ Case management schema designed

**Next Command:**
```bash
docker-compose exec api alembic init alembic
```

This will set up the migration framework so we can create the 12 new database tables for case management.
