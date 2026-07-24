from runtime.ai.lifecycle import AgentLifecycle, AgentLifecycleState


def test_initial_state() -> None:
    lc = AgentLifecycle()
    lc.initialize("a-1")
    assert lc.state_of("a-1") == AgentLifecycleState.CREATED


def test_full_path() -> None:
    lc = AgentLifecycle()
    lc.initialize("a-1")
    lc.transition("a-1", AgentLifecycleState.REGISTERED)
    lc.transition("a-1", AgentLifecycleState.VALIDATED)
    lc.transition("a-1", AgentLifecycleState.READY)
    lc.transition("a-1", AgentLifecycleState.RUNNING)
    lc.transition("a-1", AgentLifecycleState.STOPPED)
    assert lc.state_of("a-1") == AgentLifecycleState.STOPPED


def test_pause_resume() -> None:
    lc = AgentLifecycle()
    lc.initialize("a-1")
    lc.transition("a-1", AgentLifecycleState.REGISTERED)
    lc.transition("a-1", AgentLifecycleState.VALIDATED)
    lc.transition("a-1", AgentLifecycleState.READY)
    lc.transition("a-1", AgentLifecycleState.RUNNING)
    lc.transition("a-1", AgentLifecycleState.PAUSED)
    assert lc.state_of("a-1") == AgentLifecycleState.PAUSED
    lc.transition("a-1", AgentLifecycleState.RUNNING)
    assert lc.state_of("a-1") == AgentLifecycleState.RUNNING


def test_archive() -> None:
    lc = AgentLifecycle()
    lc.initialize("a-1")
    lc.transition("a-1", AgentLifecycleState.ARCHIVED)
    assert lc.state_of("a-1") == AgentLifecycleState.ARCHIVED


def test_failed_retry() -> None:
    lc = AgentLifecycle()
    lc.initialize("a-1")
    lc.transition("a-1", AgentLifecycleState.FAILED)
    lc.transition("a-1", AgentLifecycleState.CREATED)
    assert lc.state_of("a-1") == AgentLifecycleState.CREATED


def test_invalid_transition_raises() -> None:
    lc = AgentLifecycle()
    lc.initialize("a-1")
    try:
        lc.transition("a-1", AgentLifecycleState.RUNNING)
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_can_transition() -> None:
    lc = AgentLifecycle()
    lc.initialize("a-1")
    assert lc.can_transition("a-1", AgentLifecycleState.REGISTERED) is True
    assert lc.can_transition("a-1", AgentLifecycleState.RUNNING) is False


def test_history() -> None:
    lc = AgentLifecycle()
    lc.initialize("a-1")
    lc.transition("a-1", AgentLifecycleState.REGISTERED)
    assert len(lc.history) == 2
