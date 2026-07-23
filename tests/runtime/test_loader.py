import tempfile
from pathlib import Path

from runtime.kernel.loader import KernelConfig, KernelLoader

SAMPLE_MANIFEST = {
    "platform": {
        "name": "Lysergic Engineering Platform",
        "identifier": "lep",
        "version": "0.1.0",
    },
    "architecture": {
        "baseline": {
            "id": "LEP-ARCH-v0.1.0",
            "status": "frozen",
        },
    },
    "metamodel": {
        "ecp": {
            "version": "0.1.0",
            "status": "baseline",
        },
    },
    "runtime": {
        "execution_model": {
            "enabled": True,
        },
    },
    "validation": {
        "schema": {
            "dialect": "draft2020-12",
        },
    },
    "governance": {
        "artifact_lifecycle": {
            "enabled": True,
        },
    },
}


def test_loader_creates_config_from_manifest() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        manifest_path = Path(tmpdir) / "lep.yaml"
        import yaml
        with open(manifest_path, "w") as f:
            yaml.dump(SAMPLE_MANIFEST, f)

        loader = KernelLoader(manifest_path)
        config = loader.load()

        assert isinstance(config, KernelConfig)
        assert config.platform_name == "Lysergic Engineering Platform"
        assert config.platform_identifier == "lep"
        assert config.platform_version == "0.1.0"
        assert config.architecture_baseline_id == "LEP-ARCH-v0.1.0"
        assert config.architecture_status == "frozen"
        assert config.metamodel_ecp_version == "0.1.0"
        assert config.schema_dialect == "draft2020-12"
        assert config.governance_enabled is True
        assert config.runtime_enabled is True


def test_loader_is_idempotent() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        manifest_path = Path(tmpdir) / "lep.yaml"
        import yaml
        with open(manifest_path, "w") as f:
            yaml.dump(SAMPLE_MANIFEST, f)

        loader = KernelLoader(manifest_path)
        config1 = loader.load()
        config2 = loader.load()

        assert config1 is config2
        assert loader.loaded is True


def test_loader_raises_on_missing_manifest() -> None:
    loader = KernelLoader("/nonexistent/path/lep.yaml")
    try:
        loader.load()
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass


def test_loader_config_property_before_load() -> None:
    loader = KernelLoader()
    try:
        _ = loader.config
        assert False, "Expected RuntimeError"
    except RuntimeError:
        pass
