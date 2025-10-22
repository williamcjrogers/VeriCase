#!/bin/bash
set -e

# VeriCase AWS Deployment Script
# This script rebuilds Docker images and deploys to your EKS cluster

echo "=== VeriCase AWS Deployment Script ==="
echo ""

# Configuration
export AWS_ACCOUNT_ID="526015377510"
export AWS_REGION="eu-west-2"
export ECR_API_REPO="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/vericase-api"
export ECR_WORKER_REPO="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/vericase-worker"

# Step 1: Authenticate with ECR
echo "Step 1: Authenticating with ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
echo "✓ ECR authentication successful"
echo ""

# Step 2: Build and push API image
echo "Step 2: Building and pushing API image..."
cd api
docker build -t vericase-api:latest .
docker tag vericase-api:latest ${ECR_API_REPO}:latest
docker push ${ECR_API_REPO}:latest
cd ..
echo "✓ API image pushed successfully"
echo ""

# Step 3: Build and push Worker image
echo "Step 3: Building and pushing Worker image..."
cd worker
docker build -t vericase-worker:latest .
docker tag vericase-worker:latest ${ECR_WORKER_REPO}:latest
docker push ${ECR_WORKER_REPO}:latest
cd ..
echo "✓ Worker image pushed successfully"
echo ""

# Step 4: Fetch RDS password from Secrets Manager
echo "Step 4: Fetching RDS credentials from Secrets Manager..."
RDS_SECRET_ARN="arn:aws:secretsmanager:eu-west-2:526015377510:secret:rds-db-5818fc76-6f0c-4d02-8aa4-df3d01776ed3"
SECRET_JSON=$(aws secretsmanager get-secret-value --secret-id ${RDS_SECRET_ARN} --region ${AWS_REGION} --query SecretString --output text)
DB_USERNAME=$(echo ${SECRET_JSON} | jq -r .username)
DB_PASSWORD=$(echo ${SECRET_JSON} | jq -r .password)
DB_HOST="database-1.cv8uw0uuqr7f.eu-west-2.rds.amazonaws.com"
DB_PORT="5432"
DB_NAME="vericase"

DATABASE_URL="postgresql+psycopg2://${DB_USERNAME}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
echo "✓ Database credentials retrieved"
echo ""

# Step 5: Create Kubernetes Secret for DATABASE_URL
echo "Step 5: Creating Kubernetes secret for database credentials..."
kubectl create secret generic vericase-db-secret \
  --from-literal=DATABASE_URL="${DATABASE_URL}" \
  --dry-run=client -o yaml | kubectl apply -f -
echo "✓ Database secret created/updated"
echo ""

# Step 6: Apply ConfigMap
echo "Step 6: Applying Kubernetes ConfigMap..."
kubectl apply -f kubernetes-configmap-aws.yaml
echo "✓ ConfigMap applied"
echo ""

# Step 7: Restart deployments
echo "Step 7: Restarting deployments to pick up new images..."
kubectl rollout restart deployment/vericase-api
kubectl rollout restart deployment/vericase-worker
echo "✓ Deployments restarted"
echo ""

# Step 8: Wait for rollout to complete
echo "Step 8: Waiting for rollout to complete..."
kubectl rollout status deployment/vericase-api --timeout=5m
kubectl rollout status deployment/vericase-worker --timeout=5m
echo "✓ Rollout completed"
echo ""

# Step 9: Check pod status
echo "Step 9: Checking pod status..."
echo ""
kubectl get pods -l app=vericase-api
echo ""
kubectl get pods -l app=vericase-worker
echo ""

# Step 10: Display logs
echo "Step 10: Displaying recent logs..."
echo ""
echo "=== API Logs ==="
kubectl logs -l app=vericase-api --tail=20
echo ""
echo "=== Worker Logs ==="
kubectl logs -l app=vericase-worker --tail=20
echo ""

echo "=== Deployment Complete! ==="
echo ""
echo "Next steps:"
echo "1. Check if pods are running: kubectl get pods"
echo "2. View API logs: kubectl logs -f deployment/vericase-api"
echo "3. View worker logs: kubectl logs -f deployment/vericase-worker"
echo "4. Test the load balancer endpoint"
echo ""
