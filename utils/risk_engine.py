"""Deterministic, rule-based risk scoring utilities."""

from __future__ import annotations

from typing import Dict, List, Tuple, Any
import yaml


def load_rules(path: str = "data/risk_rules.yaml") -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _categorize(score: int, thresholds: Dict[str, int]) -> str:
    if score >= thresholds["reject"]:
        return "High"
    if score >= thresholds["escalate"]:
        return "High"
    if score >= thresholds["review"]:
        return "Medium"
    return "Low"


def _human_review_required(level: str, missing_facts: List[str]) -> bool:
    return level in {"Medium", "High"} or bool(missing_facts)


def _escalation_route(level: str, workflow: str) -> str:
    if level == "High":
        return f"{workflow} Counsel + Risk Committee"
    if level == "Medium":
        return f"{workflow} Operations Reviewer"
    return "No escalation required"


def _next_steps(level: str, missing_facts: List[str], base_steps: List[str]) -> List[str]:
    steps = list(base_steps)
    if missing_facts:
        steps.append("Collect missing facts before final decision.")
    if level == "High":
        steps.append("Escalate to senior reviewer and require documented approval.")
    elif level == "Medium":
        steps.append("Route to human reviewer for conditional approval.")
    else:
        steps.append("Proceed with standard approval checklist.")
    return steps


def score_contract_dict(contract: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    triggered_rules: List[str] = []
    missing_facts: List[str] = []

    data_processing = str(contract.get("data_processing", "Unknown"))
    liability_cap = str(contract.get("liability_cap", "Unknown"))
    termination_days = contract.get("termination_days")

    if data_processing.lower() == "yes":
        score += 15
        triggered_rules.append("Personal data processing increases legal/privacy risk.")

    if liability_cap.lower() in {"none", "uncapped"}:
        score += 20
        triggered_rules.append("Uncapped liability is a high-risk commercial term.")

    unilateral_amendment = str(contract.get("unilateral_amendment_rights", "unknown"))
    if unilateral_amendment.lower() in {"yes", "true"}:
        score += 12
        triggered_rules.append("Unilateral amendment rights increase change-control risk.")
    elif unilateral_amendment.lower() == "unknown":
        missing_facts.append("Whether unilateral amendment rights exist.")

    if termination_days in [None, "", "Unknown"]:
        missing_facts.append("Termination right details are missing.")
    else:
        try:
            t_days = int(termination_days)
            if t_days > 180:
                score += 12
                triggered_rules.append("Long/no practical termination right increases lock-in risk.")
        except (TypeError, ValueError):
            missing_facts.append("Termination notice format is invalid.")

    subprocessor_consent = str(contract.get("subprocessor_consent_required", "unknown"))
    if subprocessor_consent.lower() in {"no", "false"}:
        score += 10
        triggered_rules.append("Subprocessors allowed without consent increases third-party risk.")
    elif subprocessor_consent.lower() == "unknown":
        missing_facts.append("Whether subprocessor consent is required.")

    security_terms = str(contract.get("security_terms_present", "unknown"))
    if security_terms.lower() in {"no", "false"}:
        score += 14
        triggered_rules.append("Missing security terms increase information-security risk.")
    elif security_terms.lower() == "unknown":
        missing_facts.append("Whether security terms are present.")

    risk_level = "High" if score >= 50 else "Medium" if score >= 25 else "Low"
    human_review_required = _human_review_required(risk_level, missing_facts)

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "triggered_rules": triggered_rules,
        "missing_facts": missing_facts,
        "human_review_required": human_review_required,
        "escalation_route": _escalation_route(risk_level, "Legal"),
        "recommended_next_steps": _next_steps(
            risk_level,
            missing_facts,
            [
                "Validate indemnity, liability, and data processing clauses against playbook.",
                "Confirm governing law and dispute resolution standards.",
            ],
        ),
    }


def score_vendor_dict(vendor: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    triggered_rules: List[str] = []
    missing_facts: List[str] = []

    data_access = str(vendor.get("data_access", "Unknown"))
    has_dpa = str(vendor.get("dpa_in_place", "unknown"))
    soc2_status = str(vendor.get("soc2_status", "Unknown"))
    business_owner = str(vendor.get("business_owner", "")).strip()

    if data_access in {"PII", "PHI", "Personal"} and has_dpa.lower() not in {"yes", "true"}:
        score += 22
        triggered_rules.append("Handles personal data without DPA.")

    if data_access in {"Confidential", "Financial", "PII", "PHI"} and soc2_status != "Current":
        score += 18
        triggered_rules.append("Sensitive/confidential data handling without current SOC 2 evidence.")

    if data_access.lower() == "unknown":
        score += 14
        triggered_rules.append("Unknown data access scope increases uncertainty risk.")
        missing_facts.append("Data classification and access scope.")

    if not business_owner or business_owner.lower() == "unknown":
        score += 10
        triggered_rules.append("No accountable business owner identified.")
        missing_facts.append("Assigned internal business owner.")

    missing_docs = str(vendor.get("missing_docs", "None"))
    if missing_docs and missing_docs != "None":
        score += 10
        triggered_rules.append("Required vendor intake documents are missing.")
        missing_facts.extend([f"Document: {d.strip()}" for d in missing_docs.split(";") if d.strip()])

    risk_level = "High" if score >= 50 else "Medium" if score >= 25 else "Low"
    human_review_required = _human_review_required(risk_level, missing_facts)

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "triggered_rules": triggered_rules,
        "missing_facts": missing_facts,
        "human_review_required": human_review_required,
        "escalation_route": _escalation_route(risk_level, "Vendor Risk"),
        "recommended_next_steps": _next_steps(
            risk_level,
            missing_facts,
            [
                "Confirm security posture (SOC 2, controls, incident response).",
                "Validate DPA/privacy terms and data minimization obligations.",
            ],
        ),
    }


