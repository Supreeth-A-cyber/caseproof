from caseproof.validation_engine import validate_claim


def test_supported_claim():

    claim = {
        "claim_type": "failed_login_count",
        "username": "admin",
        "expected_count": 3,
        "linked_evidence": [
            {"event_type": "failed_login", "username": "admin"},
            {"event_type": "failed_login", "username": "admin"},
            {"event_type": "failed_login", "username": "admin"}
        ],
        "missing_evidence": []
    }

    result = validate_claim(claim)

    assert result["result"] == "Supported"
    assert result["expected_count"] == 3
    assert result["actual_count"] == 3
    assert result["evidence_count"] == 3
    assert "matches" in result["reason"]


def test_partially_supported_claim():

    claim = {
        "claim_type": "failed_login_count",
        "username": "admin",
        "expected_count": 5,
        "linked_evidence": [
            {"event_type": "failed_login", "username": "admin"},
            {"event_type": "failed_login", "username": "admin"},
            {"event_type": "failed_login", "username": "admin"}
        ],
        "missing_evidence": []
    }

    result = validate_claim(claim)

    assert result["result"] == "Partially supported"
    assert result["expected_count"] == 5
    assert result["actual_count"] == 3
    assert result["evidence_count"] == 3
    assert "fewer than claimed" in result["reason"]


def test_not_assessable_claim():

    claim = {
        "claim_type": "data_exfiltration",
        "username": "admin",
        "expected_count": None,
        "linked_evidence": [
            {"event_type": "success_login", "username": "admin"}
        ],
        "missing_evidence": []
    }

    result = validate_claim(claim)

    assert result["result"] == "Not assessable"
    assert "does not support data exfiltration assessment" in result["reason"]
    assert result["evidence_count"] == 1