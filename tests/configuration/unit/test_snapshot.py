from runtime.configuration.snapshot import ConfigSnapshot


def test_snapshot_creation() -> None:
    snap = ConfigSnapshot(config={"key": "val"}, source="test", version=1)
    assert snap.config == {"key": "val"}
    assert snap.source == "test"
    assert snap.version == 1


def test_snapshot_get() -> None:
    snap = ConfigSnapshot(config={"db": {"host": "localhost", "port": 5432}})
    assert snap.get("db.host") == "localhost"
    assert snap.get("db.port") == 5432


def test_snapshot_get_nested() -> None:
    snap = ConfigSnapshot(config={"a": {"b": {"c": "deep"}}})
    assert snap.get("a.b.c") == "deep"


def test_snapshot_get_default() -> None:
    snap = ConfigSnapshot(config={})
    assert snap.get("missing", "default") == "default"
    assert snap.get("missing") is None


def test_snapshot_has() -> None:
    snap = ConfigSnapshot(config={"key": "val"})
    assert snap.has("key") is True
    assert snap.has("missing") is False


def test_snapshot_frozen() -> None:
    snap = ConfigSnapshot(config={"key": "val"})
    assert snap.frozen is True


def test_snapshot_to_dict() -> None:
    snap = ConfigSnapshot(config={"k": "v"}, source="s", version=2, profile="prod")
    d = snap.to_dict()
    assert d["config"] == {"k": "v"}
    assert d["source"] == "s"
    assert d["version"] == 2
    assert d["profile"] == "prod"
    assert "timestamp" in d
