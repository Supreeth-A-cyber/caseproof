
from caseproof.audit import create_audit_metadata, AUDIT_VERSION
from uuid import UUID


def test_audit_metadata_fields():
    metadata = create_audit_metadata("CASE-001")

    assert metadata["case_id"] == "CASE-001"
    assert metadata["audit_version"] == AUDIT_VERSION
    assert "run_id" in metadata
    assert "generated_at" in metadata


def test_audit_run_id_is_valid_uuid():
    metadata = create_audit_metadata("CASE-001")

    UUID(metadata["run_id"])


def test_audit_run_ids_are_unique():
    first = create_audit_metadata("CASE-001")
    second = create_audit_metadata("CASE-001")

    assert first["run_id"] != second["run_id"]
