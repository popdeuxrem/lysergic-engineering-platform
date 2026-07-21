class DomainException(Exception):
    pass


class EntityNotFoundError(DomainException):
    def __init__(self, entity_type: str, entity_id: str) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with id {entity_id} not found")


class ValidationError(DomainException):
    def __init__(self, message: str) -> None:
        super().__init__(message)
