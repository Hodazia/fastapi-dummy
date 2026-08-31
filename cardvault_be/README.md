### run on 3 terminals


- Terminal 1: uv run uvicorn main:app --reload
- Terminal 2: docker run -p 6379:6379 --redis
- Terminal 3: uv run celery -A services.celery_app worker --loglevel=info

