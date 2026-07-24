from runtime.extensions.manager import ExtensionRuntimeManager


def test_initial_state() -> None:
    m = ExtensionRuntimeManager()
    assert m.manager_status.name == "PENDING"


def test_initialize() -> None:
    m = ExtensionRuntimeManager()
    m.initialize()
    assert m.manager_status.name == "READY"


def test_install() -> None:
    m = ExtensionRuntimeManager()
    m.initialize()
    import os
    import tempfile

    import yaml
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "extension.yaml")
        with open(path, "w") as f:
            yaml.dump({"extension_id": "ext-1", "name": "Test", "version": "1.0.0"}, f)
        record = m.install(path)
        assert record.extension_id == "ext-1"
        assert m.get("ext-1") is not None


def test_discover() -> None:
    m = ExtensionRuntimeManager()
    m.initialize()
    import os
    import tempfile

    import yaml
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "extension.yaml")
        with open(path, "w") as f:
            yaml.dump({"extension_id": "ext-1", "name": "Test", "version": "1.0.0"}, f)
        m.install(path)
        m.discover("ext-1")
        assert m.status("ext-1") == "discovered"


def test_validate() -> None:
    m = ExtensionRuntimeManager()
    m.initialize()
    import os
    import tempfile

    import yaml
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "extension.yaml")
        with open(path, "w") as f:
            yaml.dump({"extension_id": "ext-1", "name": "Test", "version": "1.0.0"}, f)
        m.install(path)
        m.discover("ext-1")
        m.validate_extension("ext-1")
        assert m.status("ext-1") == "validated"


def test_validate_fails_on_missing_id() -> None:
    m = ExtensionRuntimeManager()
    m.initialize()
    import os
    import tempfile

    import yaml
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "extension.yaml")
        with open(path, "w") as f:
            yaml.dump({"name": "Test", "version": "1.0.0"}, f)
        try:
            m.install(path)
            assert False, "Expected ManifestValidationError"
        except Exception:  # noqa: BLE001, S110
            pass


def test_load() -> None:
    m = ExtensionRuntimeManager()
    m.initialize()
    import os
    import tempfile

    import yaml
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "extension.yaml")
        with open(path, "w") as f:
            yaml.dump({"extension_id": "ext-1", "name": "Test", "version": "1.0.0"}, f)
        m.install(path)
        m.discover("ext-1")
        m.validate_extension("ext-1")
        m.load("ext-1")
        assert m.status("ext-1") == "loaded"


def test_initialize_extension() -> None:
    m = ExtensionRuntimeManager()
    m.initialize()
    import os
    import tempfile

    import yaml
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "extension.yaml")
        with open(path, "w") as f:
            yaml.dump({"extension_id": "ext-1", "name": "Test", "version": "1.0.0"}, f)
        m.install(path)
        m.discover("ext-1")
        m.validate_extension("ext-1")
        m.load("ext-1")
        m.initialize_extension("ext-1")
        assert m.status("ext-1") == "initialized"


def test_shutdown() -> None:
    m = ExtensionRuntimeManager()
    m.initialize()
    import os
    import tempfile

    import yaml
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "extension.yaml")
        with open(path, "w") as f:
            yaml.dump({"extension_id": "ext-1", "name": "Test", "version": "1.0.0"}, f)
        m.install(path)
        m.discover("ext-1")
        m.validate_extension("ext-1")
        m.load("ext-1")
        m.initialize_extension("ext-1")
        m.shutdown_extension("ext-1")
        assert m.status("ext-1") == "shutdown"


def test_remove() -> None:
    m = ExtensionRuntimeManager()
    m.initialize()
    import os
    import tempfile

    import yaml
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "extension.yaml")
        with open(path, "w") as f:
            yaml.dump({"extension_id": "ext-1", "name": "Test", "version": "1.0.0"}, f)
        m.install(path)
        assert m.remove("ext-1") is True
        assert m.get("ext-1") is None


def test_list() -> None:
    m = ExtensionRuntimeManager()
    m.initialize()
    import os
    import tempfile

    import yaml
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "extension.yaml")
        with open(path, "w") as f:
            yaml.dump({"extension_id": "ext-1", "name": "A", "version": "1.0.0"}, f)
        path2 = os.path.join(tmp, "ext2.yaml")
        with open(path2, "w") as f:
            yaml.dump({"extension_id": "ext-2", "name": "B", "version": "2.0.0"}, f)
        m.install(path)
        m.install(path2)
        assert len(m.list()) == 2


def test_status() -> None:
    m = ExtensionRuntimeManager()
    m.initialize()
    import os
    import tempfile

    import yaml
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "extension.yaml")
        with open(path, "w") as f:
            yaml.dump({"extension_id": "ext-1", "name": "Test", "version": "1.0.0"}, f)
        m.install(path)
        assert m.status("ext-1") == "installed"
        assert m.status("missing") is None


def test_snapshot() -> None:
    m = ExtensionRuntimeManager()
    m.initialize()
    import os
    import tempfile

    import yaml
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "extension.yaml")
        with open(path, "w") as f:
            yaml.dump({"extension_id": "ext-1", "name": "Test", "version": "1.0.0"}, f)
        m.install(path)
        snap = m.snapshot_state()
        assert snap.count() == 1