def score_lease_readiness_dict(lease: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    triggered_rules: List[str] = []
    missing_facts: List[str] = []

    legal_names = str(lease.get("legal_names_complete", "unknown"))
    move_in_date = str(lease.get("move_in_date", "")).strip()
    deposit_status = str(lease.get("deposit_status", "")).strip()
    utilities_clarity = str(lease.get("utilities_clarity", "unknown"))

    if legal_names.lower() not in {"yes", "true"}:
        score += 18
        triggered_rules.append("Missing/incomplete legal names means intake is not ready.")
        missing_facts.append("Complete legal entity names for all parties.")

    if not move_in_date or move_in_date.lower() == "unknown":
        score += 16
        triggered_rules.append("Missing move-in date means intake is not ready.")
        missing_facts.append("Planned move-in date.")

    if not deposit_status or deposit_status.lower() == "unknown":
        score += 14
        triggered_rules.append("Missing deposit status means intake is not ready.")
        missing_facts.append("Deposit payment/waiver status.")

    if utilities_clarity.lower() in {"no", "unclear", "unknown"}:
        score += 10
        triggered_rules.append("Unclear utilities responsibilities create operational risk.")
        missing_facts.append("Utility responsibility matrix (landlord vs tenant).")

    for optional_field, label in [
        ("pets_policy_known", "Pets policy"),
        ("parking_terms_known", "Parking terms"),
        ("additional_occupants_known", "Additional occupants terms"),
    ]:
        val = str(lease.get(optional_field, "unknown")).lower()
        if val in {"unknown", "", "none"}:
            score += 4
            triggered_rules.append(f"{label} unknown; follow-up required.")
            missing_facts.append(label)

    risk_level = "High" if score >= 50 else "Medium" if score >= 25 else "Low"
    human_review_required = _human_review_required(risk_level, missing_facts)

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "triggered_rules": triggered_rules,
        "missing_facts": missing_facts,
        "human_review_required": human_review_required,
        "escalation_route": _escalation_route(risk_level, "Lease Ops"),
        "recommended_next_steps": _next_steps(
            risk_level,
            missing_facts,
            [
                "Complete intake checklist before lease readiness sign-off.",
                "Validate financial and operational obligations with facilities/legal.",
            ],
        ),
    }


def score_governance_maturity_dict(governance: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    triggered_rules: List[str] = []
    missing_facts: List[str] = []

    if str(governance.get("human_review_gate", "no")).lower() not in {"yes", "true"}:
        score += 22
        triggered_rules.append("No human review gate in workflow design.")

    if str(governance.get("audit_log_enabled", "no")).lower() not in {"yes", "true"}:
        score += 20
        triggered_rules.append("No audit log capability for decisions.")

    if str(governance.get("prompt_versioning", "no")).lower() not in {"yes", "true"}:
        score += 12
        triggered_rules.append("No prompt versioning reduces traceability/change control.")

    if str(governance.get("evaluation_tests", "no")).lower() not in {"yes", "true"}:
        score += 12
        triggered_rules.append("No evaluation tests for quality/safety assurance.")

    if str(governance.get("confidentiality_policy", "no")).lower() not in {"yes", "true"}:
        score += 20
        triggered_rules.append("No confidentiality policy for AI-assisted workflows.")

    for required in ["owner", "last_reviewed_date"]:
        if not str(governance.get(required, "")).strip():
            missing_facts.append(required)

    risk_level = "High" if score >= 50 else "Medium" if score >= 25 else "Low"
    human_review_required = _human_review_required(risk_level, missing_facts)

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "triggered_rules": triggered_rules,
        "missing_facts": missing_facts,
        "human_review_required": human_review_required,
        "escalation_route": _escalation_route(risk_level, "AI Governance"),
        "recommended_next_steps": _next_steps(
            risk_level,
            missing_facts,
            [
                "Define and enforce governance controls with accountable owners.",
                "Establish recurring control testing and policy review cadence.",
            ],
        ),
    }


# Backward-compatible wrappers used by existing pages.
def score_contract(contract: Dict, rules: Dict) -> Tuple[int, List[str], str]:
    result = score_contract_dict(contract)
    action = "Escalate" if result["risk_level"] == "High" else "Review" if result["risk_level"] == "Medium" else "Approve"
    return result["risk_score"], result["triggered_rules"], action


def score_vendor(vendor: Dict, rules: Dict) -> Tuple[int, List[str], str, List[str]]:
    result = score_vendor_dict(vendor)
    action = "Escalate" if result["risk_level"] == "High" else "Review" if result["risk_level"] == "Medium" else "Approve"
    return result["risk_score"], result["triggered_rules"], action, result["missing_facts"]


def score_lease(lease: Dict, rules: Dict) -> Tuple[int, List[str], str, List[str]]:
    result = score_lease_readiness_dict(lease)
    action = "Escalate" if result["risk_level"] == "High" else "Review" if result["risk_level"] == "Medium" else "Approve"
    return result["risk_score"], result["triggered_rules"], action, result["missing_facts"]
