from runtime.ai.exceptions import (
    AgentNotFoundError,
    InvalidLifecycleError,
    PermissionDeniedError,
)


def test_agent_not_found() -> None:
    e = AgentNotFoundError("a-1")
    assert e.agent_id == "a-1"


def test_invalid_lifecycle() -> None:
    e = InvalidLifecycleError("created", "running")
    assert e.current == "created"
    assert e.target == "running"


def test_permission_denied() -> None:
    e = PermissionDeniedError("a-1", "tool:exec")
    assert "tool:exec" in str(e)
