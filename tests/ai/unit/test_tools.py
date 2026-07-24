from runtime.ai.exceptions import PermissionDeniedError
from runtime.ai.tools import ToolInvocation


def test_register_tool() -> None:
    t = ToolInvocation()
    t.register_tool("analyze", lambda x: f"analyzed: {x}", "Text analysis")
    assert t.tool_count == 1


def test_invoke_tool() -> None:
    t = ToolInvocation()
    t.register_tool("calc", lambda x: x * 2)
    result = t.invoke("calc", "agent-1", {"calc"}, 5)
    assert result == 10


def test_invoke_tool_denied_raises() -> None:
    t = ToolInvocation()
    t.register_tool("secret", lambda x: x)
    try:
        t.invoke("secret", "agent-1", set(), "data")
        assert False
    except PermissionDeniedError:
        pass


def test_list_tools() -> None:
    t = ToolInvocation()
    t.register_tool("t1", "handler1", "Tool 1")
    t.register_tool("t2", "handler2", "Tool 2")
    assert len(t.list_tools()) == 2
