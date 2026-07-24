from runtime.configuration.provider import ConfigSource
from runtime.configuration.resolver import LayerResolver


def test_empty_resolver() -> None:
    r = LayerResolver()
    assert r.resolve("key") == (None, None)


def test_set_and_resolve() -> None:
    r = LayerResolver()
    r.set_layer(ConfigSource.DEFAULT, {"key": "default"})
    val, src = r.resolve("key")
    assert val == "default"
    assert src == ConfigSource.DEFAULT


def test_precedence() -> None:
    r = LayerResolver()
    r.set_layer(ConfigSource.DEFAULT, {"key": "default"})
    r.set_layer(ConfigSource.RUNTIME_OVERRIDE, {"key": "override"})
    val, src = r.resolve("key")
    assert val == "override"
    assert src == ConfigSource.RUNTIME_OVERRIDE


def test_resolve_all() -> None:
    r = LayerResolver()
    r.set_layer(ConfigSource.DEFAULT, {"a": "default", "b": "default"})
    r.set_layer(ConfigSource.ENVIRONMENT, {"b": "env"})
    result = r.resolve_all()
    assert result["a"] == "default"
    assert result["b"] == "env"


def test_resolve_with_source() -> None:
    r = LayerResolver()
    r.set_layer(ConfigSource.DEFAULT, {"a": "default"})
    r.set_layer(ConfigSource.ENVIRONMENT, {"b": "env"})
    result = r.resolve_with_source()
    assert result["a"] == ("default", ConfigSource.DEFAULT)
    assert result["b"] == ("env", ConfigSource.ENVIRONMENT)


def test_clear() -> None:
    r = LayerResolver()
    r.set_layer(ConfigSource.DEFAULT, {"key": "val"})
    r.clear()
    assert r.resolve("key") == (None, None)


def test_layer_count() -> None:
    r = LayerResolver()
    assert r.layer_count == 0
    r.set_layer(ConfigSource.DEFAULT, {"a": 1})
    assert r.layer_count == 1
    r.set_layer(ConfigSource.ENVIRONMENT, {"b": 2})
    assert r.layer_count == 2
