from sqlalchemy.orm import Session

from database.models import User,Task
from schemas.task_schema import TaskCreate,TaskResponse,TaskUpdate

def create_task(
    db: Session,
    user_id: int,
    payload: TaskCreate
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        return None

    task = Task(
        title=payload.title,
        description=payload.description,
        owner_id=user_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_user_tasks(
    db: Session,
    user_id: int
):

    return (
        db.query(Task)
        .filter(Task.owner_id == user_id)
        .all()
    )


def get_task(
    db: Session,
    task_id: int
):

    return (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

def update_task(
    db: Session,
    task_id: int,
    payload: TaskUpdate
):

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        return None

    update_data = payload.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task

def delete_task(
    db: Session,
    task_id: int
):

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        return False

    db.delete(task)
    db.commit()

    return True