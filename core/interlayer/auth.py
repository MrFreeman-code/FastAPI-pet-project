from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api.models.auth import User, UserInDB

from core.db.auth_db.auth import fake_users_db


# Функция создания hash_password
def fake_hash_password(password: str):
    return "fakehashed" + password


# OAuth2 схема
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Функция для получения пользователя
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# Функция для создания токена
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials!",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


# Функция проверки токена
def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled == True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Inactive user")
    return current_user
