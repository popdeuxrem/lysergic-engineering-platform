from runtime.ai.model import (
    Agent,
    AgentCapability,
    AgentContext,
    AgentExecution,
    AgentMetadata,
)


def test_agent_creation() -> None:
    a = Agent(agent_id="a-1", name="Helper", version="1.0.0")
    assert a.agent_id == "a-1"
    assert a.name == "Helper"


def test_agent_with_capabilities() -> None:
    caps = (AgentCapability(capability_id="analyze"), AgentCapability(capability_id="summarize"))
    a = Agent(agent_id="a-1", name="Helper", version="1.0.0", capabilities=caps)
    assert len(a.capabilities) == 2


def test_metadata() -> None:
    m = AgentMetadata(agent_id="a-1", name="Helper", version="1.0.0", model="gpt-4")
    assert m.model == "gpt-4"


def test_context() -> None:
    c = AgentContext(session_id="sess-1")
    assert c.session_id == "sess-1"


def test_execution() -> None:
    e = AgentExecution(execution_id="e1", agent_id="a-1", status="completed")
    assert e.status == "completed"
