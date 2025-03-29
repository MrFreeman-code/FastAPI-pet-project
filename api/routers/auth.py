from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.models.auth import User, UserInDB

from core.db.auth_db.auth import fake_users_db
from core.interlayer.auth import fake_hash_password, get_current_active_user


router = APIRouter(prefix="", tags=["Auth"])


# Эндпоинт для получения токена
@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Получение инф из fake_users_db по username и password
    user_dict = fake_users_db.get(form_data.username)
    # если нет пользователя с таким username
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = UserInDB(**user_dict) # Передставить ключи и значения user_dict непосредственно в качестве аргументов ключ-значение, что эквивалентно:
    # UserInDB(
    #     username = user_dict["username"],
    #     email = user_dict["email"],
    #     full_name = user_dict["full_name"],
    #     disabled = user_dict["disabled"],
    #     hashed_password = user_dict["hashed_password"],
    # )
    # Создаем hash из password
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}


# Эндпоинт для защищенного ресурса
@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


# # Эндпоинт для защищенного ресурса
# @app.get("/users/me")
# async def read_users_me(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = User(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
