from pydantic import BaseModel,Field, ConfigDict
from datetime import datetime


'''
the frontend will send like this, 
{
    "title": "FastAPI",
    "content": "Learning FastAPI",
    "link": "https://fastapi.tiangolo.com",
    "type": "Website",
    "tags": [
        "python",
        "backend",
        "fastapi"
    ]
}
'''
class ContentCreate(BaseModel):
    title:str = Field(
        min_length=1,
        max_length=255
    )

    content:str = Field(
        min_length=1
    )
    link: str = Field(
        min_length=1,
        max_length=500
    )

    type: str = Field(
        min_length=1,
        max_length=100
    )

    tags: list[str] = Field(
        default_factory=list
    )


class TagResponse(BaseModel):

    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )


class UserBasicResponse(BaseModel):

    id: int
    username: str

    model_config = ConfigDict(
        from_attributes=True
    )


class ContentResponse(BaseModel):

    id: int
    title: str
    content: str
    link: str
    type: str
    user_id: int
    created_at: datetime

    tags: list[TagResponse]

    model_config = ConfigDict(
        from_attributes=True
    )


class ContentCreateResponse(BaseModel):

    message: str
    content: ContentResponse

class TagsCreate(BaseModel):
    tags: list[str] = Field(
        min_length=1
    )

class TagsResponse(BaseModel):

    message: str
    tags: list[TagResponse]