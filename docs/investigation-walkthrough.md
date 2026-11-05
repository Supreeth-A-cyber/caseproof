# CaseProof - SOC Investigation Walkthrough

## 1. Investigation Overview

**Case ID:** CASE-001  
**Case Title:** Suspicious Login Investigation  
**Investigation Type:** Authentication Event Analysis

This walkthrough demonstrates how CaseProof evaluates security investigation claims against structured evidence, identifies evidence gaps, verifies evidence integrity, and maintains an auditable investigation history.

The case uses sample authentication records containing failed and successful login events.

> This is a simulated investigation using sample data, not a report of a real security incident.

## 2. Investigation Scenario

The investigation contains four authentication event records associated with the username `admin`.

| Evidence ID | Event Type | Username |
|---|---|---|
| EV-001 | failed_login | admin |
| EV-002 | failed_login | admin |
| EV-003 | failed_login | admin |
| EV-004 | success_login | admin |

The sample case includes three investigation claims that CaseProof must evaluate.

## 3. Evidence Validation

CaseProof first validates the evidence records.

The validation process checks:

- Required evidence fields.
- Evidence record structure.
- Duplicate evidence IDs.
- Valid authentication event types.
- Non-empty usernames.

**Observed result:** All evidence records are valid.

## 4. Claim Validation

CaseProof maps investigation claims to their referenced evidence and evaluates them using predefined rules.

### Claim CL-001: Three Failed Login Attempts

**Claim:** Admin experienced three failed login attempts.

- Expected failed login count: 3
- Observed failed login count: 3
- Referenced evidence: EV-001, EV-002, EV-003

**Result: SUPPORTED**

The observed failed login count matches the claimed count.

### Claim CL-002: Data Exfiltration

**Claim:** The attacker stole company data.

- Referenced evidence: EV-004
- Evidence available: One successful login record.

**Result: NOT ASSESSABLE**

The current validation engine does not support data exfiltration assessment.

A successful login record alone does not establish that data was accessed or exfiltrated.

### Claim CL-003: Five Failed Login Attempts

**Claim:** Admin experienced five failed login attempts.

- Expected failed login count: 5
- Observed failed login count: 3
- Referenced evidence: EV-001, EV-002, EV-003

**Result: PARTIALLY SUPPORTED**

Three failed login events were found, which is fewer than the five claimed.

## 5. Evidence Gap Analysis

CaseProof identifies missing evidence categories associated with the data-exfiltration claim.

The application reports:

- Missing data access evidence.
- Missing data exfiltration evidence.

These gaps indicate that the available sample evidence is insufficient to assess the data-theft statement.

## 6. Evidence Integrity Verification

CaseProof uses the SHA-256 hashing algorithm to verify the integrity of evidence files.

The recorded hash is stored in:

`data/schemas/integrity_manifest.json`

During execution, CaseProof compares the current evidence file hash with its recorded hash.

**Observed result:** `evidence_sample.txt: VERIFIED`

This indicates that the file matches its recorded integrity value.

## 7. Audit Trail Verification

CaseProof maintains an investigation audit trail containing information such as:

- Investigation run ID.
- Case ID.
- Investigation timestamp.
- Audit version.
- Claim validation results.
- Hash-chain information.

The audit trail verification process checks the integrity of protected records.

**Observed result:** Audit trail integrity verified.

The audit trail uses hash chaining to make unauthorized modifications detectable under the current implementation's integrity assumptions.

## 8. Investigation Report

After processing the case, CaseProof generates a Markdown investigation report.

Generated report:

`reports/CASE-001_report.md`

The report includes:

- Investigation metadata.
- Evidence inventory.
- Claim validation results.
- Evidence references.
- Evidence gaps.
- Investigation limitations.

## 9. Investigation Conclusion

The available sample evidence supports the claim that three failed login attempts occurred for the `admin` account.

The claim of five failed login attempts is only partially supported because three relevant events were found.

The data-exfiltration claim remains not assessable because the current validation engine does not support this assessment and the required supporting evidence is unavailable.

The evidence file passed SHA-256 integrity verification, and the audit trail passed its hash-chain verification.

## 10. Technical Limitations

- Claim assessment is rule-based and supports limited claim types.
- Data-exfiltration assessment is not implemented.
- Evidence-gap detection currently supports specific predefined scenarios.
- SHA-256 verification checks file consistency against a recorded hash; it does not independently establish evidence authenticity.
- A hash chain is tamper-evident, not tamper-proof. An attacker able to rewrite the entire audit file may be able to recompute its hashes.
- The project is an educational prototype and is not a replacement for a production SIEM, digital forensics platform, or incident response process.

## 11. Skills Demonstrated

This project demonstrates practical exposure to:

- Python security automation.
- JSON-based security event processing.
- Authentication event analysis.
- Evidence validation.
- Rule-based security claim assessment.
- SHA-256 file integrity verification.
- Hash-chained audit logging.
- Automated testing with pytest.
- Markdown investigation reporting.

---

*CaseProof is a hands-on cybersecurity portfolio project focused on SOC investigation quality, evidence integrity, and auditability.*