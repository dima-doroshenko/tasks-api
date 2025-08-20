from fastapi import APIRouter

from .tasks.router import router as tasks_router

v1_router = APIRouter(prefix="/v1")


v1_router.include_router(tasks_router)
