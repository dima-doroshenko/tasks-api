import os
import httpx
import pytest
import pytest_asyncio

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")
TASKS_PATH = "/api/v1/tasks"


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest_asyncio.fixture
async def client(base_url: str):
    async with httpx.AsyncClient(base_url=base_url) as c:
        yield c