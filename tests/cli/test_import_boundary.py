"""Verify that cli/kilo/ maintains LEP architecture boundaries.

Architecture requirement:
  cli/kilo
      ↓
  runtime.api  (only)
      ↓
  runtime

No CLI component may directly depend on:
  - runtime.kernel
  - runtime.services
  - any internal runtime module
  - contracts, schemas, profiles, extensions, apps
"""

import ast
import pathlib


KILO_PACKAGE = pathlib.Path("cli/kilo")

PROHIBITED_IMPORTS = [
    "runtime.kernel", "runtime.services", "runtime.assets",
    "runtime.ai", "runtime.workflows", "runtime.plugins",
    "runtime.projects", "runtime.knowledge", "runtime.automation",
    "runtime.operations", "runtime.configuration", "runtime.telemetry",
    "runtime.validator",
    "contracts", "schemas", "profiles", "extensions", "apps",
]


def _get_all_kilo_py_files() -> list[pathlib.Path]:
    return sorted(KILO_PACKAGE.rglob("*.py"))


def _get_imports_from_file(path: pathlib.Path) -> list[tuple[str, str]]:
    """Return list of (module, name) for all imports found in file."""
    with open(path) as f:
        tree = ast.parse(f.read(), filename=str(path))

    imports: list[tuple[str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((alias.name, ""))
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                imports.append((node.module, alias.name or ""))
    return imports


def test_no_kilo_module_imports_prohibited_modules() -> None:
    """Every .py file under cli/kilo/ is scanned for prohibited imports."""
    errors = []
    for path in _get_all_kilo_py_files():
        rel = path.relative_to(KILO_PACKAGE)
        for mod, _ in _get_imports_from_file(path):
            for prohibited in PROHIBITED_IMPORTS:
                if mod == prohibited or mod.startswith(prohibited + "."):
                    errors.append(f"{rel}: imports {mod}")
    assert not errors, (
        "Kilo modules must not import runtime internals directly:\n"
        + "\n".join(errors)
    )


def test_adapter_imports_only_from_runtime_api() -> None:
    """The adapter module must only import runtime.api (not runtime.services)."""
    adapter_path = KILO_PACKAGE / "adapter" / "__init__.py"
    assert adapter_path.exists(), f"Adapter module missing at {adapter_path}"

    imports_runtime_api = False
    imports_runtime_services = False
    for mod, _ in _get_imports_from_file(adapter_path):
        if mod == "runtime.api" or mod.startswith("runtime.api."):
            imports_runtime_api = True
        if mod == "runtime.services" or mod.startswith("runtime.services."):
            imports_runtime_services = True

    assert imports_runtime_api, "Adapter must import from runtime.api (LEP facade)"
    assert not imports_runtime_services, (
        "Adapter must NOT import from runtime.services directly. "
        "Use create_default_lep() from runtime.api instead."
    )
