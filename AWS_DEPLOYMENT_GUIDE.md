# AWS Deployment Guide

## Code Changes Completed ✓

All code has been updated to support AWS services (RDS, S3, OpenSearch with TLS):

- **API Configuration** (`api/app/config.py`): Added AWS mode flags and TLS settings
- **Worker Configuration** (`worker/worker_app/config.py`): Added AWS mode flags and TLS settings  
- **API Storage** (`api/app/storage.py`): S3 client now supports IRSA when `MINIO_ENDPOINT` is empty
- **API Search** (`api/app/search.py`): OpenSearch client now supports TLS
- **Worker** (`worker/worker_app/worker.py`): Both S3 and OpenSearch clients now support AWS mode

## Required Environment Variables for AWS Mode

Add these to your Kubernetes ConfigMap:

```yaml
# Enable AWS services mode
USE_AWS_SERVICES: "true"

# S3 Configuration (leave MINIO_ENDPOINT empty to use IRSA)
MINIO_ENDPOINT: ""
MINIO_ACCESS_KEY: ""
MINIO_SECRET_KEY: ""
MINIO_BUCKET: "your-s3-bucket-name"
AWS_REGION: "us-east-1"  # or your region

# OpenSearch with TLS
OPENSEARCH_HOST: "your-domain.us-east-1.es.amazonaws.com"
OPENSEARCH_PORT: "443"
OPENSEARCH_USE_SSL: "true"
OPENSEARCH_VERIFY_CERTS: "true"
OPENSEARCH_INDEX: "documents"

# Database (from Secrets Manager secret)
DATABASE_URL: "postgresql+psycopg2://username:password@your-rds-endpoint:5432/vericase"
```

## Rebuild and Deploy Steps

### 1. Set Your AWS Account Details

```bash
export AWS_ACCOUNT_ID="your-account-id"
export AWS_REGION="us-east-1"  # or your region
```

### 2. Authenticate with ECR

```bash
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
```

### 3. Build and Push API Image

```bash
cd api
docker build -t vericase-api .
docker tag vericase-api:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/vericase-api:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/vericase-api:latest
cd ..
```

### 4. Build and Push Worker Image

```bash
cd worker
docker build -t vericase-worker .
docker tag vericase-worker:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/vericase-worker:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/vericase-worker:latest
cd ..
```

### 5. Update Kubernetes ConfigMap

Update your ConfigMap with the environment variables listed above:

```bash
kubectl edit configmap vericase-config
```

Or apply a new ConfigMap YAML:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: vericase-config
data:
  USE_AWS_SERVICES: "true"
  MINIO_ENDPOINT: ""
  MINIO_ACCESS_KEY: ""
  MINIO_SECRET_KEY: ""
  MINIO_BUCKET: "your-bucket-name"
  AWS_REGION: "us-east-1"
  OPENSEARCH_HOST: "your-domain.us-east-1.es.amazonaws.com"
  OPENSEARCH_PORT: "443"
  OPENSEARCH_USE_SSL: "true"
  OPENSEARCH_VERIFY_CERTS: "true"
  OPENSEARCH_INDEX: "documents"
  REDIS_URL: "redis://redis:6379/0"
  CELERY_QUEUE: "ocr"
  TIKA_URL: "http://tika:9998"
  JWT_SECRET: "your-secret-here"
```

### 6. Restart Deployments to Pick Up New Images

```bash
# Restart API deployment
kubectl rollout restart deployment/vericase-api

# Restart Worker deployment
kubectl rollout restart deployment/vericase-worker

# Check rollout status
kubectl rollout status deployment/vericase-api
kubectl rollout status deployment/vericase-worker
```

### 7. Verify Pods Are Running

```bash
kubectl get pods
kubectl logs -f deployment/vericase-api
kubectl logs -f deployment/vericase-worker
```

## How the Fix Works

### S3/IRSA Support
- When `USE_AWS_SERVICES=true` or `MINIO_ENDPOINT=""`, boto3 clients are created without `endpoint_url` or explicit credentials
- This allows the pod's IRSA service account to provide credentials automatically
- No more `ValueError: Invalid endpoint` errors

### OpenSearch TLS Support  
- When `OPENSEARCH_USE_SSL=true`, OpenSearch clients connect over HTTPS
- When `OPENSEARCH_VERIFY_CERTS=true`, TLS certificates are verified
- Port should be set to `443` for AWS OpenSearch
- No more connection failures due to TLS/SSL mismatches

### Database Connection
- `DATABASE_URL` is now fully configurable from environment variables
- The connection string from Secrets Manager can be injected directly
- No more "postgres" hostname hardcoding

## Troubleshooting

### API/Worker Pods Still Crashing?

1. Check pod logs:
   ```bash
   kubectl logs -f deployment/vericase-api
   kubectl logs -f deployment/vericase-worker
   ```

2. Verify ConfigMap is mounted:
   ```bash
   kubectl describe pod <pod-name>
   ```

3. Check IRSA permissions:
   ```bash
   kubectl describe serviceaccount vericase-api
   ```

4. Verify S3 bucket exists and IRSA role has permissions:
   ```bash
   aws s3 ls s3://your-bucket-name
   ```

5. Test OpenSearch connectivity from a pod:
   ```bash
   kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
     curl -k https://your-domain.us-east-1.es.amazonaws.com
   ```

### Images Not Updating?

Force pull new images by deleting pods:
```bash
kubectl delete pod -l app=vericase-api
kubectl delete pod -l app=vericase-worker
```

## Success Indicators

✓ API pod shows: `Starting server at 0.0.0.0:8000`
✓ Worker pod shows: `[tasks] registered tasks`
✓ No more boto3 endpoint errors
✓ No more OpenSearch SSL errors
✓ Load balancer returns HTTP responses instead of "connection closed"
