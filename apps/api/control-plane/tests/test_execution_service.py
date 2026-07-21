from src.application.execution_service import ExecutionService
from src.domain.execution_status import ExecutionStatus
from src.infrastructure.database.execution_repository import SqlAlchemyExecutionRepository


def test_service_creates_execution(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    service = ExecutionService(repo)

    result = service.create()

    assert result.execution_id is not None
    assert result.status == ExecutionStatus.CREATED


def test_service_gets_execution(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    service = ExecutionService(repo)

    created = service.create()
    result = service.get(created.execution_id)

    assert result.execution_id == created.execution_id
    assert result.status == ExecutionStatus.CREATED


def test_service_transitions_execution(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    service = ExecutionService(repo)

    created = service.create()
    service.transition(created.execution_id, ExecutionStatus.RUNNING)
    result = service.get(created.execution_id)

    assert result.status == ExecutionStatus.RUNNING


def test_service_completes_execution(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    service = ExecutionService(repo)

    created = service.create()
    service.transition(created.execution_id, ExecutionStatus.RUNNING)
    service.transition(created.execution_id, ExecutionStatus.COMPLETED)
    result = service.get(created.execution_id)

    assert result.status == ExecutionStatus.COMPLETED


def test_service_fails_execution(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    service = ExecutionService(repo)

    created = service.create()
    service.transition(created.execution_id, ExecutionStatus.RUNNING)
    service.transition(created.execution_id, ExecutionStatus.FAILED)
    result = service.get(created.execution_id)

    assert result.status == ExecutionStatus.FAILED


def test_service_rejects_invalid_transition(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    service = ExecutionService(repo)

    created = service.create()

    from src.domain.execution import InvalidExecutionTransition
    try:
        service.transition(created.execution_id, ExecutionStatus.COMPLETED)
        assert False, "Should have raised InvalidExecutionTransition"
    except InvalidExecutionTransition:
        pass


def test_service_returns_error_for_missing_execution(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    service = ExecutionService(repo)

    from src.application.exceptions import ServiceError
    try:
        service.get("nonexistent-id")
        assert False, "Should have raised ServiceError"
    except ServiceError:
        pass


def test_service_uses_same_repository_for_all_operations(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    service = ExecutionService(repo)

    created = service.create()
    service.transition(created.execution_id, ExecutionStatus.RUNNING)
    result = service.get(created.execution_id)

    assert result.status == ExecutionStatus.RUNNING
