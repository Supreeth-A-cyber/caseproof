
def map_claims_to_evidence(claims, evidence_list):
    """
    Connect analyst claims to their referenced evidence.
    Preserve all original claim information.
    """

    evidence_registry = {
        item["evidence_id"]: item
        for item in evidence_list
    }

    mapped_claims = []

    for claim in claims:

        evidence_ids = claim.get("evidence_ids", [])

        linked_evidence = []
        missing_evidence = []

        for evidence_id in evidence_ids:

            if evidence_id in evidence_registry:
                linked_evidence.append(
                    evidence_registry[evidence_id]
                )
            else:
                missing_evidence.append(evidence_id)

        mapped_claim = {
            **claim,
            "linked_evidence": linked_evidence,
            "missing_evidence": missing_evidence
        }

        mapped_claims.append(mapped_claim)

    return mapped_claims
