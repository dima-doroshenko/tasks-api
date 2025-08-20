import uuid
from typing import Optional

from fastapi import Depends

from app.exc import NotFoundError

from .models import Task
from .models import TaskStatus
from .repo import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create_task(self, /, title: str, description: str | None) -> Task:
        return await self.repo.create(title=title, description=description)

    async def get_task(self, task_id: uuid.UUID) -> Task:
        if not (task := await self.repo.get_by_id(task_id)):
            raise NotFoundError
        return task

    async def list_tasks(
        self,
        *,
        status: TaskStatus | None,
        search: str | None,
    ) -> tuple[list[Task], int]:
        return await self.repo.list(status=status, search=search)

    async def update_task(
        self,
        task_id: uuid.UUID,
        /,
        title: str | None,
        description: str | None,
        status: TaskStatus | None,
    ) -> Task:
        task = await self.get_task(task_id=task_id)
        return await self.repo.update(
            task, title=title, description=description, status=status
        )

    async def delete_task(self, task_id: uuid.UUID) -> None:
        task = await self.get_task(task_id=task_id)
        await self.repo.delete(task)
