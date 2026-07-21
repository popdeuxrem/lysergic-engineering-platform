from collections.abc import Generator
from functools import lru_cache

from sqlalchemy.orm import Session, sessionmaker

from src.infrastructure.database.engine import get_engine


@lru_cache
def _get_session_maker() -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def database_session() -> Generator[Session, None, None]:
    session = _get_session_maker()()
    try:
        yield session
    finally:
        session.close()


def create_session() -> Session:
    return _get_session_maker()()
