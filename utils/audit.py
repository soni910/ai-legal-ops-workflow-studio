"""Audit utilities for deterministic workflow logging."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List
import pandas as pd

REQUIRED_AUDIT_FIELDS = [
    "workflow_id",
    "timestamp",
    "module",
    "input_category",
    "risk_score",
    "risk_level",
    "triggered_rules",
    "missing_facts",
    "human_review_required",
    "escalation_route",
    "recommended_next_steps",
    "prompt_version",
    "schema_version",
    "decision_status",
]


def init_session_audit_log(session_state: Any) -> None:
    if "workflow_audit_log" not in session_state:
        session_state.workflow_audit_log = []


def create_audit_record(
    workflow_id: str,
    module: str,
    input_category: str,
    risk_result: Dict[str, Any],
    decision_status: str,
    prompt_version: str = "sim_prompt_v1",
    schema_version: str = "audit_schema_v1",
) -> Dict[str, Any]:
    return {
        "workflow_id": workflow_id,
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "module": module,
        "input_category": input_category,
        "risk_score": risk_result.get("risk_score", 0),
        "risk_level": risk_result.get("risk_level", "Low"),
        "triggered_rules": "; ".join(risk_result.get("triggered_rules", [])),
        "missing_facts": "; ".join(risk_result.get("missing_facts", [])),
        "human_review_required": bool(risk_result.get("human_review_required", False)),
        "escalation_route": risk_result.get("escalation_route", "No escalation required"),
        "recommended_next_steps": "; ".join(risk_result.get("recommended_next_steps", [])),
        "prompt_version": prompt_version,
        "schema_version": schema_version,
        "decision_status": decision_status,
    }


def append_audit_record(session_state: Any, record: Dict[str, Any]) -> None:
    init_session_audit_log(session_state)
    session_state.workflow_audit_log.append(record)


def session_audit_df(session_state: Any) -> pd.DataFrame:
    init_session_audit_log(session_state)
    if not session_state.workflow_audit_log:
        return pd.DataFrame(columns=REQUIRED_AUDIT_FIELDS)
    df = pd.DataFrame(session_state.workflow_audit_log)
    for col in REQUIRED_AUDIT_FIELDS:
        if col not in df.columns:
            df[col] = ""
    return df[REQUIRED_AUDIT_FIELDS]


def build_audit_log() -> pd.DataFrame:
    """Legacy seeded log for fallback visualization."""
    base = datetime(2026, 5, 15, 9, 0)
    rows: List[Dict[str, Any]] = []
    samples = [
        ("WF-CTR-001", "Contract Triage", "Contract", 48, "Medium", True, "Legal Operations Reviewer", "Review"),
        ("WF-VND-003", "Vendor Risk Intake", "Vendor", 65, "High", True, "Vendor Risk Counsel + Risk Committee", "Escalate"),
        ("WF-LSE-102", "Lease Operations", "Lease", 44, "Medium", True, "Lease Ops Reviewer", "Review"),
    ]
    for i, s in enumerate(samples):
        rows.append(
            {
                "workflow_id": s[0],
                "timestamp": (base + timedelta(minutes=i * 9)).isoformat() + "Z",
                "module": s[1],
                "input_category": s[2],
                "risk_score": s[3],
                "risk_level": s[4],
                "triggered_rules": "Simulated rule trigger",
                "missing_facts": "",
                "human_review_required": s[5],
                "escalation_route": s[6],
                "recommended_next_steps": "Route to reviewer",
                "prompt_version": "sim_prompt_v1",
                "schema_version": "audit_schema_v1",
                "decision_status": s[7],
            }
        )
    return pd.DataFrame(rows, columns=REQUIRED_AUDIT_FIELDS)
