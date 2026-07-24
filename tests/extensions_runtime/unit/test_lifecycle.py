from runtime.extensions.lifecycle import (
    ExtensionRuntimeLifecycle,
    RuntimeLifecycleState,
)


def test_initial_state() -> None:
    lc = ExtensionRuntimeLifecycle()
    lc.install("ext-1")
    assert lc.state_of("ext-1") == RuntimeLifecycleState.INSTALLED


def test_full_path() -> None:
    lc = ExtensionRuntimeLifecycle()
    lc.install("ext-1")
    lc.transition("ext-1", RuntimeLifecycleState.DISCOVERED)
    lc.transition("ext-1", RuntimeLifecycleState.VALIDATED)
    lc.transition("ext-1", RuntimeLifecycleState.LOADED)
    lc.transition("ext-1", RuntimeLifecycleState.INITIALIZED)
    lc.transition("ext-1", RuntimeLifecycleState.EXECUTING)
    lc.transition("ext-1", RuntimeLifecycleState.SHUTDOWN)
    assert lc.state_of("ext-1") == RuntimeLifecycleState.SHUTDOWN


def test_shutdown_to_remove() -> None:
    lc = ExtensionRuntimeLifecycle()
    lc.install("ext-1")
    lc.transition("ext-1", RuntimeLifecycleState.DISCOVERED)
    lc.transition("ext-1", RuntimeLifecycleState.VALIDATED)
    lc.transition("ext-1", RuntimeLifecycleState.LOADED)
    lc.transition("ext-1", RuntimeLifecycleState.INITIALIZED)
    lc.transition("ext-1", RuntimeLifecycleState.SHUTDOWN)
    lc.transition("ext-1", RuntimeLifecycleState.REMOVED)
    assert lc.state_of("ext-1") == RuntimeLifecycleState.REMOVED


def test_shutdown_to_install() -> None:
    lc = ExtensionRuntimeLifecycle()
    lc.install("ext-1")
    lc.transition("ext-1", RuntimeLifecycleState.DISCOVERED)
    lc.transition("ext-1", RuntimeLifecycleState.VALIDATED)
    lc.transition("ext-1", RuntimeLifecycleState.LOADED)
    lc.transition("ext-1", RuntimeLifecycleState.INITIALIZED)
    lc.transition("ext-1", RuntimeLifecycleState.SHUTDOWN)
    lc.transition("ext-1", RuntimeLifecycleState.INSTALLED)
    assert lc.state_of("ext-1") == RuntimeLifecycleState.INSTALLED


def test_failed_retry() -> None:
    lc = ExtensionRuntimeLifecycle()
    lc.install("ext-1")
    lc.transition("ext-1", RuntimeLifecycleState.FAILED)
    lc.transition("ext-1", RuntimeLifecycleState.INSTALLED)
    assert lc.state_of("ext-1") == RuntimeLifecycleState.INSTALLED


def test_invalid_transition_raises() -> None:
    lc = ExtensionRuntimeLifecycle()
    lc.install("ext-1")
    try:
        lc.transition("ext-1", RuntimeLifecycleState.EXECUTING)
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_can_transition() -> None:
    lc = ExtensionRuntimeLifecycle()
    lc.install("ext-1")
    assert lc.can_transition("ext-1", RuntimeLifecycleState.DISCOVERED) is True
    assert lc.can_transition("ext-1", RuntimeLifecycleState.EXECUTING) is False


def test_history() -> None:
    lc = ExtensionRuntimeLifecycle()
    lc.install("ext-1")
    lc.transition("ext-1", RuntimeLifecycleState.DISCOVERED)
    assert len(lc.history) == 2
