from runtime.ai.telemetry import Telemetry


def test_record() -> None:
    t = Telemetry()
    t.record("a-1", "execution", duration_ms=100.0)
    assert t.total_executions == 1


def test_agent_history() -> None:
    t = Telemetry()
    t.record("a-1", "e1")
    t.record("a-2", "e2")
    assert len(t.agent_history("a-1")) == 1


def test_failures() -> None:
    t = Telemetry()
    t.record("a-1", "e1", success=True)
    t.record("a-1", "e2", success=False)
    assert t.total_failures == 1
    assert len(t.failures("a-1")) == 1
