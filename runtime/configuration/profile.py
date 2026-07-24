from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from runtime.configuration.merge import deep_merge


@dataclass
class ProfileDefinition:
    profile_id: str
    name: str
    description: str = ""
    parent: str | None = None
    config: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class ProfileManager:
    def __init__(self) -> None:
        self._profiles: dict[str, ProfileDefinition] = {}
        self._active: str | None = None

    def define(self, profile: ProfileDefinition) -> None:
        if profile.profile_id in self._profiles:
            raise ValueError(f"Profile '{profile.profile_id}' already defined")
        self._profiles[profile.profile_id] = profile

    def activate(self, profile_id: str) -> None:
        if profile_id not in self._profiles:
            from runtime.configuration.exceptions import ProfileNotFoundError
            raise ProfileNotFoundError(profile_id)
        self._active = profile_id

    def get(self, profile_id: str) -> ProfileDefinition | None:
        return self._profiles.get(profile_id)

    def delete(self, profile_id: str) -> bool:
        if profile_id == self._active:
            self._active = None
        return self._profiles.pop(profile_id, None) is not None

    def resolved_config(self, profile_id: str | None = None) -> dict[str, Any]:
        pid = profile_id or self._active
        if pid is None:
            return {}
        visited: set[str] = set()
        config: dict[str, Any] = {}

        def walk(current_id: str) -> None:
            if current_id in visited:
                return
            visited.add(current_id)
            profile = self._profiles.get(current_id)
            if profile is None:
                return
            if profile.parent:
                walk(profile.parent)
            nonlocal config
            config = deep_merge(config, profile.config)

        walk(pid)
        return config

    @property
    def active(self) -> str | None:
        return self._active

    @property
    def profiles(self) -> dict[str, ProfileDefinition]:
        return dict(self._profiles)

    @property
    def count(self) -> int:
        return len(self._profiles)

    def __contains__(self, profile_id: str) -> bool:
        return profile_id in self._profiles
