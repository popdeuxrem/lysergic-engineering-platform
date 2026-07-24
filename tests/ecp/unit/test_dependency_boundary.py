from __future__ import annotations

import ast
from pathlib import Path

ECP_ROOT = Path(__file__).resolve().parent.parent.parent / "extensions" / "ecp"
ALLOWED_PREFIXES = ("extensions.sdk.", "runtime.api.", "extensions.ecp.")


def _ecp_modules() -> list[Path]:
    return [p for p in ECP_ROOT.rglob("*.py") if p.name != "__pycache__"]


def _imports_in(path: Path) -> list[ast.ImportFrom]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[ast.ImportFrom] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node)
    return imports


def _is_allowed(module: str) -> bool:
    if module.startswith(ALLOWED_PREFIXES) or module in ("extensions.sdk", "runtime.api", "extensions.ecp"):
        return True
    if module.startswith("typing.") or module in ("typing", "dataclasses", "datetime", "enum", "collections", "pathlib", "ast", "json"):
        return True
    return module == "__future__"


FORBIDDEN_PREFIXES = ("runtime.kernel", "runtime.services", "runtime.extensions")


def test_all_ecp_imports_use_allowed_dependencies() -> None:
    violations: list[str] = []
    for module_path in _ecp_modules():
        for imp in _imports_in(module_path):
            module = imp.module
            assert module is not None
            if not _is_allowed(module):
                violations.append(f"{module_path.relative_to(ECP_ROOT)}: {module}")
    assert not violations, "Disallowed imports found:\n" + "\n".join(violations)


def test_no_runtime_kernel_imports() -> None:
    violations: list[str] = []
    for module_path in _ecp_modules():
        for imp in _imports_in(module_path):
            module = imp.module
            assert module is not None
            for prefix in FORBIDDEN_PREFIXES:
                if module.startswith(prefix) or module == prefix:
                    violations.append(f"{module_path.relative_to(ECP_ROOT)}: {module}")
    assert not violations, "Forbidden runtime imports found:\n" + "\n".join(violations)
