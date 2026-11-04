
from pathlib import Path

from caseproof.integrity_manifest import (
    create_manifest,
    verify_manifest
)


EVIDENCE_DIRECTORY = Path("data/evidence")
MANIFEST_PATH = Path("data/schemas/integrity_manifest.json")


def run_integrity_check():

    if not EVIDENCE_DIRECTORY.exists():
        print("Evidence directory not found.")
        return

    if not MANIFEST_PATH.exists():

        print("No integrity manifest found.")
        print("Creating initial manifest...")

        create_manifest(
            EVIDENCE_DIRECTORY,
            MANIFEST_PATH
        )

        return

    print("\nVerifying evidence integrity...\n")

    results = verify_manifest(
        EVIDENCE_DIRECTORY,
        MANIFEST_PATH
    )

    for filename, status in results:
        print(f"{filename}: {status}")


if __name__ == "__main__":
    run_integrity_check()
