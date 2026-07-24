import json

from cli.kilo.output import CLIError, format_output


def test_format_json_success() -> None:
    output = format_output({"key": "value"}, format="json")
    parsed = json.loads(output)
    assert parsed["status"] == "success"
    assert parsed["data"]["key"] == "value"


def test_format_json_error() -> None:
    error = CLIError(code="NOT_FOUND", message="Entity not found")
    output = format_output(None, error=error, format="json")
    parsed = json.loads(output)
    assert parsed["status"] == "error"
    assert parsed["error"]["code"] == "NOT_FOUND"


def test_format_text_success() -> None:
    output = format_output({"name": "test", "version": "1.0.0"}, format="text")
    assert "name: test" in output
    assert "version: 1.0.0" in output


def test_format_text_error() -> None:
    error = CLIError(code="NOT_FOUND", message="Not found")
    output = format_output(None, error=error, format="text")
    assert "[NOT_FOUND]" in output


def test_format_text_none() -> None:
    output = format_output(None, format="text")
    assert output == ""


def test_format_text_list() -> None:
    output = format_output(["a", "b", "c"], format="text")
    assert output == "a\nb\nc"


def test_format_text_dict_with_nested() -> None:
    data = {"svc": {"count": 5, "ready": 3}, "items": ["a", "b"]}
    output = format_output(data, format="text")
    assert "svc:" in output
    assert "  count: 5" in output
    assert "  ready: 3" in output
    assert "  - a" in output


def test_cli_error_to_dict() -> None:
    error = CLIError(code="ERR", message="msg", details={"key": "val"})
    d = error.to_dict()
    assert d["code"] == "ERR"
    assert d["details"]["key"] == "val"
