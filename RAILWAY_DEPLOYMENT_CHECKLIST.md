# Railway Deployment Checklist - Port 8010

## ✅ Pre-Deployment Complete
- [x] Updated railway.json to use port 8010
- [x] Modified Dockerfile to expose port 8010
- [x] Updated start.py default port to 8010
- [x] Updated .env.example API_PORT to 8010
- [x] Created comprehensive deployment guide
- [x] Committed and pushed changes to GitHub

## 🚀 Deployment Steps

### 1. Railway Setup
- [ ] Go to https://railway.app
- [ ] Sign up/Login with GitHub
- [ ] Click "New Project"
- [ ] Select "Deploy from GitHub repo"
- [ ] Choose your `VeriCase` repository
- [ ] Wait for Railway to build and deploy

### 2. Add Services
- [ ] Add PostgreSQL database (+ New → Database → PostgreSQL)
- [ ] Add Redis database (+ New → Database → Redis)
- [ ] Wait for both services to be ready

### 3. Environment Variables
In Railway dashboard, add these to your API service:

#### Required
- [ ] SECRET_KEY (click "Generate" button)
- [ ] FRONTEND_URL (your domain or Railway URL)
- [ ] DATABASE_URL (auto-set by Railway)
- [ ] REDIS_URL (auto-set by Railway)

#### Storage (AWS S3)
- [ ] MINIO_ENDPOINT=s3.amazonaws.com
- [ ] MINIO_ACCESS_KEY=your-aws-access-key
- [ ] MINIO_SECRET_KEY=your-aws-secret-key
- [ ] MINIO_BUCKET=vericase-evidence
- [ ] MINIO_SECURE=true

#### Security
- [ ] JWT_SECRET=generate-strong-secret
- [ ] JWT_ISSUER=vericase-docs
- [ ] JWT_EXPIRE_MIN=7200

#### AI Features (Optional)
- [ ] GEMINI_API_KEY=your-gemini-api-key
- [ ] CLAUDE_API_KEY=your-claude-api-key
- [ ] OPENAI_API_KEY=your-openai-api-key
- [ ] ENABLE_AI_AUTO_CLASSIFY=true
- [ ] ENABLE_AI_DATASET_INSIGHTS=true
- [ ] AI_DEFAULT_MODEL=gemini

### 4. Test Deployment
- [ ] Check build logs in Railway dashboard
- [ ] Test health endpoint: `curl https://your-app.railway.app/health`
- [ ] Test UI: `https://your-app.railway.app/ui/landing.html`
- [ ] Test registration via API or UI

### 5. Database Setup
- [ ] Open Railway console for your service
- [ ] Run: `python railway_db_fix.py`
- [ ] Verify database migrations completed

### 6. Final Configuration
- [ ] Update frontend React app with Railway URL
- [ ] Set up custom domain (optional)
- [ ] Configure monitoring and alerts

## 🔍 Post-Deployment Tests

### API Tests
```bash
# Health check
curl https://your-app.railway.app/health

# Registration
curl -X POST https://your-app.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","full_name":"Test User"}'

# Login
curl -X POST https://your-app.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

### UI Tests
- [ ] Landing page loads: `/ui/landing.html`
- [ ] Login works: `/ui/index.html`
- [ ] Dashboard accessible: `/ui/dashboard.html`
- [ ] File upload works
- [ ] PST processing works

### Feature Tests
- [ ] User registration and login
- [ ] Case creation
- [ ] File upload and processing
- [ ] Search functionality
- [ ] Sharing features
- [ ] AI features (if configured)

## 📊 Monitoring
- [ ] Check Railway logs regularly
- [ ] Monitor database usage
- [ ] Track file storage costs
- [ ] Set up error alerts

## 💰 Cost Management
- [ ] Railway Hobby Plan: $5/month
- [ ] AWS S3: ~$1-5/month
- [ ] Monitor usage to control costs

## 🆘 Troubleshooting

### Common Issues
1. **Build fails**: Check Dockerfile and requirements.txt
2. **Database errors**: Verify DATABASE_URL and run migrations
3. **Port issues**: Ensure port 8010 is configured correctly
4. **File upload fails**: Check S3 credentials and permissions
5. **AI features not working**: Verify API keys and enable flags

### Debug Commands
```bash
# Check logs in Railway dashboard
# Open console to run commands
python railway_db_fix.py

# Test database connection
python -c "from app.db import engine; print(engine.url)"
```

## 📞 Support
- Railway documentation: https://docs.railway.app
- GitHub issues: https://github.com/williamcjrogers/VeriCase/issues
- Deployment guide: `RAILWAY_DEPLOYMENT_GUIDE.md`

---

## 🎉 Success Criteria
Your deployment is successful when:
- [ ] Application builds and deploys without errors
- [ ] Health endpoint returns 200 OK
- [ ] UI pages load correctly
- [ ] User registration and login work
- [ ] File upload and processing work
- [ ] Database migrations completed successfully

**Estimated deployment time: 15-30 minutes**
