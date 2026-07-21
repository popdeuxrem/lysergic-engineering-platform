from abc import ABC
from collections.abc import Hashable
from typing import TypeVar

TEntityId = TypeVar("TEntityId", bound=Hashable)


class Entity(ABC):
    """Base class for domain entities.

    Entities carry identity and are compared by identity, not structural equality.
    """

    _id: Hashable

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented
        return bool(self._id == other._id)

    def __hash__(self) -> int:
        return hash(self._id)
