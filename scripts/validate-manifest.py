#!/usr/bin/env python3
"""Validate artifacts manifest structure and lifecycle state consistency.

This script performs read-only validation of the manifest.
It never modifies the manifest, approves artifacts, or transitions states.
"""

import sys
from pathlib import Path

import yaml


def load_manifest(path: str) -> list[dict]:
    with open(path) as f:
        data = yaml.safe_load(f)
    if not data or "artifacts" not in data:
        print("ERROR: manifest missing 'artifacts' key")
        sys.exit(1)
    return data["artifacts"]


def validate_artifact(artifact: dict) -> list[str]:
    issues: list[str] = []
    aid = artifact.get("artifact", {}).get("id", "unknown")

    art = artifact.get("artifact", {})
    if not art.get("id"):
        issues.append(f"{aid}: missing artifact.id")
    if not art.get("title"):
        issues.append(f"{aid}: missing artifact.title")
    if not art.get("state"):
        issues.append(f"{aid}: missing artifact.state")

    state = art.get("state", "")
    valid_states = {"draft", "accepted_for_implementation", "implemented", "validated", "accepted"}
    if state and state not in valid_states:
        issues.append(f"{aid}: invalid state '{state}'")

    impl = artifact.get("implementation", {})
    if state in ("accepted_for_implementation", "implemented", "validated", "accepted"):
        if impl.get("status") != "complete":
            issues.append(f"{aid}: implementation status not 'complete'")

    val = artifact.get("validation", {})
    if state in ("validated", "accepted"):
        if val.get("status") != "complete":
            issues.append(f"{aid}: validation status not 'complete'")

    acc = artifact.get("acceptance", {})
    if state == "accepted":
        if acc.get("status") != "accepted":
            issues.append(f"{aid}: acceptance status not 'accepted'")

    nx = artifact.get("next_artifact", {})
    if nx.get("id") and nx.get("id") != "TBD" and nx.get("status") not in (
        "draft", "accepted_for_implementation", "implemented", "validated", "accepted", "ready_for_contract_generation"
    ):
        issues.append(f"{aid}: next_artifact '{nx['id']}' has invalid status '{nx.get('status')}'")

    files = artifact.get("files", [])
    if state in ("implemented", "validated", "accepted") and not files:
        issues.append(f"{aid}: no files listed for implemented artifact")

    return issues


def main() -> None:
    manifest_path = Path(__file__).parent.parent / "docs" / "manifests" / "artifacts.yaml"
    if not manifest_path.exists():
        print(f"ERROR: manifest not found at {manifest_path}")
        sys.exit(1)

    print(f"Validating manifest: {manifest_path}")
    artifacts = load_manifest(str(manifest_path))
    print(f"Found {len(artifacts)} artifacts")

    all_issues: list[str] = []
    for artifact in artifacts:
        issues = validate_artifact(artifact)
        for issue in issues:
            print(f"  ISSUE: {issue}")
        all_issues.extend(issues)

    if all_issues:
        print(f"\n{len(all_issues)} issue(s) found")
        sys.exit(2)
    else:
        print("All artifacts valid")


if __name__ == "__main__":
    main()
