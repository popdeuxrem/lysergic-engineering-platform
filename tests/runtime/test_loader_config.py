from __future__ import annotations

from runtime.kernel.loader import KernelConfig


def test_kernel_config_frozen() -> None:
    config = KernelConfig(
        platform_name="test",
        platform_identifier="t",
        platform_version="1.0.0",
        architecture_baseline_id="ARCH-001",
        architecture_status="frozen",
        metamodel_ecp_version="0.1.0",
        metamodel_ecp_status="baseline",
        schema_dialect="draft2020-12",
        governance_enabled=True,
        runtime_enabled=True,
    )
    assert config.platform_name == "test"
