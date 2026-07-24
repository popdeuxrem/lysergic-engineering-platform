class ExtensionRuntimeError(Exception):
    pass

class ExtensionRuntimeNotFoundError(ExtensionRuntimeError):
    def __init__(self, extension_id: str) -> None:
        self.extension_id = extension_id
        super().__init__(f"Extension not found: {extension_id}")

class ExtensionRuntimeConflictError(ExtensionRuntimeError):
    def __init__(self, extension_id: str) -> None:
        self.extension_id = extension_id
        super().__init__(f"Extension already registered: {extension_id}")

class InvalidLifecycleTransitionError(ExtensionRuntimeError):
    def __init__(self, current: str, target: str) -> None:
        super().__init__(f"Invalid lifecycle transition: {current} -> {target}")

class ManifestValidationError(ExtensionRuntimeError):
    def __init__(self, extension_id: str, errors: tuple[str, ...]) -> None:
        self.extension_id = extension_id
        self.errors = errors
        super().__init__(f"Manifest validation failed for '{extension_id}': {'; '.join(errors)}")

class RegistryFrozenError(ExtensionRuntimeError):
    def __init__(self) -> None:
        super().__init__("Extension registry is frozen")
