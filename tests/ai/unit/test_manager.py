from runtime.ai.manager import AIManager
from runtime.services.events import EventBus


def test_initial_state() -> None:
    m = AIManager()
    assert m.manager_status.name == "PENDING"


def test_initialize() -> None:
    m = AIManager()
    m.initialize_runtime()
    assert m.manager_status.name == "READY"


def test_create_agent() -> None:
    m = AIManager()
    m.initialize_runtime()
    a = m.create_agent("a-1", "Helper", version="1.0.0")
    assert a.agent_id == "a-1"
    assert m.get_agent("a-1") is not None


def test_register_agent() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a-1", "Helper")
    m.register_agent("a-1")
    assert m.status("a-1") == "registered"


def test_validate_agent() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a-1", "Helper")
    m.register_agent("a-1")
    m.validate_agent("a-1")
    assert m.status("a-1") == "validated"


def test_ready_agent() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a-1", "Helper")
    m.register_agent("a-1")
    m.validate_agent("a-1")
    m.ready_agent("a-1")
    assert m.status("a-1") == "ready"


def test_execute() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a-1", "Helper")
    m.register_agent("a-1")
    m.validate_agent("a-1")
    m.ready_agent("a-1")
    result = m.execute("a-1", "analyze this")
    assert result.status == "completed"


def test_execute_missing() -> None:
    m = AIManager()
    m.initialize_runtime()
    result = m.execute("missing", "prompt")
    assert result.status == "failed"


def test_stop_agent() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a-1", "Helper")
    m.register_agent("a-1")
    m.validate_agent("a-1")
    m.ready_agent("a-1")
    m.stop_agent("a-1")
    assert m.status("a-1") == "stopped"


def test_archive_agent() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a-1", "Helper")
    m.archive_agent("a-1")
    assert m.status("a-1") == "archived"


def test_status() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a-1", "Helper")
    assert m.status("a-1") == "created"
    assert m.status("missing") is None


def test_list() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a", "A")
    m.create_agent("b", "B")
    assert len(m.list_agents()) == 2


def test_evaluate() -> None:
    m = AIManager()
    m.initialize_runtime()
    result = m.evaluate("exec-1", "a-1", "output")
    assert result["valid"] is True


def test_snapshot() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a-1", "Helper")
    snap = m.snapshot_state()
    assert snap.count() == 1


def test_events() -> None:
    bus = EventBus()
    events: list[str] = []
    bus.subscribe_all(lambda e: events.append(e.event_type))
    m = AIManager(event_bus=bus)
    m.initialize_runtime()
    m.create_agent("a-1", "Helper")
    assert "ai.AgentCreated" in events


def test_shutdown() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a-1", "Helper")
    m.shutdown()
    assert m.get_agent("a-1") is None


def test_execute_with_session() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a-1", "Helper")
    m.register_agent("a-1")
    m.validate_agent("a-1")
    m.ready_agent("a-1")
    result = m.execute("a-1", "analyze", session_id="sess-1")
    assert result.status == "completed"
    memory_val = m.memory.get("sess-1", "last_prompt")
    assert memory_val == "analyze"
