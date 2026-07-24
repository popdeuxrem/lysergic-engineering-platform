from runtime.ai.executor import AIExecutor, InProcessProvider


def test_inprocess_execution() -> None:
    ex = AIExecutor()
    result = ex.execute("analyze this")
    assert result is not None
    assert "analyze" in result


def test_register_provider() -> None:
    ex = AIExecutor()
    ex.register_provider(InProcessProvider("gpt-mock"))
    result = ex.execute("hello", provider_id="inprocess")
    assert result is not None


def test_model_name() -> None:
    p = InProcessProvider("test-model")
    assert p.model_name == "test-model"


def test_default_provider() -> None:
    ex = AIExecutor()
    assert ex.default_provider.model_name == "mock"
