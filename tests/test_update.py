import asyncio
import pytest
import httpx

from tests.helpers import (
    create_task,
    update_task,
    assert_task_read_shape,
    unique_title,
)


@pytest.mark.asyncio
async def test_update_task_success(client: httpx.AsyncClient):
    title = unique_title("update")
    created = await create_task(client, title, "before")
    task_id = created["id"]

    new_title = f"{title}-updated"
    new_desc = "after"
    new_status = "in_progress"

    await asyncio.sleep(0.1)

    r = await update_task(
        client,
        task_id,
        {"title": new_title, "description": new_desc, "status": new_status},
    )
    assert r.status_code == 200, r.text
    updated = r.json()
    assert_task_read_shape(
        updated,
        expected_title=new_title,
        expected_description=new_desc,
        expected_status=new_status,
    )


@pytest.mark.asyncio
async def test_update_task_validation_errors(client: httpx.AsyncClient):
    created = await create_task(client, unique_title("update-422"))
    task_id = created["id"]

    r1 = await update_task(client, task_id, {"title": ""})
    assert r1.status_code == 422, r1.text

    r2 = await update_task(client, task_id, {"status": "bad_status"})
    assert r2.status_code == 422, r2.text