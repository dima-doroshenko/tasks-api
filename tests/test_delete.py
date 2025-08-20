import pytest
import httpx

from tests.helpers import create_task, delete_task, unique_title


@pytest.mark.asyncio
async def test_delete_task_success(client: httpx.AsyncClient):
    created = await create_task(client, unique_title("delete"))
    r = await delete_task(client, created["id"])
    assert r.status_code == 204, r.text