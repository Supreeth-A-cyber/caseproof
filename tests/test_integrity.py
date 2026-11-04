
from caseproof.integrity import calculate_sha256, verify_integrity


def test_integrity_verification(tmp_path):

    evidence_file = tmp_path / "evidence.txt"
    evidence_file.write_text("Original security evidence")

    original_hash = calculate_sha256(evidence_file)

    is_valid, message = verify_integrity(
        evidence_file,
        original_hash
    )

    assert is_valid is True


def test_modified_evidence_detection(tmp_path):

    evidence_file = tmp_path / "evidence.txt"
    evidence_file.write_text("Original security evidence")

    original_hash = calculate_sha256(evidence_file)

    evidence_file.write_text("Modified security evidence")

    is_valid, message = verify_integrity(
        evidence_file,
        original_hash
    )

    assert is_valid is False
    assert "modified" in message.lower()
