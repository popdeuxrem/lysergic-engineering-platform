from __future__ import annotations

import re


class CompatibilityChecker:
    def __init__(self) -> None:
        self._sdk_version = "1.0.0"

    def check_sdk_compatibility(self, manifest_min_sdk: str, manifest_max_sdk: str | None = None) -> tuple[bool, str]:
        if not self._satisfies(manifest_min_sdk, self._sdk_version):
            return False, f"Extension requires SDK >= {manifest_min_sdk}, current is {self._sdk_version}"
        if manifest_max_sdk is not None and not self._satisfies(self._sdk_version, manifest_max_sdk):
            return False, f"Extension requires SDK <= {manifest_max_sdk}, current is {self._sdk_version}"
        return True, ""

    def check_dependency_compatibility(self, provider_version: str, required_version: str) -> tuple[bool, str]:
        if not self._satisfies(required_version, provider_version):
            return False, f"Provider version {provider_version} does not satisfy requirement {required_version}"
        return True, ""

    def _satisfies(self, required: str, actual: str) -> bool:
        req_parts = self._parse(required)
        act_parts = self._parse(actual)
        if req_parts is None or act_parts is None:
            return False
        return act_parts >= req_parts

    def _parse(self, version: str) -> tuple[int, int, int] | None:
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version.strip())
        if not match:
            return None
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
