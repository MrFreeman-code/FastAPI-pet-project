from fastapi import FastAPI
# asynccontextmanager — это декоратор из модуля contextlib в Python, который позволяет создавать асинхронные контекстные менеджеры.
from contextlib import asynccontextmanager
from db import create_tables, delete_tables
from router import router as tasks_router


# Теперь при запуске web-сервера, сначала удаляются все таблицы, а затем создаются все таблицы через lifespan.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # await тк у нас асинхронное создание
    await delete_tables()
    print("БД очищена")
    await create_tables()
    print("БД создана и готова к работе")
    yield
    print("Выклюение")

app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)