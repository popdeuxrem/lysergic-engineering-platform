from extensions.ecp.graph import ECPRelationship
from extensions.ecp.graph.relationships import RelationshipRegistry


def test_create() -> None:
    r = RelationshipRegistry()
    rel = ECPRelationship(relationship_id="rel-1", relationship_type="depends_on", source_id="a", target_id="b")
    r.create(rel)
    assert r.get("rel-1") is rel
    assert r.count == 1


def test_list_for_entity() -> None:
    r = RelationshipRegistry()
    r.create(ECPRelationship(relationship_id="r1", relationship_type="owns", source_id="a", target_id="b"))
    r.create(ECPRelationship(relationship_id="r2", relationship_type="depends", source_id="b", target_id="c"))
    assert len(r.list_for_entity("a")) == 1
    assert len(r.list_for_entity("b")) == 2


def test_validate_self_reference() -> None:
    r = RelationshipRegistry()
    r.create(ECPRelationship(relationship_id="self", relationship_type="reflexive", source_id="x", target_id="x"))
    result = r.validate({"x", "y"})
    assert result.valid is False


def test_validate_missing_source() -> None:
    r = RelationshipRegistry()
    r.create(ECPRelationship(relationship_id="r1", relationship_type="depends", source_id="missing", target_id="y"))
    result = r.validate({"y"})
    assert result.valid is False
