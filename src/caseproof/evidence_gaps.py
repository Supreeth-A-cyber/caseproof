
def detect_evidence_gaps(claims, evidence_list):
    """
    Identify evidence gaps in analyst investigations.
    """

    available_event_types = {
        item.get("event_type")
        for item in evidence_list
    }

    gaps = []

    for claim in claims:

        statement = claim.get("statement", "").lower()
        missing_requirements = []

        if "stole company data" in statement:
            if "data_access" not in available_event_types:
                missing_requirements.append("Data access evidence")

            if "data_exfiltration" not in available_event_types:
                missing_requirements.append("Data exfiltration evidence")

        if missing_requirements:
            gaps.append({
                "claim_id": claim.get("claim_id"),
                "statement": claim.get("statement"),
                "missing_requirements": missing_requirements
            })

    return gaps
