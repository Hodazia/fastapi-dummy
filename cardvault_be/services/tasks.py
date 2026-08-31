import time
from services.celery_app import celery_app
import random

#"This function is a task that a Celery worker can execute."
@celery_app.task
def add_numbers(a:int, b:int):
    print(f"Adding {a} + {b}")
    time.sleep(10)

    result = a+b 
    print(f"Result = {result}")
    return result

@celery_app.task
def slow_task(seconds: int):
    print(f"Starting slow task for {seconds} seconds")
    time.sleep(seconds)
    print("Slow task finished")
    return f"Completed after {seconds} seconds"

@celery_app.task
def slow_task2(task_number: int):
    print(f"START task {task_number}")

    time.sleep(10)

    print(f"END task {task_number}")

    return f"Task {task_number} completed"

@celery_app.task
def multiply_numbers(a: int, b: int):
    print(f"Multiplying {a} * {b}")
    time.sleep(3)
    return a * b

@celery_app.task
def print_message():
    print("Hello from scheduled Celery task!")
    return "Hello!"


@celery_app.task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    bind=True,
    max_retries=3
)
def unreliable_task(self):
    print("Running task")

    if random.random() < 0.7:
        print("Task failed")
        raise self.retry(
            countdown=5
        )

    print("Task succeeded")
    return "Success"