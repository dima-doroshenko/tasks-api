import pytest
import httpx

from .helpers import create_task, TASKS_PATH, unique_title, STATUSES


@pytest.mark.asyncio
async def test_create_task_success(client: httpx.AsyncClient):
    title = unique_title("create-ok")
    description = "test description"
    data = await create_task(client, title, description)
    assert data["status"] in STATUSES


@pytest.mark.asyncio
async def test_create_task_validation_error_empty_title(client: httpx.AsyncClient):
    r = await client.post(TASKS_PATH, json={"title": ""})
    assert r.status_code == 422, r.text


@pytest.mark.asyncio
async def test_create_task_validation_error_title_too_long(client: httpx.AsyncClient):
    long_title = "x" * 256
    r = await client.post(TASKS_PATH, json={"title": long_title})
    assert r.status_code == 422, r.text