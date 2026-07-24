from __future__ import annotations

from runtime.automation.exceptions import AutomationConflictError, RegistryFrozenError
from runtime.automation.model import Automation


class AutomationRegistry:
    def __init__(self) -> None:
        self._automations: dict[str, Automation] = {}
        self._frozen = False

    def register(self, automation: Automation) -> None:
        if self._frozen:
            raise RegistryFrozenError()
        if automation.automation_id in self._automations:
            raise AutomationConflictError(automation.automation_id)
        self._automations[automation.automation_id] = automation

    def get(self, automation_id: str) -> Automation | None:
        return self._automations.get(automation_id)

    def unregister(self, automation_id: str) -> bool:
        if self._frozen:
            raise RegistryFrozenError()
        return self._automations.pop(automation_id, None) is not None

    def list(self) -> tuple[Automation, ...]:
        return tuple(self._automations.values())

    def list_by_trigger(self, trigger_type: str) -> tuple[Automation, ...]:
        return tuple(a for a in self._automations.values() if any(t.trigger_type == trigger_type for t in a.triggers))

    def freeze(self) -> None:
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def count(self) -> int:
        return len(self._automations)

    def __contains__(self, automation_id: str) -> bool:
        return automation_id in self._automations
