from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from .models import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None


class TaskBase(TaskCreate):
    status: TaskStatus = TaskStatus.created


class TaskUpdate(TaskCreate):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    status: TaskStatus | None = None


class TaskRead(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskList(BaseModel):
    items: list[TaskRead]
    total: int
