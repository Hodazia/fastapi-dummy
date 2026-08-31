from celery import Celery


celery_app = Celery(
    "celery_demo",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["services.tasks"],
)

# this will run the print_message task after evry 10 seconds 
'''
Every 10 seconds
       ↓
Celery Beat
       ↓
"Execute services.tasks.print_message"
       ↓
Redis

'''
celery_app.conf.beat_schedule = {

    "print-message-every-10-seconds": {
        "task": "services.tasks.print_message",
        "schedule": 10.0,
    }

}