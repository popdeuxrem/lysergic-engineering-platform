from typing import Any

from runtime.kernel.lifecycle import LifecycleManager
from runtime.kernel.loader import KernelLoader
from runtime.kernel.registry import ComponentRegistry


def create_runtime(manifest_path: str = "lep.yaml") -> tuple[KernelLoader, ComponentRegistry[Any], LifecycleManager]:
    loader = KernelLoader(manifest_path)
    loader.load()

    registry: ComponentRegistry[Any] = ComponentRegistry()
    lifecycle = LifecycleManager()

    return loader, registry, lifecycle
