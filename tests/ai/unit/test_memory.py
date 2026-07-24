from runtime.ai.memory import AgentMemory


def test_session_creation() -> None:
    m = AgentMemory()
    m.create_session("sess-1")
    assert "sess-1" in m.active_sessions


def test_set_and_get() -> None:
    m = AgentMemory()
    m.create_session("sess-1")
    m.set("sess-1", "key", "value")
    assert m.get("sess-1", "key") == "value"


def test_get_missing() -> None:
    m = AgentMemory()
    assert m.get("sess-1", "key") is None


def test_session_history() -> None:
    m = AgentMemory()
    m.create_session("sess-1")
    m.set("sess-1", "a", 1)
    m.set("sess-1", "b", 2)
    assert len(m.session_history("sess-1")) == 2


def test_clear_session() -> None:
    m = AgentMemory()
    m.create_session("sess-1")
    m.set("sess-1", "k", "v")
    m.clear_session("sess-1")
    assert "sess-1" not in m.active_sessions
