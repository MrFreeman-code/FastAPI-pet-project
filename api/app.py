from fastapi import FastAPI
from api.routers import routers
from contextlib import asynccontextmanager # asynccontextmanager — это декоратор из модуля contextlib в Python, который позволяет создавать асинхронные контекстные менеджеры.
from core.db.sqlite.session import create_tables, delete_tables

from starlette.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


# Теперь при запуске web-сервера, сначала удаляются все таблицы, а затем создаются все таблицы через lifespan.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # await тк у нас асинхронное создание
    await delete_tables()
    print("Drop table task")
    await create_tables()
    print("Create table task")
    yield
    print("Shutdown")

app = FastAPI(lifespan=lifespan)
app.include_router(routers)


#  Middleware в FastAPI (и Starlette) позволяет вам обрабатывать запросы и ответы, добавляя дополнительную логику, такую как аутентификация, логирование или, в данном случае, перенаправление.
class RedirectToDocsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/":
            return RedirectResponse(url="/docs")
        response = await call_next(request)
        return response


# Cтрока добавляет middleware RedirectToDocsMiddleware в приложение FastAPI, которое автоматически перенаправляет пользователей с корневого адреса на страницу документации FastAPI.
app.add_middleware(RedirectToDocsMiddleware)


# Параметры для запуска
args = {
    "host": "127.0.0.1",
    "port": 8080
    # ,"reload": True
}