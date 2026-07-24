from runtime.assets.lifecycle import AssetLifecycle, AssetLifecycleState


def test_initialize() -> None:
    lc = AssetLifecycle()
    lc.initialize("ast-1")
    assert lc.state_of("ast-1") == AssetLifecycleState.REGISTERED


def test_transition_validate() -> None:
    lc = AssetLifecycle()
    lc.initialize("ast-1")
    lc.transition("ast-1", AssetLifecycleState.VALIDATED)
    assert lc.state_of("ast-1") == AssetLifecycleState.VALIDATED


def test_transition_available() -> None:
    lc = AssetLifecycle()
    lc.initialize("ast-1")
    lc.transition("ast-1", AssetLifecycleState.VALIDATED)
    lc.transition("ast-1", AssetLifecycleState.AVAILABLE)
    assert lc.state_of("ast-1") == AssetLifecycleState.AVAILABLE


def test_transition_deprecated() -> None:
    lc = AssetLifecycle()
    lc.initialize("ast-1")
    lc.transition("ast-1", AssetLifecycleState.VALIDATED)
    lc.transition("ast-1", AssetLifecycleState.AVAILABLE)
    lc.transition("ast-1", AssetLifecycleState.DEPRECATED)
    assert lc.state_of("ast-1") == AssetLifecycleState.DEPRECATED


def test_transition_removed() -> None:
    lc = AssetLifecycle()
    lc.initialize("ast-1")
    lc.transition("ast-1", AssetLifecycleState.REMOVED)
    assert lc.state_of("ast-1") == AssetLifecycleState.REMOVED


def test_invalid_transition_raises() -> None:
    lc = AssetLifecycle()
    lc.initialize("ast-1")
    try:
        lc.transition("ast-1", AssetLifecycleState.AVAILABLE)
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_history() -> None:
    lc = AssetLifecycle()
    lc.initialize("ast-1")
    lc.transition("ast-1", AssetLifecycleState.VALIDATED)
    assert len(lc.history) == 2
