
import json
from pathlib import Path

from caseproof.integrity import calculate_sha256


def create_manifest(evidence_directory, manifest_path):
    """
    Generate a SHA-256 manifest for evidence files.
    """

    evidence_directory = Path(evidence_directory)
    manifest_path = Path(manifest_path)

    manifest = {}

    for file_path in evidence_directory.iterdir():

        if file_path.is_file():
            manifest[file_path.name] = calculate_sha256(file_path)

    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    with open(manifest_path, "w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=4)

    print(f"Integrity manifest created: {manifest_path}")


def verify_manifest(evidence_directory, manifest_path):
    """
    Compare evidence files against recorded SHA-256 hashes.
    """

    evidence_directory = Path(evidence_directory)
    manifest_path = Path(manifest_path)

    with open(manifest_path, "r", encoding="utf-8") as file:
        manifest = json.load(file)

    results = []

    for filename, original_hash in manifest.items():

        file_path = evidence_directory / filename

        if not file_path.exists():
            results.append((filename, "MISSING"))
            continue

        current_hash = calculate_sha256(file_path)

        if current_hash == original_hash:
            results.append((filename, "VERIFIED"))
        else:
            results.append((filename, "MODIFIED"))

    return results
