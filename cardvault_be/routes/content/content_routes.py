'''
POST   /content
GET    /content
DELETE /content
GET    /tags
POST   /tags
GET    /content/filter/{content}


Express                → FastAPI
req.body               → Pydantic model
req.userId             → get_current_user()
ContentModel.create()  → db.add() + db.commit()
ContentModel.find()    → select(Content)
deleteOne()             → db.delete()
populate()             → SQLAlchemy relationship / selectinload
TagsModel.findOne()    → select(Tag)
MongoDB $in             → SQLAlchemy .in_()

the models,
User
    id
    username
    hashed_password
    contents
    link

Content
    id
    title
    content
    link
    type
    user_id
    created_at
    user
    tags

Tag
    id
    name
    created_at
    updated_at

ContentTag
    content_id
    tag_id

Link
    id
    hash
    user_id
    user
'''


from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session, selectinload
from typing import Annotated
from sqlalchemy import select
from database.dependencies import get_db
from database.models import Content,User,Tag
from core.security import hash_password, verify_password, create_access_token
from schemas.content_schema import ContentCreate,ContentCreateResponse,ContentResponse, TagsResponse, TagResponse,TagsCreate
from core.jwt_dependencies import get_current_user

router = APIRouter(
)

'''
{
    "title": "FastAPI",
    "content": "Learning FastAPI",
    "link": "https://fastapi.tiangolo.com",
    "type": "Website",
    "tags": [
        "python",
        "backend"
    ]
}

'''

@router.post("/content",status_code=status.HTTP_201_CREATED, response_model=ContentCreateResponse)
def create_content(content_data:ContentCreate ,
     current_user: Annotated[
        User,
        Depends(get_current_user)
    ],db:Session = Depends(get_db)):

    new_content = Content(
        title=content_data.title,
        content=content_data.content,
        link=content_data.link,
        type=content_data.type,
        user_id=current_user.id
    )

    for tag_name in content_data.tags:

        tag_name = tag_name.strip()
        # Ignore empty tags
        if not tag_name:
            continue

        existing_tag = db.execute(
            select(Tag).where(
                Tag.name == tag_name
            )
        ).scalar_one_or_none()

        if existing_tag:
            tag = existing_tag
        else:
            tag = Tag(
                name=tag_name
            )

            db.add(tag)
            db.flush()

        # Add relationship
        new_content.tags.append(tag)
    # -----------------------------------------
    # 3. Add Content
    # -----------------------------------------

    db.add(new_content)
    # -----------------------------------------
    # 4. Commit transaction
    # -----------------------------------------

    db.commit()

    # -----------------------------------------
    # 5. Refresh
    # -----------------------------------------

    db.refresh(new_content)
    return {
        "message": "Content added successfully",
        "content": new_content
    }

'''
the resulting tables are,
contents

id | title    | user_id
---|----------|--------
10 | FastAPI  | 1
tags

id | name
---|--------
1  | python
2  | backend
content_tags

content_id | tag_id
-----------|-------
10         | 1
10         | 2

'''


# return all the contents of the current user 
@router.get("/content" , response_model = list[ContentResponse])
def get_contents(
     current_user: Annotated[
        User,
        Depends(get_current_user)
    ],db:Session = Depends(get_db)):
    
    result = db.execute(
        select(Content)
        .where(
            Content.user_id == current_user.id
        )
        .options(
            selectinload(Content.tags)
        )
    )

    contents = result.scalars().all()

    return contents

@router.delete("/content/{content_id}")
def delete_content(
    content_id: int,
    current_user: Annotated[
        User,
        Depends(get_current_user)
    ],
    db: Annotated[
        Session,
        Depends(get_db)
    ]
):
    # delete the contents with content_id and also of the current user only,
    content = db.execute(
        select(Content).where(
            Content.id == content_id,
            Content.user_id == current_user.id
        )
    ).scalar_one_or_none()

    if content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Content not found or you don't "
                "have permission to delete it"
            )
        )

    db.delete(content)
    db.commit()

    return {
        "message": "Content deleted successfully"
    }

@router.get(
    "/tags",
    response_model=list[TagResponse]
)
def get_tags(
    db: Annotated[
        Session,
        Depends(get_db)
    ]
):

    result = db.execute(
        select(Tag).order_by(
            Tag.name
        )
    )

    tags = result.scalars().all()

    return tags


'''
{
    "tags": [
        "python",
        "backend",
        "fastapi"
    ]
}
'''
@router.post("/tags", response_model=TagsResponse, status_code = status.HTTP_201_CREATED)
def create_tags(tag_data: TagsCreate,

    db: Annotated[
        Session,
        Depends(get_db)
    ]):
    
    created_tags = []
    for tag_name in tag_data.tags:
        tag_name = tag_name.strip()
        if not tag_name:
            continue

        existing_tag = db.execute(
            select(Tag).where(
                Tag.name == tag_name
            )
        ).scalar_one_or_none()

        if existing_tag:
            created_tags.append(existing_tag)
        else:

            new_tag = Tag(
                name=tag_name
            )

            db.add(new_tag)
            db.flush()
            created_tags.append(new_tag)

    db.commit()

    return {
        "message": "Tags created/updated successfully.",
        "tags": created_tags
    }
        