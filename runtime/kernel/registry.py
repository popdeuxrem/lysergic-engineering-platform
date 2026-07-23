from __future__ import annotations

from typing import Protocol, TypeVar

T = TypeVar("T")


class Component(Protocol):
    component_id: str

    def initialize(self) -> None: ...

    def shutdown(self) -> None: ...


C = TypeVar("C", bound=Component)


class ComponentRegistry[C: Component]:
    def __init__(self) -> None:
        self._components: dict[str, C] = {}
        self._frozen = False
        self._initialization_order: list[str] = []

    def register(self, component: C) -> None:
        if self._frozen:
            raise RuntimeError(
                f"Cannot register {component.component_id}: registry is frozen"
            )
        if component.component_id in self._components:
            raise ValueError(
                f"Component '{component.component_id}' is already registered"
            )
        self._components[component.component_id] = component
        self._initialization_order.append(component.component_id)

    def resolve(self, component_id: str) -> C:
        if component_id not in self._components:
            raise KeyError(f"Component '{component_id}' not found in registry")
        return self._components[component_id]

    def freeze(self) -> None:
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def components(self) -> dict[str, C]:
        return dict(self._components)

    @property
    def initialization_order(self) -> list[str]:
        return list(self._initialization_order)

    def initialize_all(self) -> None:
        for cid in self._initialization_order:
            self._components[cid].initialize()
        self.freeze()

    def shutdown_all(self) -> None:
        for cid in reversed(self._initialization_order):
            self._components[cid].shutdown()

    def __contains__(self, component_id: str) -> bool:
        return component_id in self._components

    def __len__(self) -> int:
        return len(self._components)
