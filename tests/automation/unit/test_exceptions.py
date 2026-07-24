from runtime.automation.exceptions import (
    AutomationNotFoundError,
    InvalidLifecycleError,
    PolicyDeniedError,
)


def test_not_found() -> None:
    e = AutomationNotFoundError("a-1")
    assert e.automation_id == "a-1"


def test_invalid_lifecycle() -> None:
    e = InvalidLifecycleError("created", "executing")
    assert e.current == "created"


def test_policy_denied() -> None:
    e = PolicyDeniedError("a-1", "target not allowed")
    assert "a-1" in str(e)
