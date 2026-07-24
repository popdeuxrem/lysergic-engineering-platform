from extensions.ecp.adapter import ECPAdapter


def test_adapter_initialize() -> None:
    a = ECPAdapter()
    a.initialize()
    assert a.ready is True
    a.shutdown()
    assert a.ready is False


def test_adapter_components() -> None:
    a = ECPAdapter()
    assert a.entities is not None
    assert a.relationships is not None
    assert a.references is not None
    assert a.graph is not None
    assert a.tier1 is not None
    assert a.tier2 is not None


def test_adapter_double_initialize() -> None:
    a = ECPAdapter()
    a.initialize()
    a.initialize()
    assert a.ready is True
