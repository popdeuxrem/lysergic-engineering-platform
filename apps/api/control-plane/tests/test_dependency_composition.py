import ast
from pathlib import Path


def test_service_layer_does_not_import_fastapi() -> None:
    source = Path(__file__).parent.parent / "src" / "application" / "execution_service.py"
    tree = ast.parse(source.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert not alias.name.startswith("fastapi"), "Service imports fastapi"
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                assert not node.module.startswith("fastapi"), "Service imports fastapi"


def test_service_layer_does_not_import_sqlalchemy() -> None:
    source = Path(__file__).parent.parent / "src" / "application" / "execution_service.py"
    tree = ast.parse(source.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert not alias.name.startswith("sqlalchemy"), "Service imports sqlalchemy"
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                assert not node.module.startswith("sqlalchemy"), "Service imports sqlalchemy"


def test_service_layer_imports_domain_only() -> None:
    source = Path(__file__).parent.parent / "src" / "application" / "execution_service.py"
    tree = ast.parse(source.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("src"):
                assert node.module.startswith(
                    ("src.domain.", "src.application.")
                ), f"Service imports outside allowed layers: {node.module}"
