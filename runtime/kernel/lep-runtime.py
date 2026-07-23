import yaml


def load_manifest(manifest_path):
    with open(manifest_path, 'r') as f:
        return yaml.safe_load(f)


def initialize_runtime(manifest):
    print(f"Initializing LEP runtime with platform version: {manifest['platform']['version']}")
    # Add runtime logic here


if __name__ == "__main__":
    manifest = load_manifest("../lep.yaml")
    initialize_runtime(manifest)
