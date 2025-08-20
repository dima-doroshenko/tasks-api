from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.core.config import config
from app.core.database import Base
from app.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=config.app.title,
    version=config.app.version,
    debug=config.app.debug,
    lifespan=lifespan,
)

app.include_router(api_router)
