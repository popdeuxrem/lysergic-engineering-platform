from src.domain.execution import Execution, InvalidExecutionTransition
from src.domain.execution_status import ExecutionStatus


def test_execution_created_with_initial_state() -> None:
    execution = Execution()

    assert execution.status == ExecutionStatus.CREATED
    assert execution.execution_id is not None
    assert execution.created_at is not None
    assert execution.updated_at is not None


def test_execution_start_transition() -> None:
    execution = Execution()
    execution.start()

    assert execution.status == ExecutionStatus.RUNNING


def test_execution_complete_transition() -> None:
    execution = Execution()
    execution.start()
    execution.complete()

    assert execution.status == ExecutionStatus.COMPLETED


def test_execution_fail_transition() -> None:
    execution = Execution()
    execution.start()
    execution.fail()

    assert execution.status == ExecutionStatus.FAILED


def test_execution_rejects_created_to_completed() -> None:
    execution = Execution()

    try:
        execution.complete()
        assert False, "Should have raised InvalidExecutionTransition"
    except InvalidExecutionTransition:
        pass


def test_execution_rejects_completed_to_running() -> None:
    execution = Execution()
    execution.start()
    execution.complete()

    try:
        execution.start()
        assert False, "Should have raised InvalidExecutionTransition"
    except InvalidExecutionTransition:
        pass


def test_execution_rejects_failed_to_running() -> None:
    execution = Execution()
    execution.start()
    execution.fail()

    try:
        execution.start()
        assert False, "Should have raised InvalidExecutionTransition"
    except InvalidExecutionTransition:
        pass


def test_execution_created_at_is_set() -> None:
    execution = Execution()
    assert execution.created_at is not None


def test_execution_updated_at_changes_on_transition() -> None:
    execution = Execution()
    original_updated = execution.updated_at

    execution.start()
    assert execution.updated_at >= original_updated
