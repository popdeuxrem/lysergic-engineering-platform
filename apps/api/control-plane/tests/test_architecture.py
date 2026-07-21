import ast
import importlib
import os
from pathlib import Path


def _collect_imports(module_name: str) -> set[str]:
    module = importlib.import_module(module_name)
    source_file = module.__file__
    if source_file is None:
        return set()
    package_paths: dict[str, Path] = {}

    src_root = Path(module.__spec__.origin).parent.parent if module.__spec__ and module.__spec__.origin else Path(source_file).parent.parent
    for root, _, files in os.walk(src_root):
        for f in files:
            if f.endswith(".py"):
                full = Path(root) / f
                rel = full.relative_to(src_root.parent)
                mod = str(rel.with_suffix("")).replace(os.sep, ".")
                package_paths[mod] = full

    imports: set[str] = set()
    for pkg_path in [p for m, p in package_paths.items() if m.startswith(module_name)]:
        tree = ast.parse(pkg_path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])

    return imports


def test_domain_does_not_import_application() -> None:
    domain_modules = {
        "src.domain.exceptions",
        "src.domain.value_objects",
        "src.domain.entities",
    }
    for mod in domain_modules:
        source = importlib.import_module(mod)
        if source.__file__ is None:
            continue
        tree = ast.parse(Path(source.__file__).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert node.module is None or not node.module.startswith(
                    "src.application"
                ), f"{mod} imports from application layer: {node.module}"
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(
                        "src.application"
                    ), f"{mod} imports from application layer: {alias.name}"


def test_domain_does_not_import_infrastructure() -> None:
    domain_modules = {
        "src.domain.exceptions",
        "src.domain.value_objects",
        "src.domain.entities",
    }
    for mod in domain_modules:
        source = importlib.import_module(mod)
        if source.__file__ is None:
            continue
        tree = ast.parse(Path(source.__file__).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert node.module is None or not node.module.startswith(
                    "src.infrastructure"
                ), f"{mod} imports from infrastructure layer: {node.module}"
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(
                        "src.infrastructure"
                    ), f"{mod} imports from infrastructure layer: {alias.name}"


def test_application_does_not_import_infrastructure() -> None:
    application_modules = {
        "src.application.exceptions",
        "src.application.dto",
        "src.application.interfaces",
    }
    for mod in application_modules:
        source = importlib.import_module(mod)
        if source.__file__ is None:
            continue
        tree = ast.parse(Path(source.__file__).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert node.module is None or not node.module.startswith(
                    "src.infrastructure"
                ), f"{mod} imports from infrastructure layer: {node.module}"
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(
                        "src.infrastructure"
                    ), f"{mod} imports from infrastructure layer: {alias.name}"


def test_domain_package_exports() -> None:
    from src.domain import DomainException, Entity, ValueObject  # noqa: F401

    assert Entity is not None
    assert ValueObject is not None


def test_application_package_exports() -> None:
    from src.application import (  # noqa: F401
        BaseDTO,
        Command,
        ExecutionService,
        Query,
        Repository,
        Result,
        UseCase,
    )

    assert BaseDTO is not None
    assert Command is not None
    assert ExecutionService is not None
    assert Query is not None
    assert Repository is not None
    assert Result is not None
    assert UseCase is not None


def test_application_layer_does_not_import_infrastructure_extended() -> None:
    application_modules = {
        "src.application.exceptions",
        "src.application.dto",
        "src.application.interfaces",
        "src.application.execution_dto",
        "src.application.execution_use_cases",
        "src.application.execution_service",
    }
    for mod in application_modules:
        source = importlib.import_module(mod)
        if source.__file__ is None:
            continue
        tree = ast.parse(Path(source.__file__).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert node.module is None or not node.module.startswith(
                    "src.infrastructure"
                ), f"{mod} imports from infrastructure layer: {node.module}"
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(
                        "src.infrastructure"
                    ), f"{mod} imports from infrastructure layer: {alias.name}"
