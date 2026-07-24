from runtime.knowledge.lifecycle import KnowledgeLifecycle, KnowledgeLifecycleState


def test_initial() -> None:
    lc = KnowledgeLifecycle()
    lc.initialize("k-1")
    assert lc.state_of("k-1") == KnowledgeLifecycleState.CREATED


def test_full_path() -> None:
    lc = KnowledgeLifecycle()
    lc.initialize("k-1")
    lc.transition("k-1", KnowledgeLifecycleState.INGESTED)
    lc.transition("k-1", KnowledgeLifecycleState.VALIDATED)
    lc.transition("k-1", KnowledgeLifecycleState.AVAILABLE)
    assert lc.state_of("k-1") == KnowledgeLifecycleState.AVAILABLE


def test_deprecate() -> None:
    lc = KnowledgeLifecycle()
    lc.initialize("k-1")
    lc.transition("k-1", KnowledgeLifecycleState.INGESTED)
    lc.transition("k-1", KnowledgeLifecycleState.VALIDATED)
    lc.transition("k-1", KnowledgeLifecycleState.AVAILABLE)
    lc.transition("k-1", KnowledgeLifecycleState.DEPRECATED)
    assert lc.state_of("k-1") == KnowledgeLifecycleState.DEPRECATED


def test_archive() -> None:
    lc = KnowledgeLifecycle()
    lc.initialize("k-1")
    lc.transition("k-1", KnowledgeLifecycleState.ARCHIVED)
    assert lc.state_of("k-1") == KnowledgeLifecycleState.ARCHIVED


def test_failed_retry() -> None:
    lc = KnowledgeLifecycle()
    lc.initialize("k-1")
    lc.transition("k-1", KnowledgeLifecycleState.FAILED)
    assert lc.state_of("k-1") == KnowledgeLifecycleState.FAILED
    lc.transition("k-1", KnowledgeLifecycleState.CREATED)
    assert lc.state_of("k-1") == KnowledgeLifecycleState.CREATED


def test_invalid_transition_raises() -> None:
    lc = KnowledgeLifecycle()
    lc.initialize("k-1")
    try:
        lc.transition("k-1", KnowledgeLifecycleState.AVAILABLE)
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_can_transition() -> None:
    lc = KnowledgeLifecycle()
    lc.initialize("k-1")
    assert lc.can_transition("k-1", KnowledgeLifecycleState.INGESTED) is True
    assert lc.can_transition("k-1", KnowledgeLifecycleState.AVAILABLE) is False


def test_history() -> None:
    lc = KnowledgeLifecycle()
    lc.initialize("k-1")
    lc.transition("k-1", KnowledgeLifecycleState.INGESTED)
    assert len(lc.history) == 2
