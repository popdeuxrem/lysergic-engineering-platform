from __future__ import annotations

from typing import TYPE_CHECKING

from extensions.ecp.graph.entities import EntityRegistry
from extensions.ecp.graph.references import ReferenceResolver
from extensions.ecp.graph.relationships import RelationshipRegistry
from extensions.ecp.graph.validator import GraphValidator
from extensions.ecp.lifecycle import ECPLifecycle
from extensions.ecp.manifest import get_ecp_manifest
from extensions.ecp.validation.tier1 import Tier1Validator
from extensions.ecp.validation.tier2 import Tier2Validator
from extensions.sdk.extension import Extension, ExtensionHealth
from extensions.sdk.manifest import ExtensionManifest

if TYPE_CHECKING:
    from runtime.api import LEP


class ECPAdapter(Extension):
    extension_id: str = "ecp"

    def __init__(self, lep: LEP | None = None) -> None:
        self._lep = lep
        self._entities = EntityRegistry()
        self._relationships = RelationshipRegistry()
        self._references = ReferenceResolver()
        self._graph = GraphValidator(self._entities, self._relationships, self._references)
        self._tier1 = Tier1Validator()
        self._tier2 = Tier2Validator(self._entities, self._relationships, self._references)
        self._initialized = False
        self._lifecycle = ECPLifecycle()

    @property
    def entities(self) -> EntityRegistry:
        return self._entities

    @property
    def relationships(self) -> RelationshipRegistry:
        return self._relationships

    @property
    def references(self) -> ReferenceResolver:
        return self._references

    @property
    def graph(self) -> GraphValidator:
        return self._graph

    @property
    def tier1(self) -> Tier1Validator:
        return self._tier1

    @property
    def tier2(self) -> Tier2Validator:
        return self._tier2

    @property
    def manifest(self) -> ExtensionManifest:
        return get_ecp_manifest()

    @property
    def health(self) -> ExtensionHealth:
        return ExtensionHealth.HEALTHY if self._initialized else ExtensionHealth.UNKNOWN

    def get_metadata(self) -> dict[str, object]:
        return {
            "entity_count": self._entities.count,
            "relationship_count": self._relationships.count,
            "reference_count": self._references.count,
            "lifecycle_state": self._lifecycle.state,
        }

    def initialize(self) -> None:
        if self._initialized:
            return
        self._lifecycle.initialize()
        self._initialized = True

    def shutdown(self) -> None:
        self._lifecycle.shutdown()
        self._initialized = False

    @property
    def ready(self) -> bool:
        return self._initialized
