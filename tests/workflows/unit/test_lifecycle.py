from runtime.workflows.lifecycle import WorkflowLifecycle, WorkflowStatus


def test_initial_state() -> None:
    lc = WorkflowLifecycle()
    lc.initialize("wf-1")
    assert lc.state_of("wf-1") == WorkflowStatus.CREATED


def test_transition_validated() -> None:
    lc = WorkflowLifecycle()
    lc.initialize("wf-1")
    lc.transition("wf-1", WorkflowStatus.VALIDATED)
    assert lc.state_of("wf-1") == WorkflowStatus.VALIDATED


def test_transition_ready() -> None:
    lc = WorkflowLifecycle()
    lc.initialize("wf-1")
    lc.transition("wf-1", WorkflowStatus.VALIDATED)
    lc.transition("wf-1", WorkflowStatus.READY)
    assert lc.state_of("wf-1") == WorkflowStatus.READY


def test_transition_running() -> None:
    lc = WorkflowLifecycle()
    lc.initialize("wf-1")
    lc.transition("wf-1", WorkflowStatus.VALIDATED)
    lc.transition("wf-1", WorkflowStatus.READY)
    lc.transition("wf-1", WorkflowStatus.RUNNING)
    assert lc.state_of("wf-1") == WorkflowStatus.RUNNING


def test_transition_completed() -> None:
    lc = WorkflowLifecycle()
    lc.initialize("wf-1")
    lc.transition("wf-1", WorkflowStatus.VALIDATED)
    lc.transition("wf-1", WorkflowStatus.READY)
    lc.transition("wf-1", WorkflowStatus.RUNNING)
    lc.transition("wf-1", WorkflowStatus.COMPLETED)
    assert lc.state_of("wf-1") == WorkflowStatus.COMPLETED


def test_transition_failed() -> None:
    lc = WorkflowLifecycle()
    lc.initialize("wf-1")
    lc.transition("wf-1", WorkflowStatus.FAILED)
    assert lc.state_of("wf-1") == WorkflowStatus.FAILED


def test_transition_stopped() -> None:
    lc = WorkflowLifecycle()
    lc.initialize("wf-1")
    lc.transition("wf-1", WorkflowStatus.VALIDATED)
    lc.transition("wf-1", WorkflowStatus.READY)
    lc.transition("wf-1", WorkflowStatus.RUNNING)
    lc.transition("wf-1", WorkflowStatus.STOPPED)
    assert lc.state_of("wf-1") == WorkflowStatus.STOPPED


def test_invalid_transition_raises() -> None:
    lc = WorkflowLifecycle()
    lc.initialize("wf-1")
    try:
        lc.transition("wf-1", WorkflowStatus.RUNNING)
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_can_transition() -> None:
    lc = WorkflowLifecycle()
    lc.initialize("wf-1")
    assert lc.can_transition("wf-1", WorkflowStatus.VALIDATED) is True
    assert lc.can_transition("wf-1", WorkflowStatus.RUNNING) is False


def test_failed_can_restart() -> None:
    lc = WorkflowLifecycle()
    lc.initialize("wf-1")
    lc.transition("wf-1", WorkflowStatus.FAILED)
    assert lc.can_transition("wf-1", WorkflowStatus.CREATED) is True


def test_history() -> None:
    lc = WorkflowLifecycle()
    lc.initialize("wf-1")
    lc.transition("wf-1", WorkflowStatus.VALIDATED)
    assert len(lc.history) == 2
