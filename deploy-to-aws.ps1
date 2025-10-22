# VeriCase AWS Deployment Script (PowerShell)
# This script rebuilds Docker images and deploys to your EKS cluster

Write-Host "=== VeriCase AWS Deployment Script ===" -ForegroundColor Green
Write-Host ""

# Configuration
$AWS_ACCOUNT_ID = "526015377510"
$AWS_REGION = "eu-west-2"
# PSScriptAnalyzer incorrectly flags these as unused - they're used in docker commands below
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseDeclaredVarsMoreThanAssignments', '')]
$ECR_API_REPO = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/vericase-api"
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseDeclaredVarsMoreThanAssignments', '')]
$ECR_WORKER_REPO = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/vericase-worker"

# Step 1: Authenticate with ECR
Write-Host "Step 1: Authenticating with ECR..." -ForegroundColor Cyan
$ecrPassword = aws ecr get-login-password --region $AWS_REGION
$ecrPassword | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
Write-Host "✓ ECR authentication successful" -ForegroundColor Green
Write-Host ""

# Step 2: Build and push API image (with UI files)
Write-Host "Step 2: Building and pushing API image..." -ForegroundColor Cyan
# Build from root to include both api and ui folders
docker build -f api/Dockerfile -t vericase-api:latest --build-arg BUILDKIT_INLINE_CACHE=1 .
docker tag vericase-api:latest ${ECR_API_REPO}:latest
docker push ${ECR_API_REPO}:latest
Write-Host "✓ API image pushed successfully" -ForegroundColor Green
Write-Host ""

# Step 3: Build and push Worker image
Write-Host "Step 3: Building and pushing Worker image..." -ForegroundColor Cyan
Push-Location worker
docker build -t vericase-worker:latest .
docker tag vericase-worker:latest "$ECR_WORKER_REPO:latest"
docker push "$ECR_WORKER_REPO:latest"
Pop-Location
Write-Host "✓ Worker image pushed successfully" -ForegroundColor Green
Write-Host ""

# Step 4: Fetch RDS password from Secrets Manager
Write-Host "Step 4: Fetching RDS credentials from Secrets Manager..." -ForegroundColor Cyan
$RDS_SECRET_ARN = "arn:aws:secretsmanager:eu-west-2:526015377510:secret:rds-db-5818fc76-6f0c-4d02-8aa4-df3d01776ed3"
$secretJson = aws secretsmanager get-secret-value --secret-id $RDS_SECRET_ARN --region $AWS_REGION --query SecretString --output text
$secret = $secretJson | ConvertFrom-Json
$DB_USERNAME = $secret.username
$DB_PASSWORD = $secret.password
$DB_HOST = "database-1.cv8uw0uuqr7f.eu-west-2.rds.amazonaws.com"
$DB_PORT = "5432"
$DB_NAME = "vericase"

$DATABASE_URL = "postgresql+psycopg2://${DB_USERNAME}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
Write-Host "✓ Database credentials retrieved" -ForegroundColor Green
Write-Host ""

# Step 5: Create Kubernetes Secret for DATABASE_URL
Write-Host "Step 5: Creating Kubernetes secret for database credentials..." -ForegroundColor Cyan
kubectl create secret generic vericase-db-secret --from-literal=DATABASE_URL="$DATABASE_URL" --dry-run=client -o yaml | kubectl apply -f -
Write-Host "✓ Database secret created/updated" -ForegroundColor Green
Write-Host ""

# Step 6: Apply ConfigMap
Write-Host "Step 6: Applying Kubernetes ConfigMap..." -ForegroundColor Cyan
kubectl apply -f kubernetes-configmap-aws.yaml
Write-Host "✓ ConfigMap applied" -ForegroundColor Green
Write-Host ""

# Step 7: Restart deployments
Write-Host "Step 7: Restarting deployments to pick up new images..." -ForegroundColor Cyan
kubectl rollout restart deployment/vericase-api
kubectl rollout restart deployment/vericase-worker
Write-Host "✓ Deployments restarted" -ForegroundColor Green
Write-Host ""

# Step 8: Wait for rollout to complete
Write-Host "Step 8: Waiting for rollout to complete..." -ForegroundColor Cyan
kubectl rollout status deployment/vericase-api --timeout=5m
kubectl rollout status deployment/vericase-worker --timeout=5m
Write-Host "✓ Rollout completed" -ForegroundColor Green
Write-Host ""

# Step 9: Check pod status
Write-Host "Step 9: Checking pod status..." -ForegroundColor Cyan
Write-Host ""
kubectl get pods -l app=vericase-api
Write-Host ""
kubectl get pods -l app=vericase-worker
Write-Host ""

# Step 10: Display logs
Write-Host "Step 10: Displaying recent logs..." -ForegroundColor Cyan
Write-Host ""
Write-Host "=== API Logs ===" -ForegroundColor Yellow
kubectl logs -l app=vericase-api --tail=20
Write-Host ""
Write-Host "=== Worker Logs ===" -ForegroundColor Yellow
kubectl logs -l app=vericase-worker --tail=20
Write-Host ""

Write-Host "=== Deployment Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Check if pods are running: kubectl get pods"
Write-Host "2. View API logs: kubectl logs -f deployment/vericase-api"
Write-Host "3. View worker logs: kubectl logs -f deployment/vericase-worker"
Write-Host "4. Test the load balancer endpoint"
Write-Host ""
