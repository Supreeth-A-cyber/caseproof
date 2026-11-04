
from caseproof.integrity_manifest import (
    create_manifest,
    verify_manifest
)


def test_manifest_verifies_original_evidence(tmp_path):

    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()

    evidence_file = evidence_dir / "sample.txt"
    evidence_file.write_text("Original evidence")

    manifest_file = tmp_path / "manifest.json"

    create_manifest(evidence_dir, manifest_file)

    results = verify_manifest(evidence_dir, manifest_file)

    assert results == [("sample.txt", "VERIFIED")]


def test_manifest_detects_modified_evidence(tmp_path):

    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()

    evidence_file = evidence_dir / "sample.txt"
    evidence_file.write_text("Original evidence")

    manifest_file = tmp_path / "manifest.json"

    create_manifest(evidence_dir, manifest_file)

    evidence_file.write_text("Changed evidence")

    results = verify_manifest(evidence_dir, manifest_file)

    assert results == [("sample.txt", "MODIFIED")]
