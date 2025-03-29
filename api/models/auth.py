from pydantic import BaseModel


# Модель пользователя
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


# Пароль пользователя в виде hashed в fake_users_db
class UserInDB(User):
    hashed_password: str