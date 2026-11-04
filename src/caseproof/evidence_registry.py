def validate_evidence(evidence_list):
    """
    Validate evidence records in an investigation.
    """

    required_fields = [
        "evidence_id",
        "event_type",
        "username"
    ]

    allowed_event_types = [
        "failed_login",
        "success_login"
    ]

    errors = []
    seen_ids = set()

    # Validate evidence list
    if not isinstance(evidence_list, list):
        return False, ["Evidence must be provided as a list."]

    if not evidence_list:
        return False, ["Evidence list cannot be empty."]

    for index, evidence in enumerate(evidence_list, start=1):

        # Validate record structure
        if not isinstance(evidence, dict):
            errors.append(
                f"Record {index}: Evidence must be a dictionary."
            )
            continue

        # Check required fields
        for field in required_fields:
            if field not in evidence:
                errors.append(
                    f"Record {index}: Missing {field}"
                )

        # Validate evidence ID
        evidence_id = evidence.get("evidence_id")

        if not isinstance(evidence_id, str) or not evidence_id.strip():
            errors.append(
                f"Record {index}: Evidence ID must be a non-empty string."
            )
        elif evidence_id in seen_ids:
            errors.append(
                f"Record {index}: Duplicate ID {evidence_id}"
            )
        else:
            seen_ids.add(evidence_id)

        # Validate event type
        event_type = evidence.get("event_type")

        if not isinstance(event_type, str):
            errors.append(
                f"Record {index}: Event type must be a string."
            )
        elif event_type not in allowed_event_types:
            errors.append(
                f"Record {index}: Invalid event type {event_type}"
            )

        # Validate username
        username = evidence.get("username")

        if not isinstance(username, str) or not username.strip():
            errors.append(
                f"Record {index}: Username must be a non-empty string."
            )

    if errors:
        return False, errors

    return True, ["All evidence records are valid."]


