import uuid

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi import status

from app.api.v1.tasks.deps import get_task_service
from app.exc import NotFoundError

from .models import TaskStatus
from .schemas import TaskCreate
from .schemas import TaskList
from .schemas import TaskRead
from .schemas import TaskUpdate
from .service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    payload: TaskCreate, service: TaskService = Depends(get_task_service)
):
    task = await service.create_task(
        title=payload.title, description=payload.description
    )
    return task


@router.get(
    "/{task_id}",
    response_model=TaskRead,
)
async def get_task_by_id(
    task_id: uuid.UUID, service: TaskService = Depends(get_task_service)
):
    try:
        return await service.get_task(task_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )


@router.get(
    "",
    response_model=TaskList,
)
async def tasks_list(
    status: TaskStatus | None = Query(default=None),
    search: str | None = Query(default=None),
    service: TaskService = Depends(get_task_service),
):
    items, total = await service.list_tasks(status=status, search=search)
    return TaskList(items=items, total=total)


@router.put(
    "/{task_id}",
    response_model=TaskRead,
)
async def update_task(
    task_id: uuid.UUID,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    try:
        return await service.update_task(
            task_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
        )
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: uuid.UUID, service: TaskService = Depends(get_task_service)
):
    try:
        await service.delete_task(task_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
