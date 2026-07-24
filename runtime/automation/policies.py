from __future__ import annotations

from runtime.automation.exceptions import PolicyDeniedError
from runtime.automation.model import Automation


class PolicyEngine:
    def __init__(self) -> None:
        self._global_allowed_targets: set[str] = {"workflow", "ai", "plugin"}

    def check_execution(self, automation: Automation) -> None:
        policy = automation.policy
        for action in automation.actions:
            if action.target not in policy.allowed_targets:
                raise PolicyDeniedError(automation.automation_id, f"target '{action.target}' not allowed")
            if action.target not in self._global_allowed_targets:
                raise PolicyDeniedError(automation.automation_id, f"global target '{action.target}' not allowed")
        if policy.max_executions > 0:
            pass

    def is_action_allowed(self, target: str) -> bool:
        return target in self._global_allowed_targets
