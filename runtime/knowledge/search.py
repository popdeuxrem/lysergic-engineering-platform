from __future__ import annotations

from typing import Any

from runtime.knowledge.catalog import KnowledgeCatalog


class KnowledgeSearch:
    def __init__(self, catalog: KnowledgeCatalog) -> None:
        self._catalog = catalog

    def search(self, query: str, kind: str | None = None) -> tuple[dict[str, Any], ...]:
        q = query.lower()
        results = list(self._catalog.entries)
        results = [r for r in results if q in r["title"].lower() or q in r["description"].lower() or any(q in t.lower() for t in r["tags"])]
        if kind is not None:
            results = [r for r in results if r["kind"] == kind]
        return tuple(results)

    def search_by_tag(self, tag: str) -> tuple[dict[str, Any], ...]:
        return self._catalog.filter(tag=tag)

    def search_by_kind(self, kind: str) -> tuple[dict[str, Any], ...]:
        return self._catalog.filter(kind=kind)
