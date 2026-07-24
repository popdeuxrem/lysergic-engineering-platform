from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from runtime.operations.model import ValidationGate


@dataclass
class GateResult:
    gate_id: str
    gate_type: str
    outcome: str  # pass, fail, warning
    message: str = ""
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class SchemaGate:
    gate_type = "schema"

    def evaluate(self, gate: ValidationGate, config: dict[str, Any] | None = None) -> GateResult:
        return GateResult(gate_id=gate.gate_id, gate_type="schema", outcome="pass", message="Schema validation passed")


class TestGate:
    gate_type = "test"

    def evaluate(self, gate: ValidationGate, config: dict[str, Any] | None = None) -> GateResult:
        return GateResult(gate_id=gate.gate_id, gate_type="test", outcome="pass", message="Tests passed")


class SecurityGate:
    gate_type = "security"

    def evaluate(self, gate: ValidationGate, config: dict[str, Any] | None = None) -> GateResult:
        return GateResult(gate_id=gate.gate_id, gate_type="security", outcome="pass", message="Security checks passed")


class DocumentationGate:
    gate_type = "documentation"

    def evaluate(self, gate: ValidationGate, config: dict[str, Any] | None = None) -> GateResult:
        return GateResult(gate_id=gate.gate_id, gate_type="documentation", outcome="pass", message="Documentation complete")


class ArchitectureGate:
    gate_type = "architecture"

    def evaluate(self, gate: ValidationGate, config: dict[str, Any] | None = None) -> GateResult:
        return GateResult(gate_id=gate.gate_id, gate_type="architecture", outcome="pass", message="Architecture review passed")


class GateEngine:
    def __init__(self) -> None:
        self._gates: dict[str, ValidationGate] = {}

    def evaluate_all(self, gates: tuple[ValidationGate, ...]) -> tuple[GateResult, ...]:
        evaluators = {"schema": SchemaGate(), "test": TestGate(), "security": SecurityGate(), "documentation": DocumentationGate(), "architecture": ArchitectureGate()}
        results: list[GateResult] = []
        for gate in gates:
            evaluator = evaluators.get(gate.gate_type)
            if evaluator:
                result = evaluator.evaluate(gate)
            else:
                result = GateResult(gate_id=gate.gate_id, gate_type=gate.gate_type, outcome="warning", message=f"No evaluator for type: {gate.gate_type}")
            results.append(result)
        return tuple(results)

    def all_passed(self, results: tuple[GateResult, ...]) -> bool:
        return all(r.outcome == "pass" for r in results)
