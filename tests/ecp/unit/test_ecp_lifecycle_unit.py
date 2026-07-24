from __future__ import annotations

from extensions.ecp.lifecycle import ECPLifecycle


def test_initial_state() -> None:
    lc = ECPLifecycle()
    assert lc.state == "installed"


def test_full_lifecycle() -> None:
    lc = ECPLifecycle()
    assert lc.state == "installed"
    lc.discover()
    assert lc.state == "discovered"
    lc.validate()
    assert lc.state == "validated"
    lc.load()
    assert lc.state == "loaded"
    lc.initialize()
    assert lc.state == "initialized"
    lc.execute()
    assert lc.state == "executing"
    lc.shutdown()
    assert lc.state == "shutdown"


def test_failure_state() -> None:
    lc = ECPLifecycle()
    lc.discover()
    lc.validate()
    lc.fail()
    assert lc.state == "failed"


def test_removal_state() -> None:
    lc = ECPLifecycle()
    lc.discover()
    lc.validate()
    lc.load()
    lc.initialize()
    lc.execute()
    lc.shutdown()
    lc.remove()
    assert lc.state == "removed"


def test_lifecycle_history() -> None:
    lc = ECPLifecycle()
    lc.discover()
    lc.validate()
    history = lc.history
    assert len(history) == 2
    assert history[0]["from"] == "installed"
    assert history[0]["to"] == "discovered"
    assert history[1]["from"] == "discovered"
    assert history[1]["to"] == "validated"


def test_initialize_is_idempotent() -> None:
    lc = ECPLifecycle()
    lc.initialize()
    lc.initialize()
    assert lc.state == "initialized"
