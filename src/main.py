
from caseproof.ingestion import load_case, validate_case
from caseproof.evidence_registry import validate_evidence
from caseproof.claim_mapper import map_claims_to_evidence
from caseproof.validation_engine import validate_claim
from caseproof.evidence_gaps import detect_evidence_gaps
from caseproof.report_generator import generate_report
from caseproof.integrity_manifest import verify_manifest
from pathlib import Path
from caseproof.logger import setup_logger
from caseproof.audit import create_audit_metadata
from caseproof.audit_trail import (
    save_audit_record,
    verify_audit_trail
)
import json

logger = setup_logger()
logger.info("Starting CaseProof investigation")

case_file = "data/sample_cases/case_001.json"

case_data = load_case(case_file)

if case_data is not None:
    audit_metadata = create_audit_metadata(case_data["case_id"])

    logger.info("Case loaded successfully: %s", case_data["case_id"])

    logger.info(
        "Investigation run created: %s",
        audit_metadata["run_id"]
    )

    if validate_case(case_data):

        is_valid, messages = validate_evidence(
            case_data["evidence"]
        )

        print("\nEvidence Validation:")

        for message in messages:
            print(message)

        if is_valid:

            print("\nClaim Validation:")

            mapped_claims = map_claims_to_evidence(
                case_data["claims"],
                case_data["evidence"]
            )

            for claim in mapped_claims:

                validation = validate_claim(claim)

                claim["validation_result"] = validation["result"]
                claim["validation_reason"] = validation["reason"]
                claim["validation_details"] = validation

                print(f"\nClaim ID: {claim['claim_id']}")
                print(f"Statement: {claim['statement']}")
                print(f"Result: {validation['result']}")
                print(f"Reason: {validation['reason']}")
                print(f"Evidence Count: {validation['evidence_count']}")

                if "expected_count" in validation:
                    print(f"Expected Count: {validation['expected_count']}")
                    print(f"Actual Count: {validation['actual_count']}")

            # Evidence Gap Analysis
            print("\nEvidence Gap Analysis:")

            gaps = detect_evidence_gaps(
                case_data["claims"],
                case_data["evidence"]
            )

            if gaps:
                for gap in gaps:
                    print(f"\nClaim ID: {gap['claim_id']}")
                    print(f"Statement: {gap['statement']}")

                    for requirement in gap["missing_requirements"]:
                        print(f"Missing: {requirement}")
            else:
                print("No evidence gaps detected.")

            # Generate Investigation Report
            generate_report(
                case_data,
                mapped_claims,
                gaps,
                audit_metadata
            )


            try:
                save_audit_record(
                    audit_metadata,
                    mapped_claims
                )

                logger.info(
                    "Investigation audit record saved: %s",
                    audit_metadata["run_id"]
                )

                print("\nInvestigation audit record saved successfully.")

            except RuntimeError as error:
                logger.error("Unable to save audit record: %s", error)
                print(f"\nAudit record save failed: {error}")

        else:
            print("Evidence validation failed. Report not generated.")

    else:
        print("Case validation failed. Report not generated.")


# Evidence Integrity Verification

print("\nEvidence Integrity Verification:")

evidence_directory = Path("data/evidence")
manifest_path = Path("data/schemas/integrity_manifest.json")

if manifest_path.exists():

    results = verify_manifest(
        evidence_directory,
        manifest_path
    )

    for filename, status in results:
        print(f"{filename}: {status}")

else:
    print("Integrity manifest not found.")


# Audit Trail Integrity Verification

print("\nAudit Trail Integrity Verification:")

audit_trail_path = Path("reports/audit_trail.json")

if audit_trail_path.exists():

    try:
        with audit_trail_path.open("r", encoding="utf-8") as file:
            audit_records = json.load(file)

        is_valid, messages = verify_audit_trail(audit_records)

        print(f"Records checked: {len(audit_records)}")

        for message in messages:
            print(message)

        if is_valid:
            print("Status: VERIFIED")
        else:
            print("Status: FAILED")

    except (json.JSONDecodeError, OSError, ValueError, TypeError) as error:
        logger.error("Audit trail verification failed: %s", error)
        print(f"Unable to verify audit trail: {error}")
        print("Status: FAILED")

else:
    print("Audit trail not found.")