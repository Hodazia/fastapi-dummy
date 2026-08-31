from fastapi import FastAPI
import os 
import uvicorn
from dotenv import load_dotenv
from routes.user.user_routes import router as userauth_router
from routes.content.content_routes import router as content_router
from services.tasks import add_numbers
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


@app.post("/add")
def add():

    # it does not execute immediately , it puts add_numbers into the cleery queue
    task = add_numbers.delay(10, 20)

    return {
        "task_id": task.id,
        "message": "Task submitted"
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


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
