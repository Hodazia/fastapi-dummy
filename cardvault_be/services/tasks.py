import logging
import random
import time

from services.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def add_numbers(a: int, b: int):
    logger.info("Adding %s + %s", a, b)
    time.sleep(10)

    result = a + b
    logger.info("Result = %s", result)
    return result


@celery_app.task
def slow_task(seconds: int):
    logger.info("Starting slow task for %s seconds", seconds)
    time.sleep(seconds)
    logger.info("Slow task finished")
    return f"Completed after {seconds} seconds"


@celery_app.task
def slow_task2(task_number: int):
    logger.info("START task %s", task_number)

    time.sleep(10)

    logger.info("END task %s", task_number)

    return f"Task {task_number} completed"


@celery_app.task
def multiply_numbers(a: int, b: int):
    logger.info("Multiplying %s * %s", a, b)
    time.sleep(3)
    return a * b


@celery_app.task
def print_message():
    logger.info("Hello from scheduled Celery task!")
    return "Hello!"


@celery_app.task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    bind=True,
    max_retries=3
)
def unreliable_task(self):
    logger.info("Running task")

    if random.random() < 0.7:
        logger.warning("Task failed, retrying")
        raise self.retry(countdown=5)

    logger.info("Task succeeded")
    return "Success"
