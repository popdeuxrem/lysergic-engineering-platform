from extensions.ecp.graph import ECPReference
from extensions.ecp.graph.references import ReferenceResolver


def test_register() -> None:
    r = ReferenceResolver()
    ref = ECPReference(reference_id="ref-1", ref_type="derived_from", target_type="artifact", target_id="ast-1")
    r.register(ref)
    assert r.get("ref-1") is ref
    assert r.count == 1


def test_resolve() -> None:
    r = ReferenceResolver()
    r.register(ECPReference(reference_id="r1", ref_type="derived_from", target_type="artifact", target_id="ast-1"))
    r.register(ECPReference(reference_id="r2", ref_type="derived_from", target_type="artifact", target_id="ast-1"))
    results = r.resolve("artifact", "ast-1")
    assert len(results) == 2


def test_validate() -> None:
    r = ReferenceResolver()
    r.register(ECPReference(reference_id="r1", ref_type="derived_from", target_type="artifact", target_id="ast-1"))
    result = r.validate({("artifact", "ast-1")})
    assert result.valid is True


def test_validate_missing_target() -> None:
    r = ReferenceResolver()
    r.register(ECPReference(reference_id="r1", ref_type="derived_from", target_type="artifact", target_id="missing"))
    result = r.validate({("artifact", "existing")})
    assert result.valid is False
