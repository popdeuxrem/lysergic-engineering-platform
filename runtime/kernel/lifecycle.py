from __future__ import annotations

from collections.abc import Callable
from enum import Enum


class LifecycleState(Enum):
    CREATED = "created"
    INITIALIZING = "initializing"
    READY = "ready"
    STOPPING = "stopping"
    STOPPED = "stopped"


class LifecycleManager:
    def __init__(self) -> None:
        self._state = LifecycleState.CREATED
        self._start_hooks: list[Callable[[], None]] = []
        self._stop_hooks: list[Callable[[], None]] = []

    @property
    def state(self) -> LifecycleState:
        return self._state

    def add_start_hook(self, hook: Callable[[], None]) -> None:
        self._start_hooks.append(hook)

    def add_stop_hook(self, hook: Callable[[], None]) -> None:
        self._stop_hooks.append(hook)

    def start(self) -> None:
        if self._state == LifecycleState.READY:
            return
        if self._state != LifecycleState.CREATED:
            raise RuntimeError(
                f"Cannot start from state: {self._state.value}"
            )
        self._state = LifecycleState.INITIALIZING
        for hook in self._start_hooks:
            hook()
        self._state = LifecycleState.READY

    def stop(self) -> None:
        if self._state == LifecycleState.STOPPED:
            return
        if self._state != LifecycleState.READY:
            raise RuntimeError(
                f"Cannot stop from state: {self._state.value}"
            )
        self._state = LifecycleState.STOPPING
        for hook in reversed(self._stop_hooks):
            hook()
        self._state = LifecycleState.STOPPED

    def is_ready(self) -> bool:
        return self._state == LifecycleState.READY

    def is_stopped(self) -> bool:
        return self._state == LifecycleState.STOPPED
