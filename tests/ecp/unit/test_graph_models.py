from extensions.ecp.graph import ECPEntity, ECPReference, ECPRelationship


def test_entity_creation() -> None:
    e = ECPEntity(entity_id="ast-1", entity_type="artifact", name="Test", version="1.0.0")
    assert e.entity_id == "ast-1"
    assert e.entity_type == "artifact"
    assert e.version == "1.0.0"


def test_relationship_creation() -> None:
    r = ECPRelationship(relationship_id="rel-1", relationship_type="depends_on", source_id="ast-1", target_id="ast-2")
    assert r.relationship_id == "rel-1"
    assert r.source_id == "ast-1"
    assert r.target_id == "ast-2"


def test_reference_creation() -> None:
    r = ECPReference(reference_id="ref-1", ref_type="derived_from", target_type="artifact", target_id="ast-1")
    assert r.reference_id == "ref-1"
    assert r.ref_type == "derived_from"
