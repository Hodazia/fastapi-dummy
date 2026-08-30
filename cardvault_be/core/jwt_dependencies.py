from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database.dependencies import get_db
from database.models import User
from core.security import decode_access_token

'''
Think of OAuth2PasswordBearer as:
"FastAPI, whenever I depend on oauth2_scheme, go look for a Bearer token in the Authorization header."

For example, client sends: Authorization: Bearer abc123

FastAPI extracts: abc123
and gives it to us.

So:
token: Annotated[str, Depends(oauth2_scheme)]
essentially means:

Get the token from:
Authorization: Bearer <token>

and put that token into the variable:
token


'''
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)

'''
Depends() , before calling the get_current_user function, it will first call the oauth2_scheme function to get the 
token from the Authorization header.

Given the JWT from the request, figure out which user is making the request.
'''

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:

    # if jwt is invalid, we will raise this exception and the client will get a 401 Unauthorized response
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    try:

        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (Exception, ValueError):
        raise credentials_exception

    user = db.get(User, user_id)

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user