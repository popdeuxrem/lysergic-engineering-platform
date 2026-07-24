from __future__ import annotations


class ECPLifecycle:
    def __init__(self) -> None:
        self._state: str = "installed"
        self._history: list[dict[str, str]] = []

    @property
    def state(self) -> str:
        return self._state

    @property
    def history(self) -> tuple[dict[str, str], ...]:
        return tuple(self._history)

    def discover(self) -> str:
        self._transition("discovered")
        return self._state

    def validate(self) -> str:
        self._transition("validated")
        return self._state

    def load(self) -> str:
        self._transition("loaded")
        return self._state

    def initialize(self) -> str:
        self._transition("initialized")
        return self._state

    def execute(self) -> str:
        self._transition("executing")
        return self._state

    def shutdown(self) -> str:
        self._transition("shutdown")
        return self._state

    def remove(self) -> str:
        self._transition("removed")
        return self._state

    def fail(self) -> str:
        self._transition("failed")
        return self._state

    def _transition(self, target: str) -> None:
        self._history.append({"from": self._state, "to": target})
        self._state = target
