# APIRouter — это класс из библиотеки FastAPI, который используется для организации и группировки маршрутов (routes)
# и позволяет выносить группу роутов в отедльный файл router и потом его перемещать в main.py (всего через одну строчку)
from fastapi import APIRouter, Depends
from api.models.schemas import TaskAdd, TasksOut, TaskId
from repository import TaskRepository
from typing import Annotated

# prefix у всей группы роутов будет одинаковый, и в tags прописываем название группый роутов
router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Добавляется async, тк работа с БД в асинхронном режиме и ф-ии тоже долны быть асинхронны
@router.post("")
async def add_task(
    task: Annotated[TaskAdd, Depends()]
) -> TaskId:
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}


@router.get("")
async def get_tasks() -> list[TasksOut]:
    tasks = await TaskRepository.find_all()
    return tasks