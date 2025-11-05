# Railway Deployment Guide - Port 8010

## Overview
This guide will help you deploy the VeriCase application to Railway.app running on port 8010.

## Prerequisites
- Railway.app account
- GitHub account
- AWS S3 bucket (for file storage)
- Domain name (optional)

## Step 1: Push to GitHub

```bash
cd vericase-docs-rapid-plus-ts
git add .
git commit -m "Configure for Railway deployment on port 8010"
git push origin main
```

## Step 2: Deploy on Railway

1. Go to https://railway.app
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `VeriCase` repository
6. Railway will auto-detect the Dockerfile and deploy

## Step 3: Add PostgreSQL Database

1. In your Railway project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway auto-connects it (sets DATABASE_URL)
4. Note the database URL for reference

## Step 4: Add Redis

1. Click "+ New" again
2. Select "Database" → "Redis"
3. Railway auto-connects it (sets REDIS_URL)

## Step 5: Configure Environment Variables

In Railway dashboard, add these variables to your API service:

### Required Variables
```
SECRET_KEY=<click "Generate" button>
FRONTEND_URL=https://your-domain.com
DATABASE_URL=<auto-set-by-railway>
REDIS_URL=<auto-set-by-railway>
```

### Storage Configuration (AWS S3)
```
MINIO_ENDPOINT=s3.amazonaws.com
MINIO_ACCESS_KEY=<your-aws-access-key>
MINIO_SECRET_KEY=<your-aws-secret-key>
MINIO_BUCKET=vericase-evidence
MINIO_SECURE=true
```

### AI Configuration (Optional)
```
GEMINI_API_KEY=your-gemini-api-key
CLAUDE_API_KEY=your-claude-api-key
OPENAI_API_KEY=your-openai-api-key
ENABLE_AI_AUTO_CLASSIFY=true
ENABLE_AI_DATASET_INSIGHTS=true
AI_DEFAULT_MODEL=gemini
```

### Security
```
JWT_SECRET=<generate-strong-secret>
JWT_ISSUER=vericase-docs
JWT_EXPIRE_MIN=7200
```

## Step 6: Port Configuration

The application is configured to run on port 8010:
- `railway.json` specifies port 8010
- `Dockerfile` exposes port 8010
- `start.py` defaults to port 8010

Railway will automatically handle the port mapping and provide a URL like:
`https://vericase-api-production.up.railway.app`

## Step 7: Test the Deployment

### Test API Health
```bash
curl https://vericase-api-production.up.railway.app/health
```

### Test UI Access
```bash
# Open in browser
open https://vericase-api-production.up.railway.app/ui/landing.html
```

### Test Registration
```bash
curl -X POST https://vericase-api-production.up.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"test123","full_name":"Your Name"}'
```

## Step 8: Database Setup

Run the database fix script to set up initial data:

```bash
# In Railway console, run:
python railway_db_fix.py
```

Or access via Railway console:
1. Go to your service → "Console"
2. Run: `python railway_db_fix.py`

## Step 9: Update Frontend Configuration

In your React website `.env`:
```bash
REACT_APP_BACKEND_URL=https://vericase-api-production.up.railway.app
REACT_APP_APP_URL=https://vericase-api-production.up.railway.app/ui/
```

## Step 10: Custom Domain (Optional)

1. In Railway, click your service → "Settings"
2. Scroll to "Domains"
3. Click "Generate Domain" or add custom domain
4. Point DNS to Railway
5. Update frontend configuration with new domain

## Troubleshooting

### Port Issues
- The app is configured for port 8010
- Railway automatically handles external port mapping
- Internal container runs on 8010, Railway exposes it on 443/80

### Database Connection
- Ensure DATABASE_URL is set correctly
- Check PostgreSQL service is running
- Run migrations if needed

### File Storage
- Verify AWS S3 credentials
- Check bucket permissions
- Ensure MINIO_SECURE=true for AWS S3

### Build Issues
- Check Dockerfile syntax
- Verify all dependencies in requirements.txt
- Review build logs in Railway dashboard

## Cost Estimate

- Railway Hobby Plan: $5/month (includes PostgreSQL + Redis)
- AWS S3 storage: ~$1-5/month
- **Total: ~$6-10/month**

## Features Deployed

✅ FastAPI backend on port 8010
✅ PostgreSQL database with migrations
✅ Redis for task queuing
✅ All UI files (landing, dashboard, correspondence)
✅ PST email processing
✅ Document management with folders
✅ Authentication and user management
✅ AI-powered features (if configured)
✅ File sharing and collaboration
✅ Search and filtering
✅ Version control

## Monitoring

Monitor your deployment via:
- Railway dashboard logs
- Health endpoint: `/health`
- Database metrics in Railway
- Error tracking in logs

## Next Steps

1. Create admin account via registration
2. Set up AI API keys for enhanced features
3. Configure custom domain
4. Set up monitoring and alerts
5. Test all features thoroughly
