import pytest
import httpx

from tests.helpers import create_task, get_task, assert_task_read_shape, unique_title


@pytest.mark.asyncio
async def test_get_task_by_id_success(client: httpx.AsyncClient):
    title = unique_title("get-by-id")
    created = await create_task(client, title, "desc")
    r = await get_task(client, created["id"])
    assert r.status_code == 200, r.text
    got = r.json()
    assert_task_read_shape(got, expected_title=title)