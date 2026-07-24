class AssetError(Exception):
    pass

class AssetNotFoundError(AssetError):
    def __init__(self, asset_id: str) -> None:
        self.asset_id = asset_id
        super().__init__(f"Asset not found: {asset_id}")

class AssetConflictError(AssetError):
    def __init__(self, asset_id: str) -> None:
        self.asset_id = asset_id
        super().__init__(f"Asset already exists: {asset_id}")

class AssetRegistrationFrozenError(AssetError):
    def __init__(self) -> None:
        super().__init__("Asset registry is frozen")

class InvalidLifecycleTransitionError(AssetError):
    def __init__(self, current: str, target: str) -> None:
        self.current = current
        self.target = target
        super().__init__(f"Invalid lifecycle transition: {current} -> {target}")

class DependencyCycleError(AssetError):
    def __init__(self, node: str) -> None:
        self.node = node
        super().__init__(f"Circular dependency detected: {node}")

class CacheInvalidError(AssetError):
    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(f"Cache entry invalid: {key}")

class ResolutionError(AssetError):
    def __init__(self, urn: str, message: str = "") -> None:
        self.urn = urn
        super().__init__(f"Resolution failed for {urn}: {message}")
