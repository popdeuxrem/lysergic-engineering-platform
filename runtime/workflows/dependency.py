from __future__ import annotations


class WorkflowDependencyValidator:
    def __init__(self) -> None:
        self._required_assets: dict[str, tuple[str, ...]] = {}

    def require_asset(self, workflow_id: str, asset_ids: tuple[str, ...]) -> None:
        self._required_assets[workflow_id] = asset_ids

    def validate_assets(self, workflow_id: str, available_assets: set[str]) -> list[str]:
        errors: list[str] = []
        required = self._required_assets.get(workflow_id, ())
        for asset_id in required:
            if asset_id not in available_assets:
                errors.append(f"Required asset not available: {asset_id}")
        return errors

    def validate_capabilities(self, workflow_id: str, available_capabilities: set[str], required_capabilities: tuple[str, ...]) -> list[str]:
        errors: list[str] = []
        for cap in required_capabilities:
            if cap not in available_capabilities:
                errors.append(f"Required capability not available: {cap}")
        return errors
