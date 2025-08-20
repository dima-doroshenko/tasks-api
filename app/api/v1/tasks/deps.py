from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dep import get_db

from .repo import TaskRepository
from .service import TaskService


def get_task_repo(session: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(session=session)


def get_task_service(
    repo: TaskRepository = Depends(get_task_repo),
) -> TaskService:
    return TaskService(repo=repo)
