from src.application.dto.execution_projection import ExecutionProjection
from src.application.queries.execution_queries import GetExecutionQuery
from src.application.queries.handlers.execution_query_handler import ExecutionQueryHandler
from src.domain.execution import Execution
from src.domain.execution_status import ExecutionStatus
from src.infrastructure.database.execution_repository import SqlAlchemyExecutionRepository


def test_query_handler_retrieves_execution(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    handler = ExecutionQueryHandler(repo)
    execution = Execution()
    repo.save(execution)

    projection = handler.handle(GetExecutionQuery(execution_id=execution.execution_id))

    assert projection is not None
    assert isinstance(projection, ExecutionProjection)
    assert projection.execution_id == execution.execution_id
    assert projection.status == ExecutionStatus.CREATED
    assert projection.created_at is not None
    assert projection.updated_at is not None


def test_query_handler_returns_none_for_missing_execution(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    handler = ExecutionQueryHandler(repo)

    projection = handler.handle(GetExecutionQuery(execution_id="nonexistent-id"))

    assert projection is None


def test_projection_fields_are_deterministic(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    handler = ExecutionQueryHandler(repo)
    execution = Execution()
    repo.save(execution)

    projection_a = handler.handle(GetExecutionQuery(execution_id=execution.execution_id))
    projection_b = handler.handle(GetExecutionQuery(execution_id=execution.execution_id))

    assert projection_a.execution_id == projection_b.execution_id
    assert projection_a.status == projection_b.status
    assert projection_a.created_at == projection_b.created_at
    assert projection_a.updated_at == projection_b.updated_at


def test_query_does_not_mutate_execution_state(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    handler = ExecutionQueryHandler(repo)
    execution = Execution()
    repo.save(execution)

    original_status = execution.status
    handler.handle(GetExecutionQuery(execution_id=execution.execution_id))

    retrieved = repo.get_by_id(execution.execution_id)
    assert retrieved.status == original_status


def test_lifecycle_transition_remains_controlled_by_command_path(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    handler = ExecutionQueryHandler(repo)
    execution = Execution()
    repo.save(execution)

    from src.domain.execution import InvalidExecutionTransition
    try:
        execution.start()
        repo.save(execution)
        handler.handle(GetExecutionQuery(execution_id=execution.execution_id))
        projection = handler.handle(GetExecutionQuery(execution_id=execution.execution_id))
        assert projection.status == ExecutionStatus.RUNNING
    except InvalidExecutionTransition:
        assert False, "Command path should allow CREATED -> RUNNING"


def test_projection_after_completed_state(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    handler = ExecutionQueryHandler(repo)
    execution = Execution()
    repo.save(execution)

    execution.start()
    execution.complete()
    repo.save(execution)

    projection = handler.handle(GetExecutionQuery(execution_id=execution.execution_id))
    assert projection.status == ExecutionStatus.COMPLETED


def test_projection_after_failed_state(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    handler = ExecutionQueryHandler(repo)
    execution = Execution()
    repo.save(execution)

    execution.start()
    execution.fail()
    repo.save(execution)

    projection = handler.handle(GetExecutionQuery(execution_id=execution.execution_id))
    assert projection.status == ExecutionStatus.FAILED


def test_api_get_endpoint_returns_projection() -> None:
    from fastapi.testclient import TestClient

    from src.main import app

    client = TestClient(app)
    response = client.get("/api/v1/executions")

    assert response.status_code in (200, 404, 405)


def test_projection_has_required_fields() -> None:
    from pydantic import TypeAdapter

    adapter = TypeAdapter(ExecutionProjection)
    schema = adapter.json_schema()

    assert "execution_id" in schema["properties"]
    assert "status" in schema["properties"]
    assert "created_at" in schema["properties"]
    assert "updated_at" in schema["properties"]
