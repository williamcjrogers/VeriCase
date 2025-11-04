# VeriCase Cloud Deployment Guide

## Quick Overview
Deploy VeriCase online so users can access it from your website's Login button.

## Architecture
```
Your Website (React) → Cloud API (FastAPI) → PostgreSQL + MinIO + Redis
                     ↓
              VeriCase App UI (index.html, correspondence-enterprise.html)
```

## Option 1: AWS Deployment (Recommended)

### Prerequisites
- AWS Account
- Domain name (e.g., app.vericase.com)
- AWS CLI installed

### Step 1: Set Up Database (RDS PostgreSQL)
```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier vericase-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username vericase \
  --master-user-password <STRONG_PASSWORD> \
  --allocated-storage 20 \
  --publicly-accessible
```

### Step 2: Set Up Object Storage (S3)
```bash
# Create S3 bucket
aws s3 mb s3://vericase-evidence

# Set CORS policy
aws s3api put-bucket-cors --bucket vericase-evidence --cors-configuration file://s3-cors.json
```

### Step 3: Deploy API (ECS Fargate)
```bash
# Build and push Docker image
aws ecr create-repository --repository-name vericase-api
docker build -t vericase-api ./api
docker tag vericase-api:latest <YOUR_AWS_ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/vericase-api:latest
docker push <YOUR_AWS_ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/vericase-api:latest

# Create ECS cluster
aws ecs create-cluster --cluster-name vericase-cluster

# Deploy service (see ecs-task-definition.json)
```

### Step 4: Set Up Domain & SSL
```bash
# Get SSL certificate
aws acm request-certificate --domain-name app.vericase.com

# Create ALB and point to ECS service
# Update Route53 to point app.vericase.com to ALB
```

## Option 2: Railway.app Deployment (Easiest)

### Prerequisites
- Railway.app account (free tier available)
- GitHub repository

### Step 1: Push Code to GitHub
```bash
cd vericase-docs-rapid-plus-ts
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/vericase.git
git push -u origin main
```

### Step 2: Deploy on Railway
1. Go to railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway will:
   - Auto-detect docker-compose.yml
   - Create PostgreSQL database
   - Deploy API container
   - Provide a public URL (e.g., vericase-api.up.railway.app)

### Step 3: Add Environment Variables
In Railway dashboard, set:
```
DATABASE_URL=postgresql://...  (auto-populated)
MINIO_ENDPOINT=s3.amazonaws.com (or Railway S3 addon)
MINIO_ACCESS_KEY=...
MINIO_SECRET_KEY=...
SECRET_KEY=<generate-random-string>
FRONTEND_URL=https://vericase.com
```

## Option 3: DigitalOcean App Platform

### Prerequisites
- DigitalOcean account
- GitHub repository

### Step 1: Create App
1. Go to DigitalOcean dashboard
2. Click "Create" → "App"
3. Connect GitHub repository
4. Select branch

### Step 2: Configure Components
```yaml
# .do/app.yaml
name: vericase
services:
  - name: api
    dockerfile_path: api/Dockerfile
    instance_count: 1
    instance_size_slug: basic-xxs
    http_port: 8000
    routes:
      - path: /
    envs:
      - key: DATABASE_URL
        scope: RUN_TIME
        value: ${db.DATABASE_URL}

databases:
  - name: db
    engine: PG
    version: "14"
```

## Connecting Your Website to Deployed App

### Update Frontend Environment Variables
In your website's `.env`:
```bash
REACT_APP_BACKEND_URL=https://app.vericase.com
REACT_APP_APP_URL=https://app.vericase.com/ui/
```

### Update Navigation.jsx
The Login button should redirect to the deployed app:
```jsx
onClick={() => {
  if (user) {
    // If logged in, go straight to app
    window.location.href = `${process.env.REACT_APP_APP_URL}index.html`;
  } else {
    // If not logged in, go to login page
    navigate('/login');
  }
}}
```

### Update CORS in API
Allow your website domain:
```python
origins = [
    "https://vericase.com",
    "https://www.vericase.com",
    "http://localhost:3000",  # for local development
]
```

## Post-Deployment Checklist

- [ ] API is accessible at public URL
- [ ] Database is running and migrations applied
- [ ] UI files are served correctly
- [ ] Authentication works (signup/login)
- [ ] CORS allows your website domain
- [ ] SSL certificate is active
- [ ] Email correspondence page loads with AG-Grid
- [ ] PST file processing works
- [ ] File uploads work with S3/MinIO

## Testing

### Test Authentication
```bash
# Signup
curl -X POST https://app.vericase.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"secure123"}'

# Login
curl -X POST https://app.vericase.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"secure123"}'
```

### Test UI
Visit: `https://app.vericase.com/ui/correspondence-enterprise.html`

## Cost Estimates

### AWS (Monthly)
- RDS t3.micro: $15
- ECS Fargate: $15
- S3: $5
- Total: ~$35/month

### Railway.app
- Hobby Plan: $5/month
- Database: Included
- Total: ~$5/month

### DigitalOcean
- Basic Droplet: $6/month
- Managed Database: $15/month
- Total: ~$21/month

## Support

For deployment issues:
- Check API logs: `docker logs <container-id>`
- Check database connection
- Verify environment variables
- Test CORS settings
