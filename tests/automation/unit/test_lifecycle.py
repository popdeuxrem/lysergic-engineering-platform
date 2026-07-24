from runtime.automation.lifecycle import AutomationLifecycle, AutomationLifecycleState


def test_initial_state() -> None:
    lc = AutomationLifecycle()
    lc.initialize("a-1")
    assert lc.state_of("a-1") == AutomationLifecycleState.CREATED


def test_full_path() -> None:
    lc = AutomationLifecycle()
    lc.initialize("a-1")
    lc.transition("a-1", AutomationLifecycleState.VALIDATED)
    lc.transition("a-1", AutomationLifecycleState.READY)
    lc.transition("a-1", AutomationLifecycleState.ENABLED)
    lc.transition("a-1", AutomationLifecycleState.EXECUTING)
    lc.transition("a-1", AutomationLifecycleState.ENABLED)
    lc.transition("a-1", AutomationLifecycleState.DISABLED)
    assert lc.state_of("a-1") == AutomationLifecycleState.DISABLED


def test_enable_disable_idempotent() -> None:
    lc = AutomationLifecycle()
    lc.initialize("a-1")
    lc.transition("a-1", AutomationLifecycleState.VALIDATED)
    lc.transition("a-1", AutomationLifecycleState.READY)
    lc.transition("a-1", AutomationLifecycleState.ENABLED)
    lc.transition("a-1", AutomationLifecycleState.DISABLED)
    lc.transition("a-1", AutomationLifecycleState.ENABLED)
    assert lc.state_of("a-1") == AutomationLifecycleState.ENABLED


def test_archive() -> None:
    lc = AutomationLifecycle()
    lc.initialize("a-1")
    lc.transition("a-1", AutomationLifecycleState.ARCHIVED)
    assert lc.state_of("a-1") == AutomationLifecycleState.ARCHIVED


def test_failed_retry() -> None:
    lc = AutomationLifecycle()
    lc.initialize("a-1")
    lc.transition("a-1", AutomationLifecycleState.FAILED)
    lc.transition("a-1", AutomationLifecycleState.CREATED)
    assert lc.state_of("a-1") == AutomationLifecycleState.CREATED


def test_invalid_transition_raises() -> None:
    lc = AutomationLifecycle()
    lc.initialize("a-1")
    try:
        lc.transition("a-1", AutomationLifecycleState.EXECUTING)
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_can_transition() -> None:
    lc = AutomationLifecycle()
    lc.initialize("a-1")
    assert lc.can_transition("a-1", AutomationLifecycleState.VALIDATED) is True
    assert lc.can_transition("a-1", AutomationLifecycleState.EXECUTING) is False


def test_history() -> None:
    lc = AutomationLifecycle()
    lc.initialize("a-1")
    lc.transition("a-1", AutomationLifecycleState.VALIDATED)
    assert len(lc.history) == 2
