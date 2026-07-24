from __future__ import annotations

from runtime.api import LEP, create_default_lep


class LEPAdapter:
    def __init__(self) -> None:
        self._lep: LEP | None = None

    def initialize(self) -> LEP:
        lep = create_default_lep()
        self._lep = lep
        return lep

    def shutdown(self) -> None:
        if self._lep is not None:
            self._lep.stop()

    @property
    def lep(self) -> LEP:
        if self._lep is None:
            raise RuntimeError("LEP not initialized. Call initialize() first.")
        return self._lep
