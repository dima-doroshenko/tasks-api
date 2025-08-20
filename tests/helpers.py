import uuid
from typing import Any, Dict, Optional

import httpx

TASKS_PATH = "/api/v1/tasks"
STATUSES = {"created", "in_progress", "completed"}


def is_uuid_like(value: Any) -> bool:
    try:
        uuid.UUID(str(value))
        return True
    except Exception:
        return False


def assert_task_read_shape(
    task: dict[str, Any],
    *,
    expected_title: str | None = None,
    expected_description: str | None = None,
    expected_status: str | None = None,
) -> None:
    assert isinstance(task.get("id"), str) and is_uuid_like(task["id"])
    assert isinstance(task.get("title"), str)
    assert task.get("status") in STATUSES
    assert isinstance(task.get("created_at"), str)
    assert isinstance(task.get("updated_at"), str)

    if "description" in task:
        assert (task["description"] is None) or isinstance(task["description"], str)

    if expected_title is not None:
        assert task["title"] == expected_title

    if expected_description is not None:
        assert task.get("description") == expected_description

    if expected_status is not None:
        assert task["status"] == expected_status


async def create_task(
    client: httpx.AsyncClient, title: str, description: Optional[str] = None
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"title": title}
    if description is not None:
        payload["description"] = description
    r = await client.post(TASKS_PATH, json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert_task_read_shape(data, expected_title=title, expected_description=description)
    return data


async def get_task(client: httpx.AsyncClient, task_id: str) -> httpx.Response:
    return await client.get(f"{TASKS_PATH}/{task_id}")


async def update_task(
    client: httpx.AsyncClient, task_id: str, payload: Dict[str, Any]
) -> httpx.Response:
    return await client.put(f"{TASKS_PATH}/{task_id}", json=payload)


async def delete_task(client: httpx.AsyncClient, task_id: str) -> httpx.Response:
    return await client.delete(f"{TASKS_PATH}/{task_id}")


def unique_title(prefix: str = "task") -> str:
    return f"{prefix}-{uuid.uuid4()}"