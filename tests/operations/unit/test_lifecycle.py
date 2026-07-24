from runtime.operations.lifecycle import OperationLifecycle, OperationLifecycleState


def test_initial() -> None:
    lc = OperationLifecycle()
    lc.initialize("op-1")
    assert lc.state_of("op-1") == OperationLifecycleState.CREATED


def test_full_path() -> None:
    lc = OperationLifecycle()
    lc.initialize("op-1")
    lc.transition("op-1", OperationLifecycleState.DEFINED)
    lc.transition("op-1", OperationLifecycleState.VALIDATED)
    lc.transition("op-1", OperationLifecycleState.READY)
    lc.transition("op-1", OperationLifecycleState.EXECUTING)
    lc.transition("op-1", OperationLifecycleState.COMPLETED)
    assert lc.state_of("op-1") == OperationLifecycleState.COMPLETED


def test_archive_restore() -> None:
    lc = OperationLifecycle()
    lc.initialize("op-1")
    lc.transition("op-1", OperationLifecycleState.ARCHIVED)
    assert lc.state_of("op-1") == OperationLifecycleState.ARCHIVED
    lc.transition("op-1", OperationLifecycleState.CREATED)
    assert lc.state_of("op-1") == OperationLifecycleState.CREATED


def test_failed_retry() -> None:
    lc = OperationLifecycle()
    lc.initialize("op-1")
    lc.transition("op-1", OperationLifecycleState.FAILED)
    lc.transition("op-1", OperationLifecycleState.CREATED)
    assert lc.state_of("op-1") == OperationLifecycleState.CREATED


def test_invalid_raises() -> None:
    lc = OperationLifecycle()
    lc.initialize("op-1")
    try:
        lc.transition("op-1", OperationLifecycleState.EXECUTING)
        assert False
    except Exception:
        pass


def test_can_transition() -> None:
    lc = OperationLifecycle()
    lc.initialize("op-1")
    assert lc.can_transition("op-1", OperationLifecycleState.DEFINED) is True
    assert lc.can_transition("op-1", OperationLifecycleState.COMPLETED) is False


def test_history() -> None:
    lc = OperationLifecycle()
    lc.initialize("op-1")
    lc.transition("op-1", OperationLifecycleState.DEFINED)
    assert len(lc.history) == 2
