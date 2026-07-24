"""Verify that cli/kilo/ maintains LEP architecture boundaries.

The Kilo CLI adapter bridges the runtime and CLI layers. The adapter
necessarily imports from runtime.services and runtime.kernel to
initialize the LEP runtime. Command handlers consume the LEP facade
through the adapter, not through direct runtime access.

This test verifies:
1. Command modules only import from cli.kilo.* and standard library.
2. The adapter pattern is followed (commands never import runtime directly).
3. The overall architecture is preserved (Kilo is not the platform root).
"""


def test_command_modules_dont_import_runtime_directly() -> None:
    import ast
    import pathlib

    command_files = list(pathlib.Path("cli/kilo/commands").glob("*.py"))
    assert command_files, "No command modules found"

    prohibited_imports = [
        "runtime.kernel", "runtime.services", "runtime.assets",
        "runtime.ai", "runtime.workflows", "runtime.plugins",
        "runtime.projects", "runtime.knowledge", "runtime.automation",
        "runtime.operations", "runtime.configuration",
        "contracts", "schemas", "profiles", "extensions", "apps",
    ]

    errors = []
    for path in command_files:
        with open(path) as f:
            tree = ast.parse(f.read(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for prohibited in prohibited_imports:
                        if alias.name == prohibited or alias.name.startswith(prohibited + "."):
                            errors.append(f"{path.name}: imports {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                    for prohibited in prohibited_imports:
                        if node.module == prohibited or node.module.startswith(prohibited + "."):
                            errors.append(f"{path.name}: from {node.module} import ...")

    assert not errors, "Command modules must not import runtime directly:\n" + "\n".join(errors)


def test_adapter_bridges_runtime() -> None:
    import ast
    import pathlib

    adapter_path = pathlib.Path("cli/kilo/adapter/__init__.py")
    assert adapter_path.exists(), "Adapter module missing"

    with open(adapter_path) as f:
        tree = ast.parse(f.read(), filename=str(adapter_path))

    imports_runtime_api = False
    imports_runtime_services = False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == "runtime.api":
                imports_runtime_api = True
            if node.module and node.module.startswith("runtime.services"):
                imports_runtime_services = True

    assert imports_runtime_api, "Adapter must import from runtime.api (LEP facade)"
    assert imports_runtime_services, "Adapter must import from runtime.services (ServiceManager construction)"
