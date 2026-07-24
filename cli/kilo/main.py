#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from typing import Any, cast

from cli.kilo.adapter import LEPAdapter
from cli.kilo.commands import cmd_doctor, cmd_inspect, cmd_validate, cmd_version
from cli.kilo.output import CLIError, detect_format, format_output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lep", description="Lysergic Engineering Platform CLI")
    parser.add_argument("--format", choices=["text", "json"], default=None, help="Output format")
    sub = parser.add_subparsers(dest="command", required=True)

    p_version = sub.add_parser("version", help="Show platform version")
    p_version.add_argument("--format", choices=["text", "json"], default=None)

    p_doctor = sub.add_parser("doctor", help="Run platform diagnostics")
    p_doctor.add_argument("--format", choices=["text", "json"], default=None)

    p_inspect = sub.add_parser("inspect", help="Inspect platform state")
    p_inspect.add_argument("--format", choices=["text", "json"], default=None)

    p_validate = sub.add_parser("validate", help="Validate platform readiness")
    p_validate.add_argument("--format", choices=["text", "json"], default=None)

    return parser


def resolve_format(args: argparse.Namespace) -> str:
    if args.format:
        return cast(str, args.format)
    return detect_format()


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    fmt = resolve_format(args)
    cmd_args: dict[str, Any] = {"format": fmt}

    try:
        adapter = LEPAdapter()
        adapter.initialize()
    except Exception as e:  # noqa: BLE001
        output = format_output(None, error=CLIError(code="RUNTIME_UNAVAILABLE", message=f"Failed to initialize LEP: {e}"), format=fmt)
        print(output)
        sys.exit(5)

    try:
        if args.command == "version":
            output = cmd_version(adapter, cmd_args)
        elif args.command == "doctor":
            output = cmd_doctor(adapter, cmd_args)
        elif args.command == "inspect":
            output = cmd_inspect(adapter, cmd_args)
        elif args.command == "validate":
            output = cmd_validate(adapter, cmd_args)
        else:
            output = format_output(None, error=CLIError(code="INVALID_INPUT", message=f"Unknown command: {args.command}"), format=fmt)
            print(output)
            sys.exit(2)
    except Exception as e:  # noqa: BLE001
        output = format_output(None, error=CLIError(code="GENERAL_ERROR", message=str(e)), format=fmt)
        print(output)
        sys.exit(1)
    finally:
        adapter.shutdown()

    print(output)


if __name__ == "__main__":
    main()
