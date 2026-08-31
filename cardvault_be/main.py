from fastapi import FastAPI
import os 
import uvicorn
from dotenv import load_dotenv
from routes.user.user_routes import router as userauth_router
from routes.content.content_routes import router as content_router
from services.tasks import add_numbers,multiply_numbers,slow_task, slow_task2,unreliable_task
from services.celery_app import celery_app
from celery.result import AsyncResult

load_dotenv()

app = FastAPI()
app.include_router(userauth_router)
app.include_router(content_router)

@app.get("/health")
def get_health():
    return {
        "status":"the server is healthy"
    }


@app.post("/tasks/add")
def add():

    # it does not execute immediately , it puts add_numbers into the cleery queue
    task = add_numbers.delay(10, 20)

    return {
        "task_id": task.id,
        "message": "Task submitted"
    }


@app.post("/tasks/slow")
def slow():
    task = slow_task.delay(20)
    '''
    start your worker and call this endpoint
    and then call it again 2 more times, u would have created 3 tasks
    Redis contains tasks waiting to be processed.
    The worker receives them.
    
    we will see like this,
    Task slow_task[A] received
    Task slow_task[B] received
    Task slow_task[C] received

    if your worker has concurrency of 4, then
    Worker
    │
    ├── Process 1 → Task A
    ├── Process 2 → Task B
    ├── Process 3 → Task C
    └── Process 4 → available

    THINK ABOUT HOW TO ACHIEVE THIS!
    '''

    return {
        "task_id": task.id,
        "message": "Slow task submitted"
    }

@app.post("/tasks/multiply")
def multiply():
    a = 10
    b = 20
    task = multiply_numbers.delay(a,b)

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
    # this tells that task will be in the redis for 10 seconds and then taken by the worker

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

    # it returns an object containing th task ID
    '''
    Task ID
   |
   v
    Redis
    |
    ├── PENDING
    ├── STARTED
    └── SUCCESS → 30
    '''
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
