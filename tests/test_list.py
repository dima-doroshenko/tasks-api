import pytest
import httpx

from tests.helpers import create_task, update_task, TASKS_PATH, unique_title


@pytest.mark.asyncio
async def test_tasks_list_filters_and_search(client: httpx.AsyncClient):
    t_created = await create_task(client, unique_title("alpha"))
    t_in_progress = await create_task(client, unique_title("beta"))
    t_completed = await create_task(client, unique_title("gamma"))

    r1 = await update_task(client, t_in_progress["id"], {"status": "in_progress"})
    assert r1.status_code == 200, r1.text
    r2 = await update_task(client, t_completed["id"], {"status": "completed"})
    assert r2.status_code == 200, r2.text

    r_all = await client.get(TASKS_PATH)
    assert r_all.status_code == 200, r_all.text
    body_all = r_all.json()
    assert isinstance(body_all.get("items"), list)
    assert isinstance(body_all.get("total"), int)
    assert len(body_all["items"]) <= body_all["total"]

    r_created = await client.get(TASKS_PATH, params={"status": "created"})
    assert r_created.status_code == 200, r_created.text
    list_created = r_created.json()
    assert all(item["status"] == "created" for item in list_created["items"])
    assert any(item["id"] == t_created["id"] for item in list_created["items"])

    r_inp = await client.get(TASKS_PATH, params={"status": "in_progress"})
    assert r_inp.status_code == 200, r_inp.text
    list_inp = r_inp.json()
    assert all(item["status"] == "in_progress" for item in list_inp["items"])
    assert any(item["id"] == t_in_progress["id"] for item in list_inp["items"])

    r_comp = await client.get(TASKS_PATH, params={"status": "completed"})
    assert r_comp.status_code == 200, r_comp.text
    list_comp = r_comp.json()
    assert all(item["status"] == "completed" for item in list_comp["items"])
    assert any(item["id"] == t_completed["id"] for item in list_comp["items"])

    r_search = await client.get(TASKS_PATH, params={"search": t_created["title"]})
    assert r_search.status_code == 200, r_search.text
    list_search = r_search.json()
    assert any(item["id"] == t_created["id"] for item in list_search["items"])