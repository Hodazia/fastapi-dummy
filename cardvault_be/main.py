import logging
from contextlib import asynccontextmanager

import redis
import uvicorn
from celery.result import AsyncResult
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from core.logging_config import setup_logging
from core.settings import get_settings
from database.start_db import engine, init_db
from routes.content.content_routes import router as content_router
from routes.user.user_routes import router as userauth_router
from services.celery_app import celery_app
from services.tasks import (
    add_numbers,
    multiply_numbers,
    slow_task,
    slow_task2,
    unreliable_task,
)

settings = get_settings()
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CardVault API (%s)", settings.environment)
    init_db()
    yield
    logger.info("Shutting down CardVault API")


app = FastAPI(
    title="CardVault API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userauth_router)
app.include_router(content_router)


@app.get("/health")
def get_health():
    return {
        "status": "healthy",
        "environment": settings.environment,
    }


@app.get("/health/ready")
def readiness_check():
    checks = {
        "database": "unknown",
        "redis": "unknown",
    }

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as exc:
        logger.exception("Database readiness check failed")
        checks["database"] = str(exc)

    try:
        redis_client = redis.from_url(settings.celery_broker_url)
        redis_client.ping()
        checks["redis"] = "ok"
    except Exception as exc:
        logger.exception("Redis readiness check failed")
        checks["redis"] = str(exc)

    is_ready = all(value == "ok" for value in checks.values())
    payload = {
        "status": "ready" if is_ready else "degraded",
        "checks": checks,
    }

    return JSONResponse(
        status_code=200 if is_ready else 503,
        content=payload,
    )


@app.post("/tasks/add")
def add():
    task = add_numbers.delay(10, 20)

    return {
        "task_id": task.id,
        "message": "Task submitted"
    }


@app.post("/tasks/slow")
def slow():
    task = slow_task.delay(20)

    return {
        "task_id": task.id,
        "message": "Slow task submitted"
    }


@app.post("/tasks/multiply")
def multiply():
    a = 10
    b = 20
    task = multiply_numbers.delay(a, b)

    return {
        "task_id": task.id,
        "message": "Multiplication task submitted"
    }


@app.post("/tasks/multiple")
def multiple_tasks():
    task1 = add_numbers.delay(10, 20)
    task2 = multiply_numbers.delay(10, 20)
    task3 = slow_task.delay(10)

    return {
        "tasks": [
            task1.id,
            task2.id,
            task3.id
        ]
    }


@app.post("/tasks/delayed")
def delayed():
    task = add_numbers.apply_async(
        args=[10, 20],
        countdown=10
    )

    return {
        "task_id": task.id,
        "message": "Task will execute after 10 seconds"
    }


@app.post("/tasks/unreliable")
def unreliable():
    task = unreliable_task.delay()

    return {
        "task_id": task.id
    }


@app.post("/tasks/{task_number}")
def create_task(task_number: int):
    task = slow_task2.delay(task_number)

    return {
        "task_id": task.id
    }


@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task = AsyncResult(
        task_id,
        app=celery_app
    )

    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result
    }


@app.delete("/tasks/{task_id}")
def cancel_task(task_id: str):
    celery_app.control.revoke(
        task_id,
        terminate=True
    )

    return {
        "task_id": task_id,
        "message": "Task revoked"
    }


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
