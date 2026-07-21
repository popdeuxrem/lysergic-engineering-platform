"""Tests for validation runner."""

import os
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent.parent / "scripts"
CONTROL_PLANE_DIR = Path(__file__).parent.parent.parent / "apps" / "api" / "control-plane"


def test_validate_script_exists() -> None:
    assert (SCRIPTS_DIR / "validate.sh").exists()


def test_validate_script_is_executable() -> None:
    assert (SCRIPTS_DIR / "validate.sh").stat().st_mode & 0o111


def test_capture_evidence_script_exists() -> None:
    assert (SCRIPTS_DIR / "capture-evidence.sh").exists()


def test_capture_evidence_script_is_executable() -> None:
    assert (SCRIPTS_DIR / "capture-evidence.sh").stat().st_mode & 0o111


def test_validate_manifest_script_exists() -> None:
    assert (SCRIPTS_DIR / "validate-manifest.py").exists()


def test_manifest_validator_runs() -> None:
    result = subprocess.run(
        ["uv", "run", "python3", str(SCRIPTS_DIR / "validate-manifest.py")],
        capture_output=True,
        text=True,
        cwd=str(CONTROL_PLANE_DIR),
    )
    assert result.returncode in (0, 2), f"Unexpected exit: {result.returncode}\n{result.stdout}\n{result.stderr}"


def test_manifest_validator_output() -> None:
    result = subprocess.run(
        ["uv", "run", "python3", str(SCRIPTS_DIR / "validate-manifest.py")],
        capture_output=True,
        text=True,
        cwd=str(CONTROL_PLANE_DIR),
    )
    assert "Validating manifest:" in result.stdout
    assert "artifacts" in result.stdout


def test_manifest_validator_does_not_modify_files() -> None:
    manifest_path = Path(__file__).parent.parent.parent / "docs" / "manifests" / "artifacts.yaml"
    mtime_before = manifest_path.stat().st_mtime
    subprocess.run(
        ["uv", "run", "python3", str(SCRIPTS_DIR / "validate-manifest.py")],
        capture_output=True,
        cwd=str(CONTROL_PLANE_DIR),
    )
    mtime_after = manifest_path.stat().st_mtime
    assert mtime_before == mtime_after, "Manifest was modified by validator"
