from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


class CapabilityProvider(Protocol):
    capability_id: str
    version: str

    def execute(self, **kwargs: Any) -> Any: ...

    @property
    def metadata(self) -> dict[str, Any]: ...


@dataclass
class CapabilityRegistration:
    capability_id: str
    provider_id: str
    version: str
    provider: CapabilityProvider | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class CapabilityRegistry:
    def __init__(self) -> None:
        self._registrations: dict[str, list[CapabilityRegistration]] = {}

    def register(self, registration: CapabilityRegistration) -> None:
        cid = registration.capability_id
        if cid not in self._registrations:
            self._registrations[cid] = []
        for existing in self._registrations[cid]:
            if existing.provider_id == registration.provider_id and existing.version == registration.version:
                raise ValueError(f"Duplicate provider '{registration.provider_id}' for capability '{cid}' version {registration.version}")
        self._registrations[cid].append(registration)

    def resolve(self, capability_id: str, version: str | None = None) -> list[CapabilityRegistration]:
        registrations = self._registrations.get(capability_id, [])
        if version is None:
            return list(registrations)
        return [r for r in registrations if r.version == version]

    def resolve_best(self, capability_id: str) -> CapabilityRegistration | None:
        registrations = self._registrations.get(capability_id, [])
        if not registrations:
            return None
        return max(registrations, key=lambda r: r.version)

    def providers_for(self, capability_id: str) -> list[str]:
        return [r.provider_id for r in self._registrations.get(capability_id, [])]

    def capabilities_for(self, provider_id: str) -> list[str]:
        return [cid for cid, regs in self._registrations.items() for r in regs if r.provider_id == provider_id]

    def remove_provider(self, capability_id: str, provider_id: str) -> bool:
        if capability_id not in self._registrations:
            return False
        before = len(self._registrations[capability_id])
        self._registrations[capability_id] = [r for r in self._registrations[capability_id] if r.provider_id != provider_id]
        return len(self._registrations[capability_id]) < before

    @property
    def capability_ids(self) -> tuple[str, ...]:
        return tuple(self._registrations.keys())

    @property
    def registration_count(self) -> int:
        return sum(len(regs) for regs in self._registrations.values())
