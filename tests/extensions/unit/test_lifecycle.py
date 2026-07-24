from extensions.sdk.lifecycle import ExtensionLifecycle, ExtensionLifecycleState


def test_initial_state() -> None:
    lc = ExtensionLifecycle()
    record = lc.register("ext-1")
    assert record.state == ExtensionLifecycleState.DISCOVERED


def test_transition_validated() -> None:
    lc = ExtensionLifecycle()
    lc.register("ext-1")
    lc.transition("ext-1", ExtensionLifecycleState.VALIDATED)
    assert lc.state_of("ext-1") == ExtensionLifecycleState.VALIDATED


def test_transition_loading() -> None:
    lc = ExtensionLifecycle()
    lc.register("ext-1")
    lc.transition("ext-1", ExtensionLifecycleState.VALIDATED)
    lc.transition("ext-1", ExtensionLifecycleState.LOADING)
    assert lc.state_of("ext-1") == ExtensionLifecycleState.LOADING


def test_transition_ready() -> None:
    lc = ExtensionLifecycle()
    lc.register("ext-1")
    lc.transition("ext-1", ExtensionLifecycleState.VALIDATED)
    lc.transition("ext-1", ExtensionLifecycleState.LOADING)
    lc.transition("ext-1", ExtensionLifecycleState.READY)
    assert lc.state_of("ext-1") == ExtensionLifecycleState.READY


def test_transition_failed() -> None:
    lc = ExtensionLifecycle()
    lc.register("ext-1")
    lc.transition("ext-1", ExtensionLifecycleState.FAILED)
    assert lc.state_of("ext-1") == ExtensionLifecycleState.FAILED


def test_transition_stopped() -> None:
    lc = ExtensionLifecycle()
    lc.register("ext-1")
    lc.transition("ext-1", ExtensionLifecycleState.VALIDATED)
    lc.transition("ext-1", ExtensionLifecycleState.LOADING)
    lc.transition("ext-1", ExtensionLifecycleState.READY)
    lc.transition("ext-1", ExtensionLifecycleState.STOPPING)
    lc.transition("ext-1", ExtensionLifecycleState.STOPPED)
    assert lc.state_of("ext-1") == ExtensionLifecycleState.STOPPED


def test_transition_removed() -> None:
    lc = ExtensionLifecycle()
    lc.register("ext-1")
    lc.transition("ext-1", ExtensionLifecycleState.REMOVED)
    assert lc.state_of("ext-1") == ExtensionLifecycleState.REMOVED


def test_invalid_transition_raises() -> None:
    lc = ExtensionLifecycle()
    lc.register("ext-1")
    try:
        lc.transition("ext-1", ExtensionLifecycleState.READY)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_get_missing_extension() -> None:
    lc = ExtensionLifecycle()
    assert lc.get("nonexistent") is None
    assert lc.state_of("nonexistent") is None


def test_transition_missing_raises() -> None:
    lc = ExtensionLifecycle()
    try:
        lc.transition("missing", ExtensionLifecycleState.VALIDATED)
        assert False, "Expected KeyError"
    except KeyError:
        pass


def test_transition_records_timestamp() -> None:
    lc = ExtensionLifecycle()
    lc.register("ext-1")
    lc.transition("ext-1", ExtensionLifecycleState.VALIDATED)
    record = lc.get("ext-1")
    assert record is not None
    assert "validated" in record.transitions


def test_transition_with_error() -> None:
    lc = ExtensionLifecycle()
    lc.register("ext-1")
    lc.transition("ext-1", ExtensionLifecycleState.FAILED, "Something broke")
    record = lc.get("ext-1")
    assert record is not None
    assert record.error == "Something broke"
