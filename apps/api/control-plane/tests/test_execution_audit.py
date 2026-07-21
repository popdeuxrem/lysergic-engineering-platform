from src.application.audit.handlers.execution_audit_handler import ExecutionAuditHandler
from src.domain.execution import Execution
from src.domain.execution_status import ExecutionStatus
from src.infrastructure.database.execution_repository import SqlAlchemyExecutionRepository


def test_audit_handler_returns_valid_for_created_execution(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    handler = ExecutionAuditHandler(repo)
    execution = Execution()
    repo.save(execution)

    result = handler.audit_by_id(execution.execution_id)

    assert result is not None
    assert result.valid is True
    assert len(result.issues) == 0
    assert result.execution_id == execution.execution_id
    assert result.status == ExecutionStatus.CREATED


def test_audit_handler_returns_valid_for_completed_execution(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    handler = ExecutionAuditHandler(repo)
    execution = Execution()
    repo.save(execution)
    execution.start()
    execution.complete()
    repo.save(execution)

    result = handler.audit_by_id(execution.execution_id)

    assert result is not None
    assert result.valid is True
    assert result.status == ExecutionStatus.COMPLETED


def test_audit_handler_returns_valid_for_failed_execution(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    handler = ExecutionAuditHandler(repo)
    execution = Execution()
    repo.save(execution)
    execution.start()
    execution.fail()
    repo.save(execution)

    result = handler.audit_by_id(execution.execution_id)

    assert result is not None
    assert result.valid is True
    assert result.status == ExecutionStatus.FAILED


def test_audit_handler_returns_none_for_missing_execution(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    handler = ExecutionAuditHandler(repo)

    result = handler.audit_by_id("nonexistent-id")

    assert result is None


def test_audit_does_not_mutate_execution(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    handler = ExecutionAuditHandler(repo)
    execution = Execution()
    repo.save(execution)
    original_status = execution.status

    handler.audit_by_id(execution.execution_id)

    retrieved = repo.get_by_id(execution.execution_id)
    assert retrieved.status == original_status


def test_audit_projection_has_required_fields(db_session) -> None:
    from pydantic import TypeAdapter
    from src.application.audit.execution_audit import ExecutionAuditProjection

    adapter = TypeAdapter(ExecutionAuditProjection)
    schema = adapter.json_schema()

    assert "execution_id" in schema["properties"]
    assert "status" in schema["properties"]
    assert "valid" in schema["properties"]
    assert "issues" in schema["properties"]


def test_audit_is_deterministic(db_session) -> None:
    repo = SqlAlchemyExecutionRepository(db_session)
    handler = ExecutionAuditHandler(repo)
    execution = Execution()
    repo.save(execution)

    result_a = handler.audit_by_id(execution.execution_id)
    result_b = handler.audit_by_id(execution.execution_id)

    assert result_a is not None
    assert result_b is not None
    assert result_a.valid == result_b.valid
    assert result_a.issues == result_b.issues


def test_audit_handler_uses_repository_only(db_session) -> None:
    import ast
    from pathlib import Path

    source = Path(__file__).parent.parent / "src" / "application" / "audit" / "handlers" / "execution_audit_handler.py"
    tree = ast.parse(source.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module:
                assert not node.module.startswith("sqlalchemy"), "Handler imports sqlalchemy"
