'''
Define pydantic models for user creation, response, updation

'''

from pydantic import BaseModel, Field
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