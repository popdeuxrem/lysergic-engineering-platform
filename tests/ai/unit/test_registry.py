from runtime.ai.model import Agent, AgentCapability
from runtime.ai.registry import AgentRegistry


def test_register() -> None:
    r = AgentRegistry()
    r.register(Agent(agent_id="a-1", name="Helper", version="1.0.0"))
    assert "a-1" in r
    assert r.count == 1


def test_duplicate_raises() -> None:
    r = AgentRegistry()
    r.register(Agent(agent_id="a-1", name="T", version="1.0.0"))
    try:
        r.register(Agent(agent_id="a-1", name="T", version="1.0.0"))
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_get() -> None:
    r = AgentRegistry()
    a = Agent(agent_id="a-1", name="T", version="1.0.0")
    r.register(a)
    assert r.get("a-1") is a
    assert r.get("missing") is None


def test_unregister() -> None:
    r = AgentRegistry()
    r.register(Agent(agent_id="a", name="A", version="1.0.0"))
    assert r.unregister("a") is True
    assert r.count == 0


def test_list() -> None:
    r = AgentRegistry()
    r.register(Agent(agent_id="a", name="A", version="1.0.0"))
    r.register(Agent(agent_id="b", name="B", version="2.0.0"))
    assert len(r.list()) == 2


def test_list_by_capability() -> None:
    caps = (AgentCapability(capability_id="analyze"),)
    r = AgentRegistry()
    r.register(Agent(agent_id="a", name="A", version="1.0.0", capabilities=caps))
    r.register(Agent(agent_id="b", name="B", version="1.0.0"))
    assert len(r.list_by_capability("analyze")) == 1


def test_freeze() -> None:
    r = AgentRegistry()
    r.freeze()
    try:
        r.register(Agent(agent_id="late", name="Late", version="1.0.0"))
        assert False
    except Exception:  # noqa: BLE001, S110
        pass
