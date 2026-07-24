from runtime.configuration.watcher import ConfigWatcher


def test_watch_and_notify() -> None:
    w = ConfigWatcher()
    received: list[tuple[str, object, object]] = []
    def handler(key: str, old: object, new: object) -> None:
        received.append((key, old, new))
    w.watch("db.host", handler)
    w.notify("db.host", "localhost", "remote")
    assert len(received) == 1
    assert received[0] == ("db.host", "localhost", "remote")


def test_wildcard_watch() -> None:
    w = ConfigWatcher()
    received: list[str] = []
    def handler(key: str, old: object, new: object) -> None:
        received.append(key)
    w.watch("*", handler)
    w.notify("any.key", None, "val")
    assert received == ["any.key"]


def test_unwatch() -> None:
    w = ConfigWatcher()
    def handler(key: str, old: object, new: object) -> None:
        pass
    w.watch("key", handler)
    assert w.unwatch("key", handler) is True
    assert w.count == 0


def test_unwatch_nonexistent() -> None:
    w = ConfigWatcher()
    assert w.unwatch("missing", lambda k, o, n: None) is False


def test_disable_suppresses_notify() -> None:
    w = ConfigWatcher()
    called = False
    def handler(key: str, old: object, new: object) -> None:
        nonlocal called
        called = True
    w.watch("key", handler)
    w.disable()
    w.notify("key", "old", "new")
    assert called is False


def test_enable() -> None:
    w = ConfigWatcher()
    w.disable()
    w.enable()
    assert w.enabled is True


def test_count() -> None:
    w = ConfigWatcher()
    assert w.count == 0
    w.watch("a", lambda k, o, n: None)
    w.watch("b", lambda k, o, n: None)
    assert w.count == 2
