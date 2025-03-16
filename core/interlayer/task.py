from core.db.sqlite.crud.task import TaskRepository


async def add_one_task(task):
    task_id = await TaskRepository.add_one_task(task)
    return  task_id


async def get_all_tasks():
    tasks = await TaskRepository.get_all_tasks()
    return  tasks