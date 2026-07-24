from runtime.configuration.exceptions import ProviderNotFoundError
from runtime.configuration.provider import (
    ConfigSource,
    ProviderRegistration,
    ProviderRegistry,
)


class FakeProvider:
    def __init__(self, pid: str = "fake", priority: int = 0) -> None:
        self.provider_id = pid
        self.source = ConfigSource.PROVIDER
        self._priority = priority
        self._data = {"fake.key": pid}

    def load(self) -> dict[str, str]:
        return self._data

    @property
    def priority(self) -> int:
        return self._priority


def test_register() -> None:
    r = ProviderRegistry()
    reg = ProviderRegistration(provider_id="p1", provider=FakeProvider("p1"))
    r.register(reg)
    assert "p1" in r
    assert r.count == 1


def test_register_duplicate_raises() -> None:
    r = ProviderRegistry()
    r.register(ProviderRegistration(provider_id="p1", provider=FakeProvider("p1")))
    try:
        r.register(ProviderRegistration(provider_id="p1", provider=FakeProvider("p1")))
        assert False
    except ValueError:
        pass


def test_get() -> None:
    r = ProviderRegistry()
    r.register(ProviderRegistration(provider_id="p1", provider=FakeProvider("p1")))
    reg = r.get("p1")
    assert reg.provider_id == "p1"


def test_get_missing_raises() -> None:
    r = ProviderRegistry()
    try:
        r.get("missing")
        assert False
    except ProviderNotFoundError:
        pass


def test_unregister() -> None:
    r = ProviderRegistry()
    r.register(ProviderRegistration(provider_id="p1", provider=FakeProvider("p1")))
    assert r.unregister("p1") is True
    assert r.count == 0
    assert r.unregister("p1") is False


def test_freeze_prevents_register() -> None:
    r = ProviderRegistry()
    r.freeze()
    try:
        r.register(ProviderRegistration(provider_id="late", provider=FakeProvider("late")))
        assert False
    except RuntimeError:
        pass


def test_providers_property() -> None:
    r = ProviderRegistry()
    r.register(ProviderRegistration(provider_id="a", provider=FakeProvider("a")))
    assert "a" in r.providers
