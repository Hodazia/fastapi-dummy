# CardVault Backend

FastAPI + Celery + Redis API with JWT auth and content management.

## Local development

```bash
cp .env.example .env   # set DATABASE_URL and optionally SECRET_KEY

# Terminal 1 — API
uv run uvicorn main:app --reload

# Terminal 2 — Redis
docker run -d -p 6379:6379 --name cardvault-redis redis:7-alpine

# Terminal 3 — Celery worker
uv run celery -A services.celery_app worker --loglevel=info

# Terminal 4 — Celery beat (optional, for scheduled tasks)
uv run celery -A services.celery_app beat --loglevel=info
```

## Docker (production-like stack)

```bash
cp .env.example .env   # fill in production values
docker compose up -d --build
curl http://localhost:8000/health/ready
```

## AWS EC2 deployment

See [DEPLOY.md](./DEPLOY.md) for the full cost-optimized EC2 guide.

## Health endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Liveness — API is running |
| `GET /health/ready` | Readiness — DB + Redis checks |

## Environment variables

See [.env.example](./.env.example) for all supported variables.
