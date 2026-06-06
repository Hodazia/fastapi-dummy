from sqlalchemy.orm import Session

from database.models import User
from schemas.user_schema import UserCreate,UserResponse,UserUpdate

def create_user(
    db: Session,
    payload: UserCreate
):

    existing_user = (
        db.query(User)
        .filter(
            User.email == payload.email
        )
        .first()
    )

    if existing_user:
        raise ValueError(
            "Email already exists"
        )

    user = User(
        username=payload.username,
        email=payload.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_users(
    db: Session
):

    return (
        db.query(User)
        .all()
    )

def get_user(
    db: Session,
    user_id: int
):

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

def update_user(
    db: Session,
    user_id: int,
    payload: UserUpdate
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        return None

    update_data = payload.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user

def delete_user(
    db: Session,
    user_id: int
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        return False

    db.delete(user)
    db.commit()

    return True