from typing import List
from fastapi import APIRouter, HTTPException 
from models import user
from models.user import UserCreate, UserResponse, UserUpdate
from Service.user_service import get_all_users, get_user_by_id, create_user,update_user, delete_user

api_router =  APIRouter(
    prefix="/people", # it was users have updated to /people
    tags=["users"]
)


# fetch all users
@api_router.get("/", response_model=List[UserResponse])
def fetch_users():
    return get_all_users()

# create a new user
@api_router.post("/", response_model= UserResponse)
def add_users(user:UserCreate):
    return create_user(user)

# fetch user by id
@api_router.get("/{user_id}", response_model= UserResponse)
def fetch_user_by_id(user_id:int):
    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@api_router.put("/{user_id}", response_model=UserResponse)
def edit_user(user_id:int, payload:UserUpdate):
    user = update_user(user_id, payload)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@api_router.delete("/{user_id}", )
def edit_user(user_id:int):
    deleted_user = delete_user(user_id)

    if not deleted_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message":"User deleted successfully!"
    }

