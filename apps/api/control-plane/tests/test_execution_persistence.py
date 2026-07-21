import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.domain.execution import Execution
from src.domain.execution_status import ExecutionStatus
from src.infrastructure.database.base import Base
from src.infrastructure.database.execution_model import ExecutionModel
from src.infrastructure.database.execution_repository import SqlAlchemyExecutionRepository


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


def test_repository_saves_execution(db_session: Session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    execution = Execution()

    repo.save(execution)

    saved = db_session.get(ExecutionModel, execution.execution_id)
    assert saved is not None
    assert saved.id == execution.execution_id
    assert saved.status == ExecutionStatus.CREATED.value


def test_repository_retrieves_execution(db_session: Session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    execution = Execution()
    repo.save(execution)

    retrieved = repo.get_by_id(execution.execution_id)

    assert retrieved is not None
    assert retrieved.execution_id == execution.execution_id
    assert retrieved.status == ExecutionStatus.CREATED


def test_repository_returns_none_for_missing(db_session: Session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)

    result = repo.get_by_id("nonexistent-id")

    assert result is None


def test_repository_persists_status_transition(db_session: Session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    execution = Execution()
    repo.save(execution)

    execution.start()
    repo.save(execution)

    retrieved = repo.get_by_id(execution.execution_id)
    assert retrieved is not None
    assert retrieved.status == ExecutionStatus.RUNNING


def test_repository_persists_completed_state(db_session: Session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    execution = Execution()
    repo.save(execution)

    execution.start()
    execution.complete()
    repo.save(execution)

    retrieved = repo.get_by_id(execution.execution_id)
    assert retrieved is not None
    assert retrieved.status == ExecutionStatus.COMPLETED


def test_repository_persists_failed_state(db_session: Session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    execution = Execution()
    repo.save(execution)

    execution.start()
    execution.fail()
    repo.save(execution)

    retrieved = repo.get_by_id(execution.execution_id)
    assert retrieved is not None
    assert retrieved.status == ExecutionStatus.FAILED


def test_repository_updates_existing_record(db_session: Session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    execution = Execution()
    repo.save(execution)

    execution.start()
    repo.save(execution)

    records = db_session.query(ExecutionModel).all()
    assert len(records) == 1
    assert records[0].status == ExecutionStatus.RUNNING.value


def test_repository_round_trip_preserves_fields(db_session: Session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    execution = Execution()
    repo.save(execution)

    retrieved = repo.get_by_id(execution.execution_id)

    assert retrieved is not None
    assert retrieved.execution_id == execution.execution_id
    assert retrieved.created_at is not None
    assert retrieved.updated_at is not None
