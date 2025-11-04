# Quick Deploy to Railway.app

## 1. Push to GitHub (if not already done)
```bash
cd vericase-docs-rapid-plus-ts
git init
git add .
git commit -m "Initial commit"
gh repo create vericase-app --private --source=. --push
# Or manually create repo on github.com and:
# git remote add origin https://github.com/YOUR_USERNAME/vericase-app.git
# git push -u origin main
```

## 2. Deploy on Railway
1. Go to https://railway.app
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `vericase-app` repository
6. Railway will auto-detect and deploy

## 3. Add PostgreSQL Database
1. In your Railway project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway auto-connects it (sets DATABASE_URL)

## 4. Add Redis
1. Click "+ New" again
2. Select "Database" → "Redis"
3. Railway auto-connects it (sets REDIS_URL)

## 5. Set Environment Variables
In Railway dashboard, add these variables to your API service:

```
SECRET_KEY=<click "Generate" button>
FRONTEND_URL=https://vericase.com
MINIO_ENDPOINT=s3.amazonaws.com
MINIO_ACCESS_KEY=<your-aws-key>
MINIO_SECRET_KEY=<your-aws-secret>
S3_BUCKET=vericase-evidence
MINIO_SECURE=true
```

## 6. Get Your App URL
Railway provides a URL like: `vericase-api-production.up.railway.app`

## 7. Update Your Website
In your React website `.env`:
```bash
REACT_APP_BACKEND_URL=https://vericase-api-production.up.railway.app
REACT_APP_APP_URL=https://vericase-api-production.up.railway.app/ui/
```

## 8. Update CORS
The API will automatically allow your FRONTEND_URL domain.

## 9. Test It!
```bash
# Test API
curl https://vericase-api-production.up.railway.app/health

# Test UI
open https://vericase-api-production.up.railway.app/ui/landing.html

# Test Login
curl -X POST https://vericase-api-production.up.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"test123","full_name":"Your Name"}'
```

## 10. Update Your Website Login Button
The Login button will now redirect to your deployed app!

---

## Estimated Monthly Cost
- Railway Hobby Plan: $5/month (includes PostgreSQL + Redis)
- AWS S3 for file storage: ~$1-5/month
- **Total: ~$6-10/month**

## Custom Domain (Optional)
1. In Railway, click your service → "Settings"
2. Scroll to "Domains"
3. Click "Generate Domain" or add custom domain
4. Point `app.vericase.com` to Railway
5. Update REACT_APP_BACKEND_URL to use custom domain

---

## What Gets Deployed
✅ FastAPI backend with all endpoints
✅ PostgreSQL database
✅ Redis for task queuing
✅ All UI files (landing, index, correspondence-enterprise)
✅ PST email processing
✅ Document management
✅ Authentication system
✅ AG-Grid Enterprise correspondence view

## Next Steps After Deploy
1. Create your account via website
2. Upload a PST file
3. View emails in AG-Grid table
4. Share link with team members
