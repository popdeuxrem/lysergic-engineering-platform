from runtime.operations.gates import (
    GateEngine,
    SchemaGate,
    SecurityGate,
    ValidationGate,
)


def test_gate_evaluate() -> None:
    g = GateEngine()
    gates = (ValidationGate(gate_id="g1", gate_type="schema"), ValidationGate(gate_id="g2", gate_type="test"))
    results = g.evaluate_all(gates)
    assert len(results) == 2
    assert all(r.outcome == "pass" for r in results)


def test_all_passed() -> None:
    g = GateEngine()
    gates = (ValidationGate(gate_id="g1", gate_type="schema"),)
    results = g.evaluate_all(gates)
    assert g.all_passed(results) is True


def test_schema_gate() -> None:
    g = SchemaGate()
    gate = ValidationGate(gate_id="g1", gate_type="schema")
    result = g.evaluate(gate)
    assert result.outcome == "pass"


def test_security_gate() -> None:
    g = SecurityGate()
    gate = ValidationGate(gate_id="g1", gate_type="security")
    result = g.evaluate(gate)
    assert result.outcome == "pass"
