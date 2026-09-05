from celery import Celery

from core.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "cardvault",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["services.tasks"],
)

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=300,
    worker_prefetch_multiplier=1,
)

celery_app.conf.beat_schedule = {
    "print-message-every-10-seconds": {
        "task": "services.tasks.print_message",
        "schedule": 10.0,
    }
}
