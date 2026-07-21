from abc import ABC, abstractmethod
from typing import Protocol, TypeVar

from src.domain.entities import Entity

TEntity = TypeVar("TEntity", bound=Entity)
TId_contra = TypeVar("TId_contra", contravariant=True)


class Repository(Protocol[TEntity, TId_contra]):
    """Repository protocol for domain entity persistence.

    Implementations belong in the infrastructure layer.
    """

    async def get_by_id(self, entity_id: TId_contra) -> TEntity | None: ...
    async def save(self, entity: TEntity) -> None: ...
    async def delete(self, entity: TEntity) -> None: ...


class UseCase(ABC):
    """Base class for application use cases (service operations).

    Use cases orchestrate domain entities and repositories to fulfill
    application commands and queries.
    """

    @abstractmethod
    async def execute(self) -> object:
        pass
