from extensions.ecp.graph import ECPEntity
from extensions.ecp.graph.entities import EntityRegistry


def test_create() -> None:
    r = EntityRegistry()
    e = ECPEntity(entity_id="ast-1", entity_type="artifact", name="Test")
    r.create(e)
    assert r.get("ast-1") is e
    assert r.count == 1


def test_duplicate_raises() -> None:
    r = EntityRegistry()
    r.create(ECPEntity(entity_id="dup", entity_type="t", name="Dup"))
    try:
        r.create(ECPEntity(entity_id="dup", entity_type="t", name="Dup"))
        assert False
    except ValueError:
        pass


def test_list() -> None:
    r = EntityRegistry()
    r.create(ECPEntity(entity_id="a", entity_type="schema", name="A"))
    r.create(ECPEntity(entity_id="b", entity_type="template", name="B"))
    assert len(r.list()) == 2
    assert len(r.list_by_type("schema")) == 1


def test_remove() -> None:
    r = EntityRegistry()
    r.create(ECPEntity(entity_id="a", entity_type="t", name="A"))
    assert r.remove("a") is True
    assert r.count == 0


def test_validate() -> None:
    r = EntityRegistry()
    e = ECPEntity(entity_id="ast-1", entity_type="artifact", name="Test")
    r.create(e)
    result = r.validate()
    assert result.valid is True


def test_validate_missing_type() -> None:
    r = EntityRegistry()
    r.create(ECPEntity(entity_id="bad", entity_type="", name="Bad"))
    result = r.validate()
    assert result.valid is False
