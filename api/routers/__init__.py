from fastapi import APIRouter

from api.routers.task import router as task_router

routers = APIRouter()

routers.include_router(task_router)