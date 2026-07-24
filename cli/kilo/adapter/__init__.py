from __future__ import annotations

from runtime.api import LEP
from runtime.services.events import EventBus
from runtime.services.health import HealthService
from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceRegistry
from runtime.services.resolver import DependencyResolver


class LEPAdapter:
    def __init__(self) -> None:
        self._registry: ServiceRegistry | None = None
        self._manager: ServiceManager | None = None
        self._lep: LEP | None = None

    def initialize(self) -> LEP:
        registry = ServiceRegistry()
        resolver = DependencyResolver()
        health = HealthService()
        event_bus = EventBus()
        manager = ServiceManager(registry=registry, resolver=resolver, health=health, event_bus=event_bus)
        lep = LEP(manager)
        lep.start()
        self._registry = registry
        self._manager = manager
        self._lep = lep
        return lep

    def shutdown(self) -> None:
        if self._lep is not None:
            self._lep.stop()

    @property
    def lep(self) -> LEP:
        if self._lep is None:
            raise RuntimeError("LEP not initialized. Call initialize() first.")
        return self._lep

    @property
    def manager(self) -> ServiceManager:
        if self._manager is None:
            raise RuntimeError("LEP not initialized. Call initialize() first.")
        return self._manager
