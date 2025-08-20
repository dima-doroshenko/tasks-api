import uuid

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from .models import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None


class TaskBase(TaskCreate):
    status: TaskStatus = TaskStatus.created


class TaskUpdate(TaskCreate):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    status: TaskStatus | None = None


class TaskRead(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    status: TaskStatus

    model_config = ConfigDict(from_attributes=True)


class TaskList(BaseModel):
    items: list[TaskRead]
    total: int
