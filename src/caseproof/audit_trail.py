
import json
import hashlib
from pathlib import Path


AUDIT_TRAIL_PATH = Path("reports/audit_trail.json")


def calculate_record_hash(record):
    """
    Generate a SHA-256 hash for an audit record.
    """

    record_data = {
        key: value
        for key, value in record.items()
        if key != "record_hash"
    }

    canonical_data = json.dumps(
        record_data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    )

    return hashlib.sha256(
        canonical_data.encode("utf-8")
    ).hexdigest()



def initialize_hash_chain(records):
    """
    Initialize hash fields for valid legacy records.
    Reject malformed or partially protected audit trails.
    """

    if not isinstance(records, list):
        raise ValueError("Audit trail must be a list.")

    if not records:
        return records

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(
                f"Invalid audit record format at position {index + 1}."
            )

    hash_states = []

    for record in records:
        has_previous_hash = "previous_hash" in record
        has_record_hash = "record_hash" in record

        if has_previous_hash != has_record_hash:
            raise ValueError(
                "Incomplete hash fields detected in audit trail."
            )

        hash_states.append(has_previous_hash)

    if any(hash_states) and not all(hash_states):
        raise ValueError(
            "Mixed legacy and hash-protected records detected."
        )

    if all(hash_states):
        return records

    previous_hash = "GENESIS"

    for record in records:
        record["previous_hash"] = previous_hash
        record["record_hash"] = calculate_record_hash(record)
        previous_hash = record["record_hash"]

    return records



def verify_audit_trail(records):
    """
    Verify the integrity of the audit trail hash chain.
    """

    if not isinstance(records, list):
        return False, ["Audit trail must be a list."]

    previous_hash = "GENESIS"
    messages = []

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            messages.append(
                f"Record {index + 1}: Invalid record format."
            )
            return False, messages

        if "record_hash" not in record:
            messages.append(
                f"Record {index + 1}: Missing record hash."
            )
            return False, messages

        if record.get("previous_hash") != previous_hash:
            messages.append(
                f"Record {index + 1}: Previous hash mismatch."
            )
            return False, messages

        expected_hash = calculate_record_hash(record)

        if record["record_hash"] != expected_hash:
            messages.append(
                f"Record {index + 1}: Record hash mismatch."
            )
            return False, messages

        previous_hash = record["record_hash"]

    messages.append("Audit trail integrity verified.")
    return True, messages


def save_audit_record(audit_metadata, mapped_claims):
    """
    Save an investigation run to the persistent audit trail.
    """

    AUDIT_TRAIL_PATH.parent.mkdir(parents=True, exist_ok=True)

    records = []

    if AUDIT_TRAIL_PATH.exists():
        try:
            with AUDIT_TRAIL_PATH.open("r", encoding="utf-8") as file:
                records = json.load(file)

            if not isinstance(records, list):
                raise ValueError("Audit trail must contain a JSON list.")

        except (json.JSONDecodeError, OSError, ValueError) as error:
            raise RuntimeError(
                f"Unable to read existing audit trail: {error}"
            ) from error

    records = initialize_hash_chain(records)

    is_valid, messages = verify_audit_trail(records)

    if not is_valid:
        raise RuntimeError(
            "Existing audit trail integrity check failed: "
            + " ".join(messages)
        )

    audit_record = {
        "run_id": audit_metadata["run_id"],
        "case_id": audit_metadata["case_id"],
        "generated_at": audit_metadata["generated_at"],
        "audit_version": audit_metadata["audit_version"],
        "claims": [
            {
                "claim_id": claim["claim_id"],
                "validation_result": claim.get(
                    "validation_result", "Not assessed"
                ),
                "validation_reason": claim.get(
                    "validation_reason", "No explanation available."
                ),
                "evidence_ids": claim.get("evidence_ids", [])
            }
            for claim in mapped_claims
        ]
    }

    previous_hash = (
        records[-1]["record_hash"]
        if records
        else "GENESIS"
    )

    audit_record["previous_hash"] = previous_hash
    audit_record["record_hash"] = calculate_record_hash(audit_record)

    records.append(audit_record)

    temporary_path = AUDIT_TRAIL_PATH.with_suffix(".tmp")

    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=4)

    temporary_path.replace(AUDIT_TRAIL_PATH)

    return audit_record
