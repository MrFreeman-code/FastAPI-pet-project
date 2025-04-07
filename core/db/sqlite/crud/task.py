from sqlalchemy import select
from core.db.sqlite.session import get_session
from core.db.sqlite.tables.task import TaskTable
from api.models.task import TaskAdd, TasksOut


# В классе создаем две функции: для добавления task и находжения всех tasks
class TaskRepository:
    @classmethod
    # создаем асинх функцию, в которую передаем параметры описанные в TaskAdd.
    # TaskAdd чтоб у нас сохранялась типизация и возвращаем task.id
    async def add_one_task(cls, data: TaskAdd) -> int:
        # создаем объект сессиии (session) к БД
        async with get_session() as session:
            # приводим data к виду словарика
            task_dict = data.model_dump()

            # в TaskTable предаем словарик task_dict, раскрытый (**task_dict)
            task = TaskTable(**task_dict)
            # добавляем объект task в сессию (эта синхронная операция, тк пока никакого ображаения к БД нет)
            session.add(task)
            # await - обращение к БД
            # flush еще не завершит транзакцию, еще не добавит строку, но только отправит изменения в БД и позволит вернуть id таски
            await session.flush()
            # тут сесиия все изменения, j в нее были добавлены через "add" отправляет в БД
            await session.commit()
            # возвращаем id таски
            return task.id


    @classmethod
    async def get_all_tasks(cls,
                            limit: int,
                            offset: int) -> list[TasksOut]:
        async with get_session() as session:
            query = select(TaskTable).limit(limit).offset(offset)
            # обратись (await) к БД через ссессию (session), исполнив (execute) запрос (query)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [TasksOut.model_validate(task_model) for task_model in task_models]
            return task_schemas