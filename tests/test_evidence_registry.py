
from caseproof.evidence_registry import validate_evidence


def test_valid_evidence():

    evidence = [
        {
            "evidence_id": "EV-001",
            "event_type": "failed_login",
            "username": "admin"
        }
    ]

    is_valid, messages = validate_evidence(evidence)

    assert is_valid is True


def test_duplicate_evidence_ids():

    evidence = [
        {
            "evidence_id": "EV-001",
            "event_type": "failed_login",
            "username": "admin"
        },
        {
            "evidence_id": "EV-001",
            "event_type": "success_login",
            "username": "admin"
        }
    ]

    is_valid, messages = validate_evidence(evidence)

    assert is_valid is False
    assert any("Duplicate ID" in message for message in messages)


def test_missing_username():

    evidence = [
        {
            "evidence_id": "EV-001",
            "event_type": "failed_login"
        }
    ]

    is_valid, messages = validate_evidence(evidence)

    assert is_valid is False
    assert any("username" in message for message in messages)

def test_invalid_evidence_record_type():
    evidence = ["invalid_record"]

    is_valid, messages = validate_evidence(evidence)

    assert is_valid is False
    assert "Evidence must be a dictionary." in messages[0]


def test_invalid_evidence_id_type():
    evidence = [
        {
            "evidence_id": 123,
            "event_type": "failed_login",
            "username": "admin"
        }
    ]

    is_valid, messages = validate_evidence(evidence)

    assert is_valid is False
    assert any("Evidence ID must be a non-empty string." in msg for msg in messages)


def test_empty_username():
    evidence = [
        {
            "evidence_id": "EV-005",
            "event_type": "failed_login",
            "username": " "
        }
    ]

    is_valid, messages = validate_evidence(evidence)

    assert is_valid is False
    assert any("Username must be a non-empty string." in msg for msg in messages)


def test_empty_evidence_list():
    is_valid, messages = validate_evidence([])

    assert is_valid is False
    assert "Evidence list cannot be empty." in messages


def test_invalid_event_type():
    evidence = [
        {
            "evidence_id": "EV-006",
            "event_type": "unknown_event",
            "username": "admin"
        }
    ]

    is_valid, messages = validate_evidence(evidence)

    assert is_valid is False
    assert any("Invalid event type" in msg for msg in messages)