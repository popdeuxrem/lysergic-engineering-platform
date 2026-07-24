from __future__ import annotations

from typing import Any

from cli.kilo.adapter import LEPAdapter
from cli.kilo.output import CLIError, detect_format, format_output


def cmd_version(lep: LEPAdapter, args: dict[str, Any]) -> str:
    fmt = args.get("format", detect_format())
    try:
        lep.lep.runtime.platform_version()
        data = lep.lep.version()
        return format_output(data, format=fmt)
    except Exception as e:  # noqa: BLE001
        err = CLIError(code="RUNTIME_UNAVAILABLE", message=str(e))
        return format_output(None, error=err, format=fmt)


def cmd_doctor(lep: LEPAdapter, args: dict[str, Any]) -> str:
    fmt = args.get("format", detect_format())
    try:
        snapshot = lep.lep.diagnostics.snapshot()
        data = {
            "ready": snapshot.get("ready", False),
            "health": snapshot.get("health", {}),
            "services": snapshot.get("services", {}),
            "lifecycle": snapshot.get("lifecycle", "unknown"),
            "errors": snapshot.get("errors", []),
        }
        return format_output(data, format=fmt)
    except Exception as e:  # noqa: BLE001
        err = CLIError(code="RUNTIME_UNAVAILABLE", message=str(e))
        return format_output(None, error=err, format=fmt)


def cmd_inspect(lep: LEPAdapter, args: dict[str, Any]) -> str:
    fmt = args.get("format", detect_format())
    try:
        summary = lep.lep.runtime.summary()
        telemetry = lep.lep.diagnostics.telemetry_summary()
        data = {
            "platform": summary,
            "telemetry": telemetry,
            "services": {"ids": lep.lep.runtime.service_ids(), "count": lep.lep.runtime.service_count()},
            "status": lep.lep.runtime.runtime_status(),
            "uptime": lep.lep.runtime.uptime(),
        }
        return format_output(data, format=fmt)
    except Exception as e:  # noqa: BLE001
        err = CLIError(code="RUNTIME_UNAVAILABLE", message=str(e))
        return format_output(None, error=err, format=fmt)


def cmd_validate(lep: LEPAdapter, args: dict[str, Any]) -> str:
    fmt = args.get("format", detect_format())
    try:
        snapshot = lep.lep.diagnostics.snapshot()
        ready = snapshot.get("ready", False)
        health = snapshot.get("health", {})
        overall = health.get("overall", "unknown") if isinstance(health, dict) else "unknown"
        errors_list = snapshot.get("errors", [])
        issues: list[str] = []
        if not ready:
            issues.append("Platform is not ready")
        if overall != "ready":
            issues.append(f"Health status: {overall}")
        if errors_list:
            issues.append(f"{len(errors_list)} recorded errors")
        valid = len(issues) == 0
        data = {"valid": valid, "ready": ready, "health": overall, "issues": issues}
        return format_output(data, format=fmt)
    except Exception as e:  # noqa: BLE001
        err = CLIError(code="RUNTIME_UNAVAILABLE", message=str(e))
        return format_output(None, error=err, format=fmt)
