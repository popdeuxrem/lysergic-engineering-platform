from collections.abc import Generator
from functools import lru_cache

from sqlalchemy.orm import Session, sessionmaker

from src.infrastructure.database.engine import get_engine


@lru_cache
def _get_session_maker() -> sessionmaker[Session]:
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def _make_session() -> Session:
    maker = _get_session_maker()
    session: Session = maker()
    return session


def database_session() -> Generator[Session, None, None]:
    session = _make_session()
    try:
        yield session
    finally:
        session.close()


def create_session() -> Session:
    return _make_session()
