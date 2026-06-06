
'''
POST    /users/{user_id}/tasks
GET     /users/{user_id}/tasks

GET     /tasks/{task_id}
PUT     /tasks/{task_id}
DELETE  /tasks/{task_id}


'''

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database.dependencies import get_db

from schemas.task_schema import (
    TaskCreate,
    TaskUpdate,
    TaskResponse
)

from services.task_service import (
    create_task,
    get_user_tasks,
    get_task,
    update_task,
    delete_task
)

router = APIRouter(
    tags=["Tasks"]
)

@router.post("/users/{user_id}/tasks", response_model=TaskResponse)
def create_new_task(
    user_id: int,
    payload: TaskCreate,
    db: Session = Depends(get_db)
):

    task = create_task(
        db,
        user_id,
        payload
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return task


@router.get("/users/{user_id}/tasks", response_model=list[TaskResponse])
def fetch_user_tasks(
    user_id: int,
    db: Session = Depends(get_db)
):

    return get_user_tasks(
        db,
        user_id
    )

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def fetch_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = get_task(
        db,
        task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@router.put("/tasks/{task_id}",response_model=TaskResponse)
def edit_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db)
):

    task = update_task(
        db,
        task_id,
        payload
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@router.delete("/tasks/{task_id}")
def remove_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_task(
        db,
        task_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task deleted successfully"
    }