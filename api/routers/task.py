# APIRouter — это класс из библиотеки FastAPI, который используется для организации и группировки маршрутов (routes)
# и позволяет выносить группу роутов в отедльный файл router и потом его перемещать в main.py (всего через одну строчку)
from fastapi import APIRouter, Depends, status

from typing import Annotated
from core.interlayer import task as t
from api.models.task import TaskAdd, TaskId, TasksOut

from api.models.auth import User
from core.interlayer.auth import get_current_active_user

# prefix у всей группы роутов будет одинаковый, и в tags прописываем название группый роутов
router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Добавляется async, тк работа с БД в асинхронном режиме и ф-ии тоже долны быть асинхронны
@router.post("/add", summary="Создать таску")
async def add_one_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task: Annotated[TaskAdd, Depends()]
) -> TaskId:
    task_id = await t.add_one_task(task)
    return {"ok": True, "task_id": task_id}


@router.get("/get-all", summary="Получить все таски")
async def get_all_tasks(
    #current_user: Annotated[User, Depends(get_current_active_user)]
) -> list[TasksOut]:
    tasks = await t.get_all_tasks()
    return tasks


@router.get("/rout-for-tests", summary="Роут для тестирования разными способами!")
async def rout_for_tests(
) -> list:
    tasks = []
    return tasks