'''

POST /register

POST /login

'''

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.dependencies import get_db
from database.models import User
from core.security import hash_password, verify_password, create_access_token
from schemas.user_schema import UserRegister,UserLogin,UserResponse,Token


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


'''
client sends,
{
    "username": "zia",
    "password": "mypassword"
}
the DB becomes,
users

id | username | hashed_password
---|----------|----------------
1  | zia      | $argon2id$...
'''
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, db:Session = Depends(get_db)):
    existing_user = db.execute(
        select(User).where(
                User.username == user_data.username
        )
    ).scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    hashed_password = hash_password(user_data.password)
    new_user = User(username=user_data.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post(
    "/login",
    response_model=Token
)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):

    # 1. Find user by username
    user = db.execute(
        select(User).where(
            User.username == user_data.username
        )
    ).scalar_one_or_none()

    # 2. User doesn't exist
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # 3. Verify password
    password_valid = verify_password(
        user_data.password,
        user.hashed_password
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # 4. Create JWT
    access_token = create_access_token(
        user.id
    )

    # 5. Return JWT
    return Token(
        access_token=access_token,
        token_type="bearer"
    )