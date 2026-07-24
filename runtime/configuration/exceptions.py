class ConfigurationError(Exception):
    pass

class ProviderNotFoundError(ConfigurationError):
    def __init__(self, provider_id: str) -> None:
        self.provider_id = provider_id
        super().__init__(f"Configuration provider not found: {provider_id}")

class ProfileNotFoundError(ConfigurationError):
    def __init__(self, profile_id: str) -> None:
        self.profile_id = profile_id
        super().__init__(f"Configuration profile not found: {profile_id}")

class ValidationError(ConfigurationError):
    def __init__(self, message: str, errors: tuple[str, ...] = ()) -> None:
        self.errors = errors
        super().__init__(message)

class MergeConflictError(ConfigurationError):
    def __init__(self, key: str, left: object, right: object) -> None:
        self.key = key
        self.left = left
        self.right = right
        super().__init__(f"Merge conflict at '{key}': {left!r} vs {right!r}")

class SnapshotFrozenError(ConfigurationError):
    def __init__(self) -> None:
        super().__init__("Configuration snapshot is frozen and cannot be modified")

class WatchError(ConfigurationError):
    pass
