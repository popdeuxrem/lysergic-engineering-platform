from extensions.ecp.graph import ECPEntity, ECPRelationship
from extensions.ecp.graph.entities import EntityRegistry
from extensions.ecp.graph.references import ReferenceResolver
from extensions.ecp.graph.relationships import RelationshipRegistry
from extensions.ecp.graph.validator import GraphValidator


def test_validate_acyclic() -> None:
    entities = EntityRegistry()
    relationships = RelationshipRegistry()
    references = ReferenceResolver()
    entities.create(ECPEntity(entity_id="a", entity_type="node", name="A"))
    entities.create(ECPEntity(entity_id="b", entity_type="node", name="B"))
    relationships.create(ECPRelationship(relationship_id="r1", relationship_type="depends", source_id="a", target_id="b"))
    v = GraphValidator(entities, relationships, references)
    result = v.validate_all()
    assert result.valid is True


def test_validate_cycle_detected() -> None:
    entities = EntityRegistry()
    relationships = RelationshipRegistry()
    references = ReferenceResolver()
    entities.create(ECPEntity(entity_id="a", entity_type="node", name="A"))
    entities.create(ECPEntity(entity_id="b", entity_type="node", name="B"))
    relationships.create(ECPRelationship(relationship_id="r1", relationship_type="depends", source_id="a", target_id="b"))
    relationships.create(ECPRelationship(relationship_id="r2", relationship_type="depends", source_id="b", target_id="a"))
    v = GraphValidator(entities, relationships, references)
    result = v.validate_all()
    assert result.valid is False
