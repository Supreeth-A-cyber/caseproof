
import uuid
from datetime import datetime, timezone


AUDIT_VERSION = "1.0.0"


def create_audit_metadata(case_id):
    """
    Create metadata for an investigation run.
    """

    return {
        "run_id": str(uuid.uuid4()),
        "case_id": case_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "audit_version": AUDIT_VERSION
    }
