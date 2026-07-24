from __future__ import annotations

from extensions.ecp.manifest import get_ecp_manifest
from extensions.sdk.manifest import ExtensionManifest


def test_get_ecp_manifest_returns_manifest() -> None:
    manifest = get_ecp_manifest()
    assert isinstance(manifest, ExtensionManifest)


def test_ecp_manifest_identity() -> None:
    manifest = get_ecp_manifest()
    assert manifest.extension_id == "ecp"
    assert manifest.name == "Engineering Control Plane"
    assert manifest.version == "0.1.0"


def test_ecp_manifest_author() -> None:
    manifest = get_ecp_manifest()
    assert manifest.author == "PortfolioAuthority"


def test_ecp_manifest_capabilities() -> None:
    manifest = get_ecp_manifest()
    assert "ecp.graph.manage" in manifest.capabilities
    assert "ecp.graph.validate" in manifest.capabilities
    assert "ecp.graph.resolve" in manifest.capabilities
    assert "ecp.governance.evidence" in manifest.capabilities
    assert "ecp.governance.decision" in manifest.capabilities


def test_ecp_manifest_permissions() -> None:
    manifest = get_ecp_manifest()
    assert len(manifest.permissions) == 1
    assert manifest.permissions[0].resource == "graph"
    assert "read" in manifest.permissions[0].actions
    assert "write" in manifest.permissions[0].actions
    assert "validate" in manifest.permissions[0].actions


def test_ecp_manifest_metadata() -> None:
    manifest = get_ecp_manifest()
    assert manifest.metadata["runtime_compatibility"] == ">=0.1.0,<1.0.0"
    assert manifest.metadata["owner"] == "PortfolioAuthority"


def test_ecp_manifest_sdk_compatibility() -> None:
    manifest = get_ecp_manifest()
    assert manifest.min_sdk_version == "0.1.0"
    assert manifest.max_sdk_version == "1.0.0"


def test_ecp_manifest_entry_point() -> None:
    manifest = get_ecp_manifest()
    assert manifest.entry_point == "extensions.ecp.adapter:ECPAdapter"


def test_ecp_manifest_no_dependencies() -> None:
    manifest = get_ecp_manifest()
    assert manifest.dependencies == ()
    assert manifest.optional_dependencies == ()
