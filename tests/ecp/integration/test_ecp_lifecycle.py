from extensions.ecp.adapter import ECPAdapter
from extensions.ecp.graph import ECPEntity, ECPRelationship
from extensions.ecp.lifecycle import ECPLifecycle


def test_lifecycle() -> None:
    lc = ECPLifecycle()
    assert lc.state == "installed"
    lc.discover()
    assert lc.state == "discovered"
    lc.validate()
    assert lc.state == "validated"
    lc.load()
    assert lc.state == "loaded"
    lc.initialize()
    assert lc.state == "initialized"
    lc.shutdown()
    assert lc.state == "shutdown"


def test_full_graph_lifecycle() -> None:
    a = ECPAdapter()
    a.initialize()
    a.entities.create(ECPEntity(entity_id="ast-1", entity_type="artifact", name="Schema A", version="1.0.0"))
    a.entities.create(ECPEntity(entity_id="ast-2", entity_type="artifact", name="Schema B", version="1.0.0"))
    assert a.entities.count == 2
    a.relationships.create(ECPRelationship(relationship_id="r1", relationship_type="depends_on", source_id="ast-1", target_id="ast-2"))
    assert a.relationships.count == 1
    result = a.graph.validate_all()
    assert result.valid is True
    a.shutdown()
