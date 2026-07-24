class KnowledgeError(Exception):
    pass

class KnowledgeNotFoundError(KnowledgeError):
    def __init__(self, knowledge_id: str) -> None:
        self.knowledge_id = knowledge_id
        super().__init__(f"Knowledge not found: {knowledge_id}")

class KnowledgeConflictError(KnowledgeError):
    def __init__(self, knowledge_id: str) -> None:
        self.knowledge_id = knowledge_id
        super().__init__(f"Knowledge already exists: {knowledge_id}")

class InvalidLifecycleTransitionError(KnowledgeError):
    def __init__(self, current: str, target: str) -> None:
        self.current = current
        self.target = target
        super().__init__(f"Invalid transition: {current} -> {target}")

class RegistryFrozenError(KnowledgeError):
    def __init__(self) -> None:
        super().__init__("Knowledge registry is frozen")

class IngestionError(KnowledgeError):
    def __init__(self, source: str, message: str) -> None:
        super().__init__(f"Ingestion failed from '{source}': {message}")

class ValidationError(KnowledgeError):
    def __init__(self, knowledge_id: str, errors: tuple[str, ...]) -> None:
        self.knowledge_id = knowledge_id
        self.errors = errors
        super().__init__(f"Validation failed for '{knowledge_id}': {'; '.join(errors)}")
