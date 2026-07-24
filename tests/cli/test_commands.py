
from typing import Any

from cli.kilo.commands import cmd_doctor, cmd_inspect, cmd_validate, cmd_version


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

    def version(self) -> dict[str, str]:
        return {"platform": "Lysergic Engineering Platform", "version": "0.1.0", "architecture": "LEP-ARCH-v0.1.0"}

    def health(self) -> dict[str, Any]:
        return {"status": "ready", "ready": 1, "total": 1, "services": {}}

    def summary(self) -> dict[str, Any]:
        return {"platform": "Lysergic Engineering Platform", "version": "0.1.0", "ready": True}

    @property
    def runtime(self):
        return self

    @property
    def diagnostics(self):
        return self

    def runtime_status(self) -> dict[str, Any]:
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

    def service_ids(self) -> tuple[str, ...]:
        return ("api.runtime", "api.diagnostics", "api.validation")

    def service_count(self) -> int:
        return 3

    def is_governance_enabled(self) -> bool:
        return True

    def snapshot(self) -> dict[str, Any]:
        return {
            "ready": True,
            "health": {"overall": "ready", "ready": 1, "total": 1},
            "services": {"registered": ["api.runtime"], "instances": [], "count": 1},
            "lifecycle": "ready",
            "errors": [],
        }

    def telemetry_summary(self) -> dict[str, Any]:
        return {"event_count": 0, "subscriber_count": 0, "errors": []}

    def is_healthy(self) -> bool:
        return True


class FakeAdapter:
    def __init__(self) -> None:
        self._lep = FakeLEP()

    def initialize(self) -> FakeLEP:
        return self._lep

    def shutdown(self) -> None:
        pass

    @property
    def lep(self) -> FakeLEP:
        return self._lep


def test_cmd_version_text() -> None:
    adapter = FakeAdapter()
    output = cmd_version(adapter, {"format": "text"})
    assert "Lysergic Engineering Platform" in output


def test_cmd_version_json() -> None:
    adapter = FakeAdapter()
    import json
    output = cmd_version(adapter, {"format": "json"})
    parsed = json.loads(output)
    assert parsed["status"] == "success"
    assert parsed["data"]["version"] == "0.1.0"


def test_cmd_doctor_text() -> None:
    adapter = FakeAdapter()
    output = cmd_doctor(adapter, {"format": "text"})
    assert "ready" in output.lower() or "True" in output


def test_cmd_doctor_json() -> None:
    adapter = FakeAdapter()
    import json
    output = cmd_doctor(adapter, {"format": "json"})
    parsed = json.loads(output)
    assert parsed["status"] == "success"
    assert "ready" in parsed["data"]


def test_cmd_inspect_text() -> None:
    adapter = FakeAdapter()
    output = cmd_inspect(adapter, {"format": "text"})
    assert "Lysergic Engineering Platform" in output


def test_cmd_inspect_json() -> None:
    adapter = FakeAdapter()
    import json
    output = cmd_inspect(adapter, {"format": "json"})
    parsed = json.loads(output)
    assert parsed["status"] == "success"
    assert "telemetry" in parsed["data"]


def test_cmd_validate_text() -> None:
    adapter = FakeAdapter()
    output = cmd_validate(adapter, {"format": "text"})
    assert "valid" in output.lower() or "True" in output


def test_cmd_validate_json() -> None:
    adapter = FakeAdapter()
    import json
    output = cmd_validate(adapter, {"format": "json"})
    parsed = json.loads(output)
    assert parsed["status"] == "success"
    assert "valid" in parsed["data"]
