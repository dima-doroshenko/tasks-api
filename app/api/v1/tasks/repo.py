import uuid

from sqlalchemy import func, update
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Task
from .models import TaskStatus


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, /, title: str, description: str | None) -> Task:
        task = Task(title=title, description=description)
        self.session.add(task)
        await self.session.flush()
        return task

    async def get_by_id(self, task_id: uuid.UUID) -> Task | None:
        return await self.session.get(Task, task_id)

    async def list(
        self,
        /,
        status: TaskStatus | None = None,
        search: str | None = None,
    ) -> tuple[list[Task], int]:
        filters = []
        if status:
            filters.append(Task.status == status)
        if search:
            ilike = f"%{search.lower()}%"
            filters.append(
                (func.lower(Task.title).like(ilike))
                | (func.lower(Task.description).like(ilike))
            )

        q = select(Task).where(*filters).order_by(Task.created_at.desc())
        items = list(await self.session.scalars(q))
        return items, len(items)

    async def update(
        self,
        task: Task,
        /,
        title: str | None = None,
        description: str | None = None,
        status: TaskStatus | None = None,
    ) -> Task:
        update_dict = {
            "title": title,
            "description": description,
            "status": status,
        }
        stmt = (
            update(Task)
            .values({k: v for k, v in update_dict.items() if v})
            .returning(Task)
        )
        return await self.session.scalar(stmt)

    async def delete(self, task: Task) -> None:
        await self.session.delete(task)
