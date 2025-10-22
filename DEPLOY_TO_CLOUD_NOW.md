# Deploy VeriCase Docs to AWS Cloud - Quick Guide

## 🚀 Your Setup

You have:
- ✅ EKS Cluster in `eu-west-2`
- ✅ RDS PostgreSQL Database
- ✅ S3 Bucket for documents
- ✅ OpenSearch for search
- ✅ ElastiCache Redis
- ✅ ECR Repositories for images
- ✅ IRSA configured for S3 access
- ✅ Deployment scripts ready

## ⚡ Quick Deployment (5 Steps)

### Step 1: Run the Deployment Script

You have a ready-to-use script. Just run it:

```bash
# On Windows (PowerShell)
.\deploy-to-aws.ps1

# Or on Linux/Mac (if you have WSL or Git Bash)
./deploy-to-aws.sh
```

This script will:
1. Authenticate with ECR
2. Build and push API image (with all new features)
3. Build and push Worker image
4. Fetch RDS credentials from Secrets Manager
5. Update Kubernetes secrets
6. Apply ConfigMap
7. Restart deployments
8. Show pod status

### Step 2: Run Database Migration for Folders

The folder management features need a new database table. After deployment, run the migration:

```bash
# Get the API pod name
kubectl get pods -n vericase -l app=vericase-api

# Execute migration
kubectl exec -n vericase -it <api-pod-name> -- python -c "
import psycopg2
import os
from urllib.parse import urlparse

db_url = os.getenv('DATABASE_URL')
result = urlparse(db_url)
conn = psycopg2.connect(
    host=result.hostname,
    port=result.port,
    database=result.path[1:],
    user=result.username,
    password=result.password
)
cur = conn.cursor()
cur.execute(open('/app/migrations/20251020_add_folders.sql').read())
conn.commit()
print('Migration completed successfully')
"
```

Or simpler - copy the migration SQL and run it directly:

```bash
# Copy migration file to pod
kubectl cp api/migrations/20251020_add_folders.sql vericase/<api-pod-name>:/tmp/

# Execute it
kubectl exec -n vericase -it <api-pod-name> -- psql $DATABASE_URL -f /tmp/20251020_add_folders.sql
```

### Step 3: Verify Deployment

```bash
# Check pod status
kubectl get pods -n vericase

# Check API logs
kubectl logs -n vericase -l app=vericase-api --tail=50

# Check worker logs
kubectl logs -n vericase -l app=vericase-worker --tail=50

# Get load balancer URL
kubectl get svc -n vericase vericase-api
```

### Step 4: Test the Application

```bash
# Get the external load balancer URL
LOAD_BALANCER_URL=$(kubectl get svc -n vericase vericase-api -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

echo "Your application is at: http://$LOAD_BALANCER_URL/ui/index.html"

# Test the API
curl http://$LOAD_BALANCER_URL/docs
```

### Step 5: Access Your Application

Open in browser:
```
http://<load-balancer-dns>/ui/index.html
```

Example:
```
http://a1b2c3d4e5f6-123456789.eu-west-2.elb.amazonaws.com/ui/index.html
```

---

## 📋 What's Deployed

### New Features Going Live:
1. ✅ **Folder Management**
   - Create, rename, delete folders
   - Right-click context menus
   - Automatic path updates

2. ✅ **Multi-Select**
   - Ctrl+Click for individual selection
   - Shift+Click for range selection
   - Ctrl+A to select all
   - Selection count badge

3. ✅ **Drag & Drop**
   - Drag documents to folders
   - Visual drop indicators
   - Multi-document drag
   - Toast notifications

4. ✅ **Enhanced Search**
   - Live search with debouncing
   - File type icons
   - Folder path display
   - Keyboard shortcuts

5. ✅ **Visual Polish**
   - Loading states and spinners
   - File type icons (📄 📝 📊 🖼️)
   - Smooth animations
   - Toast notifications

---

## 🔧 Troubleshooting

### Pods Won't Start?

```bash
# Describe pod to see events
kubectl describe pod -n vericase <pod-name>

# Check logs for errors
kubectl logs -n vericase <pod-name>
```

### Database Connection Issues?

```bash
# Verify secret exists
kubectl get secret -n vericase vericase-db

# Check secret content
kubectl get secret -n vericase vericase-db -o yaml
```

### S3 Access Issues?

