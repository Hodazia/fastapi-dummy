import time
from services.celery_app import celery_app

#"This function is a task that a Celery worker can execute."
@celery_app.task
def add_numbers(a:int, b:int):
    print(f"Adding {a} + {b}")
    time.sleep(10)

    result = a+b 
    print(f"Result = {result}")
    return result