from cli.kilo.adapter import LEPAdapter


class FakeLEP:
    def __init__(self) -> None:
        self._started = False

    def start(self) -> None:
        self._started = True

    def stop(self) -> None:
        self._started = False

    @property
    def ready(self) -> bool:
        return self._started

    def version(self) -> dict:
        return {"platform": "Lysergic Engineering Platform", "version": "0.1.0", "architecture": "LEP-ARCH-v0.1.0"}

    def health(self) -> dict:
        return {"status": "ready", "ready": 1, "total": 1, "services": {}}

    def summary(self) -> dict:
        return {"platform": "Lysergic Engineering Platform", "version": "0.1.0", "ready": True}

    @property
    def runtime(self):
        return self

    @property
    def diagnostics(self):
        return self

    def runtime_status(self) -> dict:
        return {"ready": True, "health": "ready", "lifecycle": "ready"}

    def uptime(self) -> str:
        return "1h 30m"

    def platform_name(self) -> str:
        return "Lysergic Engineering Platform"

    def platform_version(self) -> str:
        return "0.1.0"

    def architecture_id(self) -> str:
        return "LEP-ARCH-v0.1.0"

    def architecture_status(self) -> str:
        return "frozen"

    def schema_dialect(self) -> str:
        return "draft2020-12"

    def service_ids(self) -> tuple:
        return ("api.runtime", "api.diagnostics", "api.validation")

    def service_count(self) -> int:
        return 3

    def is_governance_enabled(self) -> bool:
        return True

    def snapshot(self) -> dict:
        return {
            "ready": True,
            "health": {"overall": "ready", "ready": 1, "total": 1},
            "services": {"registered": ["api.runtime"], "instances": [], "count": 1},
            "lifecycle": "ready",
            "errors": [],
        }

    def telemetry_summary(self) -> dict:
        return {"event_count": 0, "subscriber_count": 0, "errors": []}

    def is_healthy(self) -> bool:
        return True


def test_adapter_initialize() -> None:
    adapter = LEPAdapter()
    lep = adapter.initialize()
    assert lep is not None
    adapter.shutdown()


def test_adapter_not_initialized() -> None:
    adapter = LEPAdapter()
    try:
        _ = adapter.lep
        assert False
    except RuntimeError:
        pass


def test_adapter_double_initialize() -> None:
    adapter = LEPAdapter()
    adapter.initialize()
    adapter.initialize()
    adapter.shutdown()
