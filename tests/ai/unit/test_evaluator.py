from runtime.ai.evaluator import Evaluator


def test_evaluate() -> None:
    e = Evaluator()
    result = e.evaluate("exec-1", "a-1", "output", "output")
    assert result.valid is True
    assert result.score == 1.0


def test_evaluate_mismatch() -> None:
    e = Evaluator()
    result = e.evaluate("exec-1", "a-1", "actual", "expected")
    assert result.valid is False
    assert result.score == 0.0


def test_history() -> None:
    e = Evaluator()
    e.evaluate("e1", "a-1", "out")
    e.evaluate("e2", "a-2", "out")
    assert len(e.history("a-1")) == 1


def test_all_results() -> None:
    e = Evaluator()
    e.evaluate("e1", "a-1", "out")
    assert len(e.all_results) == 1
