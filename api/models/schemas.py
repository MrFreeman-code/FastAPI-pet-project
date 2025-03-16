# Для описания OpenAPI
from typing import Optional
from pydantic import BaseModel, ConfigDict


# Входная модель. Создаем класс с TaskAdd, который наследуем от BaseModel
class TaskAdd(BaseModel):
    name: str
    description: Optional[str] = None


# Модель ответа при успешной загрузке данных в БД
class TaskId(BaseModel):
    ok: bool = True
    task_id: int


# Создаем TasksOut (выходная модель), которая будет наследовать все поля от класса TaskAdd + поле id
class TasksOut(TaskAdd):
    id: int
    # Когда хотим из SQLAlchemy модели преобразовать ее в схему.
    # Тк это не словарик, а прям экземпляр класса SQLAlchemy нужно добавить конфигурацию,
    # связанную с pydantic. Те указываем поробуй не только как словарик распарсить этот объект,
    # но и как экземпляр класса из атребутов его достань все свойства
    model_config = ConfigDict(from_attributes=True)
