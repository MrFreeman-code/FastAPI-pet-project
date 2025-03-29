from fastapi import APIRouter

from api.routers.task import router as task_router
from api.routers.auth import router as auth_router

routers = APIRouter()

routers.include_router(task_router)
routers.include_router(auth_router)