```bash
# Verify service account has IRSA annotation
kubectl describe sa -n vericase vericase-api-sa

# Should show annotation like:
# eks.amazonaws.com/role-arn: arn:aws:iam::526015377510:role/vericase-s3-access
```

### Migration Failed?

You can run the migration manually from your local machine:

```bash
# Using psql locally
export DB_HOST="database-1.cv8uw0uuqr7f.eu-west-2.rds.amazonaws.com"
export DB_USER="<username-from-secrets-manager>"
export DB_PASS="<password-from-secrets-manager>"
export DB_NAME="vericase"

psql "postgresql://$DB_USER:$DB_PASS@$DB_HOST:5432/$DB_NAME" -f api/migrations/20251020_add_folders.sql
```

---

## 🌐 DNS Setup (Optional but Recommended)

### Option 1: Route 53 with Custom Domain

```bash
# Get load balancer hostname
LB_HOSTNAME=$(kubectl get svc -n vericase vericase-api -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

echo "Create a CNAME record:"
echo "docs.yourdomain.com -> $LB_HOSTNAME"
```

Then access via: `https://docs.yourdomain.com/ui/index.html`

### Option 2: Use AWS Load Balancer DNS Directly

The load balancer DNS works immediately - no setup needed!

---

## 📊 Post-Deployment Checklist

After deployment, verify:

- [ ] API pods are running (3 replicas)
- [ ] Worker pods are running (2 replicas)
- [ ] Load balancer has external IP/hostname
- [ ] Can access `/docs` endpoint (FastAPI docs)
- [ ] Can load `/ui/index.html` in browser
- [ ] Can sign up / log in
- [ ] Can create folders
- [ ] Can upload documents
- [ ] Can search documents
- [ ] Can drag & drop to move documents
- [ ] Multi-select works (Ctrl+Click, Shift+Click)
- [ ] All file type icons display correctly

---

## 🔐 Security Considerations

Before going to production:

1. **Change JWT Secret**
   ```yaml
   JWT_SECRET: "generate-a-strong-random-secret-here"
   ```

2. **Enable HTTPS**
   - Set up AWS Certificate Manager certificate
   - Configure ALB with HTTPS listener
   - Redirect HTTP to HTTPS

3. **Restrict CORS**
   ```yaml
   CORS_ORIGINS: "https://docs.yourdomain.com"
   ```

4. **Set up WAF**
   - Protect against DDoS
   - Rate limiting
   - SQL injection protection

5. **Enable CloudWatch Logs**
   - Monitor application logs
   - Set up alerts for errors

---

## 💰 Cost Optimization

Your AWS setup includes:
- **RDS PostgreSQL** - ~$50-200/month (depending on instance size)
- **ElastiCache Redis** - ~$20-100/month
- **OpenSearch** - ~$50-200/month
- **S3 Storage** - ~$0.023/GB/month
- **ALB Load Balancer** - ~$20/month
- **EKS Cluster** - ~$73/month + worker nodes
- **Data Transfer** - Variable based on usage

**Total estimated: ~$250-600/month** for a small production deployment

### Cost Saving Tips:
- Use smaller RDS instance for dev/staging
- Use single-AZ instead of multi-AZ for non-critical environments
- Set up S3 lifecycle policies to move old documents to Glacier
- Use spot instances for worker nodes
- Enable autoscaling based on load

---

## 📈 Scaling for Production

### Horizontal Scaling
```yaml
# Increase replicas as needed
kubectl scale deployment/vericase-api --replicas=5 -n vericase
kubectl scale deployment/vericase-worker --replicas=4 -n vericase
```

### Auto-scaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vericase-api-hpa
  namespace: vericase
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vericase-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## 🎯 Quick Deploy Command

If you just want to deploy NOW with one command:

```bash
# Deploy everything
./deploy-to-aws.sh

# Then run migration (replace <pod-name> with actual pod name from kubectl get pods)
kubectl cp api/migrations/20251020_add_folders.sql vericase/<pod-name>:/tmp/migration.sql -n vericase
kubectl exec -n vericase -it <pod-name> -- psql $DATABASE_URL -f /tmp/migration.sql

# Get your URL
kubectl get svc -n vericase vericase-api
```

---

## ✨ You're Ready!

Your VeriCase Docs application with all new features will be live in AWS with enterprise-grade:
- Folder management
- Multi-select
- Drag & drop
- Enhanced search
- Professional UI polish

**Just run `./deploy-to-aws.sh` and you're live!** 🚀
