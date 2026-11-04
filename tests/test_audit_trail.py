
import json

from caseproof.audit_trail import (
    save_audit_record,
    verify_audit_trail,
    calculate_record_hash,
    initialize_hash_chain
)


def test_save_audit_record(tmp_path, monkeypatch):

    audit_file = tmp_path / "audit_trail.json"

    monkeypatch.setattr(
        "caseproof.audit_trail.AUDIT_TRAIL_PATH",
        audit_file
    )

    metadata = {
        "run_id": "test-run-001",
        "case_id": "CASE-001",
        "generated_at": "2026-11-04T10:00:00+00:00",
        "audit_version": "1.0.0"
    }

    claims = [
        {
            "claim_id": "CL-001",
            "validation_result": "Supported",
            "validation_reason": "Observed count matches.",
            "evidence_ids": ["EV-001", "EV-002"]
        }
    ]

    record = save_audit_record(metadata, claims)

    assert audit_file.exists()
    assert record["case_id"] == "CASE-001"

    saved_data = json.loads(
        audit_file.read_text(encoding="utf-8")
    )

    assert len(saved_data) == 1
    assert saved_data[0]["claims"][0]["validation_result"] == "Supported"


def test_audit_trail_appends_records(tmp_path, monkeypatch):

    audit_file = tmp_path / "audit_trail.json"

    monkeypatch.setattr(
        "caseproof.audit_trail.AUDIT_TRAIL_PATH",
        audit_file
    )

    metadata = {
        "run_id": "test-run-002",
        "case_id": "CASE-001",
        "generated_at": "2026-11-04T10:00:00+00:00",
        "audit_version": "1.0.0"
    }

    save_audit_record(metadata, [])
    save_audit_record(metadata, [])

    saved_data = json.loads(
        audit_file.read_text(encoding="utf-8")
    )

    assert len(saved_data) == 2


def test_audit_trail_detects_modified_record():

    records = [
        {
            "run_id": "run-001",
            "case_id": "CASE-001",
            "previous_hash": "GENESIS",
        }
    ]

    records[0]["record_hash"] = calculate_record_hash(records[0])

    records[0]["case_id"] = "CASE-999"

    is_valid, messages = verify_audit_trail(records)

    assert is_valid is False
    assert "Record 1: Record hash mismatch." in messages


def test_audit_trail_detects_deleted_record():

    records = []

    previous_hash = "GENESIS"

    for run_id in ["run-001", "run-002", "run-003"]:
        record = {
            "run_id": run_id,
            "case_id": "CASE-001",
            "previous_hash": previous_hash
        }

        record["record_hash"] = calculate_record_hash(record)
        previous_hash = record["record_hash"]
        records.append(record)

    del records[1]

    is_valid, messages = verify_audit_trail(records)

    assert is_valid is False
    assert "Record 2: Previous hash mismatch." in messages


def test_audit_trail_detects_reordered_records():

    records = []

    previous_hash = "GENESIS"

    for run_id in ["run-001", "run-002", "run-003"]:
        record = {
            "run_id": run_id,
            "case_id": "CASE-001",
            "previous_hash": previous_hash
        }

        record["record_hash"] = calculate_record_hash(record)
        previous_hash = record["record_hash"]
        records.append(record)

    records[1], records[2] = records[2], records[1]

    is_valid, messages = verify_audit_trail(records)

    assert is_valid is False

def test_audit_trail_verifies_valid_chain():

    records = []

    previous_hash = "GENESIS"

    for run_id in ["run-001", "run-002"]:

        record = {
            "run_id": run_id,
            "case_id": "CASE-001",
            "previous_hash": previous_hash
        }

        record["record_hash"] = calculate_record_hash(record)

        previous_hash = record["record_hash"]
        records.append(record)

    is_valid, messages = verify_audit_trail(records)

    assert is_valid is True
    assert "Audit trail integrity verified." in messages


import pytest


def test_initialize_rejects_non_dictionary_record():

    records = [
        {"run_id": "run-001"},
        "invalid-record"
    ]

    with pytest.raises(ValueError, match="Invalid audit record format"):
        initialize_hash_chain(records)


def test_initialize_rejects_incomplete_hash_fields():

    records = [
        {
            "run_id": "run-001",
            "previous_hash": "GENESIS"
        }
    ]

    with pytest.raises(ValueError, match="Incomplete hash fields"):
        initialize_hash_chain(records)


def test_initialize_rejects_mixed_legacy_and_protected_records():

    records = [
        {
            "run_id": "run-001"
        },
        {
            "run_id": "run-002",
            "previous_hash": "GENESIS",
            "record_hash": "invalid-hash"
        }
    ]

    with pytest.raises(ValueError, match="Mixed legacy and hash-protected"):
        initialize_hash_chain(records)


def test_verify_rejects_non_list_audit_trail():

    is_valid, messages = verify_audit_trail(
        {"run_id": "run-001"}
    )

    assert is_valid is False
    assert "Audit trail must be a list." in messages


def test_verify_rejects_invalid_record_type():

    records = [
        "invalid-record"
    ]

    is_valid, messages = verify_audit_trail(records)

    assert is_valid is False
    assert "Record 1: Invalid record format." in messages

def test_verify_accepts_empty_audit_trail():

    is_valid, messages = verify_audit_trail([])

    assert is_valid is True
    assert "Audit trail integrity verified." in messages