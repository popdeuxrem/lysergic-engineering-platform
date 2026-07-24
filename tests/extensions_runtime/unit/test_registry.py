from extensions.sdk.manifest import ExtensionManifest
from runtime.extensions.registry import ExtensionRuntimeRecord, ExtensionRuntimeRegistry


def _record(eid: str = "ext-1") -> ExtensionRuntimeRecord:
    return ExtensionRuntimeRecord(extension_id=eid, manifest=ExtensionManifest(extension_id=eid, name=eid, version="1.0.0"))


def test_register() -> None:
    r = ExtensionRuntimeRegistry()
    r.register(_record())
    assert "ext-1" in r
    assert r.count == 1


def test_duplicate_raises() -> None:
    r = ExtensionRuntimeRegistry()
    r.register(_record("dup"))
    try:
        r.register(_record("dup"))
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_get() -> None:
    r = ExtensionRuntimeRegistry()
    rec = _record("ext-1")
    r.register(rec)
    assert r.get("ext-1") is rec
    assert r.get("missing") is None


def test_unregister() -> None:
    r = ExtensionRuntimeRegistry()
    r.register(_record("a"))
    assert r.unregister("a") is True
    assert r.count == 0


def test_list() -> None:
    r = ExtensionRuntimeRegistry()
    r.register(_record("a"))
    r.register(_record("b"))
    assert len(r.list()) == 2


def test_list_by_state() -> None:
    r = ExtensionRuntimeRegistry()
    r.register(_record("a"))
    r.register(_record("b"))
    assert len(r.list_by_state("installed")) == 2


def test_set_state() -> None:
    r = ExtensionRuntimeRegistry()
    r.register(_record("a"))
    r.set_state("a", "discovered")
    assert r.get("a").state == "discovered"


def test_set_error() -> None:
    r = ExtensionRuntimeRegistry()
    r.register(_record("a"))
    r.set_error("a", "fail")
    assert r.get("a").error == "fail"


def test_freeze() -> None:
    r = ExtensionRuntimeRegistry()
    r.freeze()
    try:
        r.register(_record("late"))
        assert False
    except Exception:  # noqa: BLE001, S110
        pass
