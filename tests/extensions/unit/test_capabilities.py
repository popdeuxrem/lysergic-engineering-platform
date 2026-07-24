from extensions.sdk.capabilities import CapabilityRegistration, CapabilityRegistry


class FakeProvider:
    def __init__(self, cid: str, ver: str = "1.0.0") -> None:
        self.capability_id = cid
        self.version = ver

    def execute(self, **kwargs: object) -> str:
        return f"{self.capability_id}:{self.version}"

    @property
    def metadata(self) -> dict[str, object]:
        return {"id": self.capability_id, "version": self.version}


def test_register_capability() -> None:
    registry = CapabilityRegistry()
    reg = CapabilityRegistration(capability_id="schema.validate", provider_id="ext-1", version="1.0.0", provider=FakeProvider("schema.validate"))
    registry.register(reg)
    assert registry.registration_count == 1


def test_resolve_capability() -> None:
    registry = CapabilityRegistry()
    registry.register(CapabilityRegistration(capability_id="graph.analyze", provider_id="ext-1", version="1.0.0"))
    results = registry.resolve("graph.analyze")
    assert len(results) == 1


def test_resolve_by_version() -> None:
    registry = CapabilityRegistry()
    registry.register(CapabilityRegistration(capability_id="cache", provider_id="ext-1", version="1.0.0"))
    registry.register(CapabilityRegistration(capability_id="cache", provider_id="ext-2", version="2.0.0"))
    results = registry.resolve("cache", version="2.0.0")
    assert len(results) == 1
    assert results[0].provider_id == "ext-2"


def test_resolve_best_version() -> None:
    registry = CapabilityRegistry()
    registry.register(CapabilityRegistration(capability_id="cache", provider_id="ext-1", version="1.0.0"))
    registry.register(CapabilityRegistration(capability_id="cache", provider_id="ext-2", version="2.0.0"))
    best = registry.resolve_best("cache")
    assert best is not None
    assert best.provider_id == "ext-2"


def test_resolve_best_none() -> None:
    registry = CapabilityRegistry()
    assert registry.resolve_best("nonexistent") is None


def test_providers_for() -> None:
    registry = CapabilityRegistry()
    registry.register(CapabilityRegistration(capability_id="c1", provider_id="a", version="1.0.0"))
    registry.register(CapabilityRegistration(capability_id="c1", provider_id="b", version="1.0.0"))
    providers = registry.providers_for("c1")
    assert "a" in providers
    assert "b" in providers


def test_capabilities_for() -> None:
    registry = CapabilityRegistry()
    registry.register(CapabilityRegistration(capability_id="c1", provider_id="ext", version="1.0.0"))
    registry.register(CapabilityRegistration(capability_id="c2", provider_id="ext", version="1.0.0"))
    caps = registry.capabilities_for("ext")
    assert "c1" in caps
    assert "c2" in caps


def test_duplicate_provider_raises() -> None:
    registry = CapabilityRegistry()
    registry.register(CapabilityRegistration(capability_id="c1", provider_id="ext-1", version="1.0.0"))
    try:
        registry.register(CapabilityRegistration(capability_id="c1", provider_id="ext-1", version="1.0.0"))
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_remove_provider() -> None:
    registry = CapabilityRegistry()
    registry.register(CapabilityRegistration(capability_id="c1", provider_id="ext-1", version="1.0.0"))
    assert registry.remove_provider("c1", "ext-1") is True
    assert len(registry.resolve("c1")) == 0


def test_remove_provider_missing() -> None:
    registry = CapabilityRegistry()
    assert registry.remove_provider("c1", "missing") is False


def test_capability_ids() -> None:
    registry = CapabilityRegistry()
    registry.register(CapabilityRegistration(capability_id="a", provider_id="e1", version="1.0.0"))
    registry.register(CapabilityRegistration(capability_id="b", provider_id="e2", version="1.0.0"))
    assert "a" in registry.capability_ids
    assert "b" in registry.capability_ids
