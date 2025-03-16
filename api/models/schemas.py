from typing import Optional
from pydantic import BaseModel, ConfigDict


# Для описания нашего OpenAPI, в данном случае, что он возвращает.
# Создаем класс с Tack, который наследуем от BaseModel
class TaskAdd(BaseModel):
    name: str # обязательное поле name
    description: Optional[str] = None # опциональное (необязательное) поле description


# Создаем TasksGet, которая будет наследовать все поля от класса TaskAdd + поле id
class TasksOut(TaskAdd):
    id: int
    # Когда хотим из SQLAlchemy модели преобразовать ее в схему.
    # Тк это не словарик, а прям экземпляр класса SQLAlchemy нужно добавить конфигурацию,
    # связанную с pydantic. Те указываем поробуй не только как словарик распарсить этот объект,
    # но и как экземпляр класса из атребутов его достань все свойства
    model_config = ConfigDict(from_attributes=True)


class TaskId(BaseModel):
    ok: bool = True
    task_id: int