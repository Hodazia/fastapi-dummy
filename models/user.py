'''
Define pydantic models for user creation, response, updation

'''

from pydantic import BaseModel, Field,EmailStr , ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    name:str = Field(description="The name of the user")
    email:str = Field(description="The email of the user")
    age:int = Field(description="The age of the user")

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None


class ClientUserRegister(BaseModel):
    email:EmailStr  
    username: str = Field(min_length=3, max_length=50)
    password:str = Field(min_length=8, max_length=100)
# we won't store the user's password but rather the hashed password

class ClientUserLogin(BaseModel):
    email: EmailStr
    password: str


class ClientUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    role: str
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str