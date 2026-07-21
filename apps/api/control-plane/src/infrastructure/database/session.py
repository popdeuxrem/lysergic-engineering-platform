from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker

from src.infrastructure.database.engine import get_engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def database_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
