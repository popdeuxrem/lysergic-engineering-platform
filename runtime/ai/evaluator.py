from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class EvaluationResult:
    execution_id: str
    agent_id: str
    valid: bool = True
    score: float = 0.0
    metrics: dict[str, Any] = field(default_factory=dict)
    feedback: str = ""
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class Evaluator:
    def __init__(self) -> None:
        self._results: list[EvaluationResult] = []

    def evaluate(self, execution_id: str, agent_id: str, output: Any, expected: Any | None = None) -> EvaluationResult:
        score = 1.0 if expected is None or output == expected else 0.0
        result = EvaluationResult(
            execution_id=execution_id, agent_id=agent_id,
            valid=score >= 0.5, score=score,
            metrics={"output_length": len(str(output)) if output else 0},
        )
        self._results.append(result)
        return result

    def history(self, agent_id: str) -> tuple[EvaluationResult, ...]:
        return tuple(r for r in self._results if r.agent_id == agent_id)

    @property
    def all_results(self) -> tuple[EvaluationResult, ...]:
        return tuple(self._results)
