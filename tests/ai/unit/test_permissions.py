from runtime.ai.permissions import AgentPermissions


def test_configure_tools() -> None:
    p = AgentPermissions()
    p.configure("a-1", tools={"tool-1", "tool-2"})
    assert p.can_access_tool("a-1", "tool-1") is True
    assert p.can_access_tool("a-1", "tool-3") is False


def test_deny_by_default() -> None:
    p = AgentPermissions()
    assert p.can_access_tool("a-1", "anything") is False


def test_knowledge_access() -> None:
    p = AgentPermissions()
    p.configure("a-1", knowledge={"k-1"})
    assert p.can_access_knowledge("a-1", "k-1") is True
    assert p.can_access_knowledge("a-1", "k-2") is False


def test_project_access() -> None:
    p = AgentPermissions()
    p.configure("a-1", projects={"p-1"})
    assert p.can_access_project("a-1", "p-1") is True


def test_enforce_tool_pass() -> None:
    p = AgentPermissions()
    p.configure("a-1", tools={"safe-tool"})
    p.enforce_tool("a-1", "safe-tool")


def test_enforce_tool_denied_raises() -> None:
    p = AgentPermissions()
    p.configure("a-1", tools={"safe"})
    try:
        p.enforce_tool("a-1", "unsafe")
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_revoke() -> None:
    p = AgentPermissions()
    p.configure("a-1", tools={"tool"})
    p.revoke("a-1")
    assert p.can_access_tool("a-1", "tool") is False
