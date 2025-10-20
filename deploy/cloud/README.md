# Cloud Deployment Guide

Follow these steps to host VeriCase Docs on a public domain so users hit a single HTTPS URL.

## 1. Provision infrastructure

1. Launch an Ubuntu 22.04+ VM (2 vCPU / 4 GB RAM suggested) on your favourite provider (AWS Lightsail, DigitalOcean, Hetzner, etc.).
2. Assign a static/public IP.
3. Point a DNS record (e.g. `docs.yourdomain.com`) to that IP.

## 2. Prepare the host

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin nginx certbot python3-certbot-nginx git
sudo usermod -aG docker $USER
newgrp docker
```

Clone the repo (or rsync it up):

```bash
git clone https://github.com/your-org/vericase-docs.git
cd vericase-docs
```

## 3. Configure environment

1. Copy the cloud env template:
   ```bash
   cp deploy/cloud/.env.cloud.example .env
   ```
2. Set strong values for `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, and `JWT_SECRET`.
3. Update `MINIO_PUBLIC_ENDPOINT` and `CORS_ORIGINS` to match your domain.

## 4. Launch the containers

```bash
cd deploy/cloud
docker compose up -d --build
```

All services (API, worker, MinIO, OpenSearch, etc.) now listen on localhost-only ports so that only the reverse proxy can reach them.

## 5. Configure Nginx reverse proxy

1. Copy the sample config:
   ```bash
   sudo cp deploy/cloud/nginx.conf.example /etc/nginx/sites-available/vericase-docs
   sudo ln -s /etc/nginx/sites-available/vericase-docs /etc/nginx/sites-enabled/vericase-docs
   ```
2. Edit `/etc/nginx/sites-available/vericase-docs` and replace `docs.yourdomain.com` with your real domain.
3. Test and reload:
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

At this point HTTP traffic should proxy to the API and MinIO.

## 6. Enable HTTPS

Let’s Encrypt can be issued via certbot’s nginx plugin:

```bash
sudo certbot --nginx -d docs.yourdomain.com
```

Certbot will update the Nginx config to redirect HTTP → HTTPS and configure automatic renewals.

## 7. Verify

1. Open `https://docs.yourdomain.com/ui` and create an account.
2. Upload a document, wait a few seconds for OCR/indexing, and run a search from the UI.
3. Use the TypeScript SDK with base URL `https://docs.yourdomain.com`.

Optional: expose the MinIO console by adding a `/minio-console` location block and protecting it with basic auth.

## 8. Maintenance tips

- **Backups:** snapshot MinIO data volume and Postgres volume regularly.
- **Monitoring:** watch container logs (`docker compose logs -f api worker`).
- **Updates:** pull latest code, rebuild containers (`docker compose pull && docker compose up -d --build`).
- **Scaling:** move Postgres/OpenSearch to managed services or larger nodes as your corpus grows.

You now have a single-domain, TLS-terminated VeriCase Docs instance that your whole team can use.
