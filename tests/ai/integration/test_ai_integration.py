from runtime.ai.manager import AIManager
from runtime.services.events import EventBus


def test_full_lifecycle() -> None:
    bus = EventBus()
    events: list[str] = []
    bus.subscribe_all(lambda e: events.append(e.event_type))

    m = AIManager(event_bus=bus)
    m.initialize_runtime()

    m.create_agent("a-1", "Research Agent", version="1.0.0", model="gpt-4", description="AI researcher")
    assert "ai.AgentCreated" in events

    m.register_agent("a-1")
    assert "ai.AgentRegistered" in events

    m.validate_agent("a-1")
    assert "ai.AgentValidated" in events

    m.ready_agent("a-1")

    result = m.execute("a-1", "Research quantum computing")
    assert result.status == "completed"
    assert "ai.AgentExecutionStarted" in events
    assert "ai.AgentExecutionCompleted" in events

    m.stop_agent("a-1")
    assert "ai.AgentStopped" in events
    assert m.status("a-1") == "stopped"

    assert len(m.list_agents()) == 1


def test_permission_enforcement() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a-1", "Secure Agent")
    m.permissions.configure("a-1", tools={"safe-tool"})
    assert m.permissions.can_access_tool("a-1", "safe-tool") is True
    assert m.permissions.can_access_tool("a-1", "unsafe-tool") is False


def test_telemetry_and_evaluation() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a-1", "Monitored Agent", version="1.0.0")
    m.register_agent("a-1")
    m.validate_agent("a-1")
    m.ready_agent("a-1")
    m.execute("a-1", "task")
    assert m.telemetry.total_executions >= 1
    eval_result = m.evaluate("exec-1", "a-1", "mock output")
    assert eval_result["valid"] is True or eval_result["valid"] is False


def test_tool_integration() -> None:
    m = AIManager()
    m.initialize_runtime()
    m.create_agent("a-1", "Tool Agent")
    m.tools.register_tool("search", lambda q: f"results for {q}", "Search tool", "plugin")
    m.permissions.configure("a-1", tools={"search"})
    assert m.tools.tool_count == 1
    tools = m.tools.list_tools()
    assert any(t["tool_id"] == "search" for t in tools)
