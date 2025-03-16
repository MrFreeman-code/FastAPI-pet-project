import uvicorn
from fastapi import FastAPI
# asynccontextmanager — это декоратор из модуля contextlib в Python, который позволяет создавать асинхронные контекстные менеджеры.
from api.routers.router import router as tasks_router
from contextlib import asynccontextmanager
from db import create_tables, delete_tables

from starlette.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

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


#  Middleware в FastAPI (и Starlette) позволяет вам обрабатывать запросы и ответы, добавляя дополнительную логику, такую как аутентификация, логирование или, в данном случае, перенаправление.
class RedirectToDocsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/":
            return RedirectResponse(url="/docs")
        response = await call_next(request)
        return response


# Cтрока добавляет middleware RedirectToDocsMiddleware в приложение FastAPI, которое автоматически перенаправляет пользователей с корневого адреса на страницу документации FastAPI.
app.add_middleware(RedirectToDocsMiddleware)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)