from runtime.kernel.lifecycle import LifecycleManager, LifecycleState


def test_initial_state_is_created() -> None:
    lm = LifecycleManager()
    assert lm.state == LifecycleState.CREATED


def test_start_transitions_to_ready() -> None:
    lm = LifecycleManager()
    lm.start()
    assert lm.state == LifecycleState.READY
    assert lm.is_ready() is True


def test_start_is_idempotent() -> None:
    lm = LifecycleManager()
    lm.start()
    lm.start()
    assert lm.state == LifecycleState.READY


def test_stop_transitions_to_stopped() -> None:
    lm = LifecycleManager()
    lm.start()
    lm.stop()
    assert lm.state == LifecycleState.STOPPED
    assert lm.is_stopped() is True


def test_stop_is_idempotent() -> None:
    lm = LifecycleManager()
    lm.start()
    lm.stop()
    lm.stop()
    assert lm.state == LifecycleState.STOPPED


def test_start_hooks_execute() -> None:
    lm = LifecycleManager()
    calls: list[str] = []
    lm.add_start_hook(lambda: calls.append("hook1"))
    lm.add_start_hook(lambda: calls.append("hook2"))
    lm.start()
    assert calls == ["hook1", "hook2"]


def test_stop_hooks_execute_in_reverse() -> None:
    lm = LifecycleManager()
    calls: list[str] = []
    lm.add_stop_hook(lambda: calls.append("stop1"))
    lm.add_stop_hook(lambda: calls.append("stop2"))
    lm.start()
    lm.stop()
    assert calls == ["stop2", "stop1"]


def test_start_from_non_created_raises() -> None:
    lm = LifecycleManager()
    lm.start()
    lm.stop()
    try:
        lm.start()
        assert False, "Expected RuntimeError"
    except RuntimeError:
        pass


def test_stop_from_non_ready_raises() -> None:
    lm = LifecycleManager()
    try:
        lm.stop()
        assert False, "Expected RuntimeError"
    except RuntimeError:
        pass
