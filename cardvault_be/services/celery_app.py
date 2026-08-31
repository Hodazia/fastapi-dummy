from celery import Celery


celery_app = Celery(
    "celery_demo",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["services.tasks"],
)