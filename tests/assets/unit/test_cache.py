from runtime.assets.cache import AssetCache


def test_set_and_get() -> None:
    c = AssetCache()
    c.set("key1", "value1")
    assert c.get("key1") == "value1"


def test_get_missing() -> None:
    c = AssetCache()
    assert c.get("missing") is None


def test_invalidate() -> None:
    c = AssetCache()
    c.set("k", "v")
    assert c.invalidate("k") is True
    assert c.get("k") is None


def test_clear() -> None:
    c = AssetCache()
    c.set("a", 1)
    c.set("b", 2)
    c.clear()
    assert c.size == 0


def test_disable() -> None:
    c = AssetCache()
    c.disable()
    assert c.enabled is False
    c.enable()
    assert c.enabled is True


def test_access_count() -> None:
    c = AssetCache()
    c.set("k", "v")
    c.get("k")
    c.get("k")
    entry = c._entries["k"]
    assert entry.access_count == 2
