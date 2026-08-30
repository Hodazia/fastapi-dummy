from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from database.dependencies import get_db
from database.models import ClientUser
from models.user import ClientUserRegister, ClientUserLogin, ClientUserResponse, Token
from core.security import hash_password, verify_password, create_access_token
from core.jwt_dependencies import get_current_user

router = APIRouter(
    prefix="/client_user",
    tags=["client_user"]
)

@router.post("/register", response_model=ClientUserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: ClientUserRegister, db: Session = Depends(get_db)) -> ClientUserResponse:
    existing_user = db.execute(
        select(ClientUser).where(
            or_(
                ClientUser.email == user_data.email,
                ClientUser.username == user_data.username,
            )
        )
    ).scalar_one_or_none()
    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    hashed_password = hash_password(user_data.password)
    new_user = ClientUser(email=user_data.email, username=user_data.username, hashed_password=hashed_password,role="user")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(
    credentials: ClientUserLogin,
    db: Session = Depends(get_db),
):
    user = db.scalar(
        select(ClientUser).where(ClientUser.email == credentials.email)
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        credentials.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Inactive user",
        )

    access_token = create_access_token(
        user_id=user.id,
        role=user.role,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/me", response_model=ClientUserResponse)
def get_my_profile(
    current_user:Annotated[
    ClientUser,Depends(get_current_user)]
):
    return current_user
