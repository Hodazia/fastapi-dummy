from re import S
from turtle import st
from pydantic import BaseModel , Field, ConfigDict

class UserRegister(BaseModel):
    username:str = Field(min_length=3, max_length=50)
    password:str = Field(min_length=3, max_length=50)

class  UserLogin(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):
    id:int
    username:str
    model_config = ConfigDict(
        from_attributes=True
    )


class Token(BaseModel):
    access_token:str
    token_type:str