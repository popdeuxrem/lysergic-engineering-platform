from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from src.config.settings import get_settings


def create_database_engine() -> Engine:
    settings = get_settings()
    url = (
        f"postgresql+psycopg://{settings.postgres_user}:"
        f"{settings.postgres_password}@{settings.postgres_host}:"
        f"{settings.postgres_port}/{settings.postgres_db}"
    )
    return create_engine(url, future=True)


def get_engine() -> Engine:
    return create_database_engine()
