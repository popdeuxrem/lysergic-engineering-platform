"""Verify architecture boundaries for cli/kilo/ and runtime/extensions/.

Architecture requirement:
  cli/kilo  │  runtime/extensions
      ↓     │       ↓
  runtime.api (only) │ runtime.api + extensions.sdk
      ↓     │       ↓
  runtime  │  runtime
"""

import ast
import pathlib


PACKAGES = {
    "cli/kilo": pathlib.Path("cli/kilo"),
    "runtime/extensions": pathlib.Path("runtime/extensions"),
}

PROHIBITED_IMPORTS = [
    "runtime.kernel", "runtime.services", "runtime.assets",
    "runtime.ai", "runtime.workflows", "runtime.plugins",
    "runtime.projects", "runtime.knowledge", "runtime.automation",
    "runtime.operations", "runtime.configuration", "runtime.telemetry",
    "runtime.validator",
    "contracts", "schemas", "profiles", "extensions", "apps",
]

# Each package has an allowlist of module prefixes that are permitted
ALLOWED_PREFIXES = {
    "cli/kilo": ["runtime.api"],
    "runtime/extensions": ["runtime.api", "extensions.sdk"],
}


def _get_all_py_files(pkg_path: pathlib.Path) -> list[pathlib.Path]:
    return sorted(pkg_path.rglob("*.py"))


def _get_imports_from_file(path: pathlib.Path) -> list[tuple[str, str]]:
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


def _is_allowed(mod: str, pkg_name: str) -> bool:
    for prefix in ALLOWED_PREFIXES.get(pkg_name, []):
        if mod == prefix or mod.startswith(prefix + "."):
            return True
    return False


def test_no_module_imports_prohibited_modules() -> None:
    """Every .py file under cli/kilo/ and runtime/extensions/ is scanned."""
    errors = []
    for pkg_name, pkg_path in PACKAGES.items():
        for path in _get_all_py_files(pkg_path):
            rel = path.relative_to(pkg_path)
            for mod, _ in _get_imports_from_file(path):
                is_prohibited = any(
                    mod == p or mod.startswith(p + ".") for p in PROHIBITED_IMPORTS
                )
                if is_prohibited and not _is_allowed(mod, pkg_name):
                    errors.append(f"{pkg_name}/{rel}: imports {mod}")
    assert not errors, (
        "Modules must not import prohibited runtime internals:\n"
        + "\n".join(errors)
    )


def test_adapter_imports_only_from_runtime_api() -> None:
    """Kilo adapter must only import runtime.api (not runtime.services)."""
    adapter_path = pathlib.Path("cli/kilo/adapter/__init__.py")
    assert adapter_path.exists(), f"Adapter module missing at {adapter_path}"

    imports_runtime_services = False
    for mod, _ in _get_imports_from_file(adapter_path):
        if mod == "runtime.services" or mod.startswith("runtime.services."):
            imports_runtime_services = True

    assert not imports_runtime_services, (
        "Adapter must NOT import from runtime.services directly. "
        "Use create_default_lep() from runtime.api instead."
    )
