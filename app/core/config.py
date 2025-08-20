from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASEDIR = Path(__file__).resolve().parent.parent


class Database(BaseModel):
    url: str = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"


class App(BaseModel):
    title: str = "Tasks API"
    version: str = "0.1"
    debug: bool = True


class Config(BaseSettings):
    app: App = App()
    db: Database = Database()


config = Config()
