from runtime.configuration.merge import (
    deep_merge,
    deep_merge_all,
    filter_keys,
    flatten,
    unflatten,
)


def test_deep_merge_simple() -> None:
    base = {"a": 1, "b": 2}
    override = {"b": 3, "c": 4}
    result = deep_merge(base, override)
    assert result == {"a": 1, "b": 3, "c": 4}


def test_deep_merge_nested() -> None:
    base = {"db": {"host": "localhost", "port": 5432}}
    override = {"db": {"host": "remote"}}
    result = deep_merge(base, override)
    assert result == {"db": {"host": "remote", "port": 5432}}


def test_deep_merge_conflict_error() -> None:
    try:
        deep_merge({"a": 1}, {"a": 2}, strategy="error")
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_deep_merge_all() -> None:
    configs = [{"a": 1}, {"b": 2}, {"a": 3}]
    result = deep_merge_all(configs)
    assert result == {"a": 3, "b": 2}


def test_flatten() -> None:
    data = {"db": {"host": "localhost", "port": 5432}}
    flat = flatten(data)
    assert flat == {"db.host": "localhost", "db.port": 5432}


def test_unflatten() -> None:
    flat = {"db.host": "localhost", "db.port": 5432}
    result = unflatten(flat)
    assert result == {"db": {"host": "localhost", "port": 5432}}


def test_flatten_unflatten_roundtrip() -> None:
    original = {"app": {"name": "test", "version": "1.0", "nested": {"key": "val"}}}
    flat = flatten(original)
    result = unflatten(flat)
    assert result == original


def test_filter_keys() -> None:
    data = {"app.name": "test", "db.host": "localhost", "app.version": "1.0"}
    filtered = filter_keys(data, "app.")
    assert "app.name" in filtered
    assert "db.host" not in filtered
