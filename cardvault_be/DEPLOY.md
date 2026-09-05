# CardVault EC2 Deployment Guide

Cost-conscious production setup for FastAPI + Celery + Redis, with **managed Postgres (Neon)** on a **single EC2 instance**.

## Recommended architecture (low cost)

```text
Internet
   │
   ▼
EC2 (t3.micro / t4g.micro)          Neon Postgres (free tier)
   │                                      ▲
   ├── nginx :80 / :443                   │
   ├── api (FastAPI) ─────────────────────┘
   ├── celery-worker
   ├── celery-beat
   └── redis (Docker, same instance)
```

### Why this saves money

| Component | Recommendation | Approx. cost |
|-----------|----------------|--------------|
| EC2 | `t3.micro` or `t4g.micro` (1 vCPU, 1 GB RAM) | ~$0–8/month (free tier eligible) |
| Postgres | Keep **Neon** (already in use) | Free tier available |
| Redis | Run in Docker on the same EC2 | $0 extra |
| ElastiCache | **Skip** for now | Saves ~$15+/month |
| RDS | **Skip** for now | Saves ~$15+/month |
| Load balancer | **Skip** for a single instance | Saves ~$16+/month |

For a side project or MVP, one small EC2 + Neon + local Redis is the sweet spot.

---

## Prerequisites

1. AWS account
2. A domain name (optional but recommended for HTTPS)
3. Your Neon `DATABASE_URL` (already configured locally)
4. A strong `SECRET_KEY` (32+ characters)

Generate a secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

---

## Step 1 — Launch EC2

1. Go to **EC2 → Launch instance**
2. **AMI:** Ubuntu 24.04 LTS
3. **Instance type:** `t3.micro` (x86) or `t4g.micro` (ARM, often cheaper)
4. **Key pair:** Create or select one
5. **Storage:** 20 GB gp3 is enough
6. **Security group:**
   - SSH (22) — **your IP only**
   - HTTP (80) — `0.0.0.0/0`
   - HTTPS (443) — `0.0.0.0/0`
   - Do **not** expose 8000 or 6379 publicly; nginx talks to the API internally

7. Launch the instance

---

## Step 2 — Connect and install Docker

```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

Run the setup script from the repo:

```bash
bash deploy/ec2-setup.sh
```

Or manually:

```bash
sudo apt-get update
sudo apt-get install -y git curl
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu
newgrp docker
```

---

## Step 3 — Deploy the app

```bash
git clone YOUR_REPO_URL
cd YOUR_REPO/cardvault_be

cp .env.example .env
nano .env   # fill DATABASE_URL, SECRET_KEY, CORS_ORIGINS
```

Production `.env` example:

```env
ENVIRONMENT=production
LOG_LEVEL=INFO
DATABASE_URL=postgresql+psycopg://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
SECRET_KEY=your-long-random-secret-here
CORS_ORIGINS=https://your-frontend.com
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
SQL_ECHO=false
```

Start all services:

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f api
```

Verify:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/health/ready
```

---

## Step 4 — nginx reverse proxy (recommended)

Install nginx on the host (not in Docker) so TLS terminates at the edge:

```bash
sudo apt-get install -y nginx
sudo cp deploy/nginx/cardvault.conf /etc/nginx/sites-available/cardvault
sudo ln -s /etc/nginx/sites-available/cardvault /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

For HTTPS with Let's Encrypt:

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

---

## Step 5 — Auto-restart on reboot

Docker Compose uses `restart: unless-stopped`, so containers come back after reboot once Docker starts.

Enable Docker on boot:

```bash
sudo systemctl enable docker
```

---

## Updating the app

```bash
cd ~/cardvault_be
git pull
docker compose up -d --build
```

---

## Monitoring and logs

```bash
docker compose logs -f
docker compose logs -f api
docker compose logs -f celery-worker
docker compose logs -f celery-beat
docker stats
```

---

## Cost-saving tips

1. **Stop the instance** when not in use (dev/staging) — you only pay for EBS storage while stopped.
2. Use **t4g.micro** (Graviton) if your image supports ARM — often 20% cheaper.
3. Keep Postgres on **Neon free tier** instead of RDS.
4. Run Redis on the same EC2 — no ElastiCache needed at this scale.
5. Set **CloudWatch billing alerts** so you get notified early.
6. Use a **single Celery worker** with `--concurrency=2` on a 1 GB instance.

---

## Production checklist

- [ ] `ENVIRONMENT=production` in `.env`
- [ ] Strong `SECRET_KEY` (32+ chars)
- [ ] `CORS_ORIGINS` set to your frontend domain (not `*`)
- [ ] Neon DB URL uses `postgresql+psycopg://` and `sslmode=require`
- [ ] Security group: only 22, 80, 443 open (not 8000/6379)
- [ ] HTTPS enabled via nginx + certbot
- [ ] `docker compose ps` shows all 4 services healthy
- [ ] `/health/ready` returns `"status": "ready"`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Celery tasks not running | Check `docker compose logs celery-worker` |
| Redis connection refused | Ensure `CELERY_BROKER_URL=redis://redis:6379/0` in compose |
| DB connection failed | Verify Neon URL and that EC2 outbound internet works |
| OOM on t3.micro | Lower Celery concurrency to 1 |
| Beat schedule not firing | Check `docker compose logs celery-beat` |
