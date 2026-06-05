from fastapi import APIRouter
from models.user_response import UserResponse

api_router =  APIRouter()


@api_router.get("/health", status_code=200, response_model=UserResponse) 
def health_check():
    return UserResponse(message="healthy")