from __future__ import annotations

from extensions.sdk.manifest import ExtensionManifest, ExtensionPermission


def get_ecp_manifest() -> ExtensionManifest:
    return ExtensionManifest(
        extension_id="ecp",
        name="Engineering Control Plane",
        version="0.1.0",
        description="The Engineering Control Plane provides governance graph semantics for the LEP platform, including entity management, relationship management, reference resolution, and graph validation.",
        author="PortfolioAuthority",
        dependencies=(),
        optional_dependencies=(),
        capabilities=(
            "ecp.graph.manage",
            "ecp.graph.validate",
            "ecp.graph.resolve",
            "ecp.governance.evidence",
            "ecp.governance.decision",
        ),
        permissions=(
            ExtensionPermission(resource="graph", actions=("read", "write", "validate")),
        ),
        min_sdk_version="0.1.0",
        max_sdk_version="1.0.0",
        entry_point="extensions.ecp.adapter:ECPAdapter",
        homepage="",
        license="",
        metadata={
            "runtime_compatibility": ">=0.1.0,<1.0.0",
            "owner": "PortfolioAuthority",
        },
    )
