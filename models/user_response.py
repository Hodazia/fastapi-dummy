'''
Define a random response from a /health endpoint

'''

from pydantic import BaseModel, Field

class UserResponse(BaseModel):
    message: str = Field(description="A random message from the /health endpoint")