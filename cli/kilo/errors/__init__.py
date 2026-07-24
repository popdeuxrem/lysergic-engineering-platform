from __future__ import annotations

from cli.kilo.output import EXIT_CODES, CLIError


class CommandError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


def exit_code_for(error_code: str) -> int:
    return EXIT_CODES.get(error_code, 1)


def cli_error_to_exit(error: CLIError) -> int:
    return EXIT_CODES.get(error.code, 1)
