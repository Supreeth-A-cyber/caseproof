def validate_claim(claim):
    """
    Validate structured analyst claims against linked evidence.
    Returns a result and an explanation.
    """

    evidence = claim["linked_evidence"]
    missing = claim["missing_evidence"]

    if not evidence:
        return {
            "result": "Not assessable",
            "reason": "No linked evidence was provided.",
            "evidence_count": 0
        }

    if missing:
        return {
            "result": "Not assessable",
            "reason": f"Missing evidence references: {missing}",
            "evidence_count": len(evidence)
        }

    claim_type = claim.get("claim_type")

    if claim_type == "failed_login_count":

        username = claim.get("username")
        expected_count = claim.get("expected_count")

        actual_count = sum(
            1 for item in evidence
            if item.get("event_type") == "failed_login"
            and item.get("username") == username
        )

        if expected_count is None:
            return {
                "result": "Not assessable",
                "reason": "Expected failed login count was not provided.",
                "evidence_count": len(evidence)
            }

        if actual_count == expected_count:
            result = "Supported"
            reason = "Observed failed login count matches the claimed count."

        elif actual_count > 0 and actual_count < expected_count:
            result = "Partially supported"
            reason = "Some failed login events were found, but fewer than claimed."

        else:
            result = "Contradicted"
            reason = "Observed failed login count does not support the claim."

        return {
            "result": result,
            "reason": reason,
            "expected_count": expected_count,
            "actual_count": actual_count,
            "evidence_count": len(evidence)
        }

    if claim_type == "data_exfiltration":
        return {
            "result": "Not assessable",
            "reason": "The current validation engine does not support data exfiltration assessment.",
            "evidence_count": len(evidence)
        }

    return {
        "result": "Not assessable",
        "reason": f"Unsupported claim type: {claim_type}",
        "evidence_count": len(evidence)
    }