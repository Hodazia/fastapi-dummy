from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database.dependencies import get_db

from schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse
)

from services.user_service import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


'''
POST    /users
GET     /users
GET     /users/{user_id}
PUT     /users/{user_id}
DELETE  /users/{user_id}
'''
@router.post("",response_model=UserResponse)
def create_new_user(
    payload: UserCreate,
    db: Session = Depends(get_db) # what is this depends(get_db) ??
):

    try:
        return create_user(
            db,
            payload
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("",response_model=list[UserResponse])
def fetch_users(
    db: Session = Depends(get_db)
):
    return get_users(db)

@router.get("/{user_id}",response_model=UserResponse)
def fetch_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_user(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.put( "/{user_id}",response_model=UserResponse)
def edit_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db)
):

    user = update_user(
        db,
        user_id,
        payload
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.delete("/{user_id}")
def remove_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_user(
        db,
        user_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }