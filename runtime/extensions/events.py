from __future__ import annotations

from runtime.api import publish_event


class ExtensionRuntimeEventPublisher:
    def installed(self, extension_id: str) -> None:
        publish_event("ext.ExtensionInstalled", {"extension_id": extension_id}, source="extensions.runtime")

    def discovered(self, extension_id: str) -> None:
        publish_event("ext.ExtensionDiscovered", {"extension_id": extension_id}, source="extensions.runtime")

    def validated(self, extension_id: str) -> None:
        publish_event("ext.ExtensionValidated", {"extension_id": extension_id}, source="extensions.runtime")

    def loaded(self, extension_id: str) -> None:
        publish_event("ext.ExtensionLoaded", {"extension_id": extension_id}, source="extensions.runtime")

    def initialized(self, extension_id: str) -> None:
        publish_event("ext.ExtensionInitialized", {"extension_id": extension_id}, source="extensions.runtime")

    def shutdown(self, extension_id: str) -> None:
        publish_event("ext.ExtensionShutdown", {"extension_id": extension_id}, source="extensions.runtime")

    def removed(self, extension_id: str) -> None:
        publish_event("ext.ExtensionRemoved", {"extension_id": extension_id}, source="extensions.runtime")

    def failed(self, extension_id: str, error: str) -> None:
        publish_event("ext.ExtensionFailed", {"extension_id": extension_id, "error": error}, source="extensions.runtime")
