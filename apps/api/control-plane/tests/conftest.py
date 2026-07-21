import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infrastructure.database.base import Base


@pytest.fixture
def db_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()
