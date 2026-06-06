from pydantic import BaseModel, Field
from datetime import datetime
'''
Define pydantic models for task creation, updation and response
'''

class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    owner_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }