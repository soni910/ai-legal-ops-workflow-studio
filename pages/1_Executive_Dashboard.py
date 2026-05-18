import streamlit as st
import pandas as pd
from utils.app_common import page_header, safe_read_csv, risk_badge

from utils.audit import build_audit_log
from utils.risk_engine import load_rules, score_contract, score_vendor, score_lease
from utils.report_generator import summarize_evaluations

page_header("Executive Dashboard", "Portfolio-Level AI Workflow Monitoring", "Executive-facing simulated AI operations dashboard. Simulated AI workflow prototype; not legal advice.")

# -----------------------------
# Data load
# -----------------------------
contracts = safe_read_csv("data/sample_contracts.csv", ["contract_id","counterparty"])
vendors = safe_read_csv("data/sample_vendors.csv", ["vendor_id","vendor_name"])
leases = safe_read_csv("data/sample_lease_intakes.csv", ["lease_id","site_name"])
evals = safe_read_csv("data/evaluation_tests.csv", ["test_id","status"])
audit_log = build_audit_log().sort_values("timestamp", ascending=False)
rules = load_rules()

# -----------------------------
# Helper scoring wrappers
# -----------------------------
def bucket_from_score(score: int) -> str:
    if score >= rules["thresholds"]["escalate"]:
        return "High"
    if score >= rules["thresholds"]["review"]:
        return "Medium"
    return "Low"


contract_results = []
for _, r in contracts.iterrows():
    row = r.to_dict()
    score, reasons, action = score_contract(row, rules)
    contract_results.append(
        {
            "workflow": "Contract",
            "id": row["contract_id"],
            "score": score,
            "action": action,
            "risk_bucket": bucket_from_score(score),
            "human_review_required": action in {"Review", "Escalate", "Reject"},
            "missing_docs_count": 0,
            "open_escalation": action in {"Escalate", "Reject"},
            "reason_count": len(reasons),
        }
    )

vendor_results = []
for _, r in vendors.iterrows():
    row = r.to_dict()
    score, reasons, action, missing = score_vendor(row, rules)
    vendor_results.append(
        {
            "workflow": "Vendor",
            "id": row["vendor_id"],
            "score": score,
            "action": action,
            "risk_bucket": bucket_from_score(score),
            "human_review_required": action in {"Review", "Escalate", "Reject"},
            "missing_docs_count": len(missing),
            "open_escalation": action in {"Escalate", "Reject"},
            "reason_count": len(reasons),
        }
    )

lease_results = []
for _, r in leases.iterrows():
    row = r.to_dict()
    score, reasons, action, missing = score_lease(row, rules)
    lease_results.append(
        {
            "workflow": "Lease",
            "id": row["lease_id"],
            "score": score,
            "action": action,
            "risk_bucket": bucket_from_score(score),
            "human_review_required": action in {"Review", "Escalate", "Reject"},
            "missing_docs_count": len(missing),
            "open_escalation": action in {"Escalate", "Reject"},
            "reason_count": len(reasons),
        }
    )

results_df = pd.DataFrame(contract_results + vendor_results + lease_results)
ev_summary = summarize_evaluations(evals)

# -----------------------------
# Session-state persistence for dashboard KPIs
# -----------------------------
if "executive_dashboard_metrics" not in st.session_state:
    st.session_state.executive_dashboard_metrics = {}

metrics = {
    "total_reviews": int(len(results_df)),
    "high_risk_reviews": int((results_df["risk_bucket"] == "High").sum()),
    "medium_risk_reviews": int((results_df["risk_bucket"] == "Medium").sum()),
    "low_risk_reviews": int((results_df["risk_bucket"] == "Low").sum()),
    "human_review_required": int(results_df["human_review_required"].sum()),
    "open_escalations": int(results_df["open_escalation"].sum()),
    "missing_document_count": int(results_df["missing_docs_count"].sum()),
    "governance_maturity_score": int(round((ev_summary["pass_rate"] * 0.7) + (100 - (results_df["open_escalation"].mean() * 100)) * 0.3, 0)),
}

st.session_state.executive_dashboard_metrics = metrics

# -----------------------------
# Employer-facing overview
# -----------------------------
st.markdown(
    """
This dashboard illustrates how legal and operations leaders can monitor AI-assisted workflows with clear operating signals:
- triage throughput,
- risk concentration,
- human-review load,
- escalation pressure,
- documentation quality,
- and governance effectiveness.
"""
)

# -----------------------------
# KPI cards
# -----------------------------
row1 = st.columns(4)
row1[0].metric("Total Simulated Reviews", metrics["total_reviews"])
row1[1].metric("High-Risk Reviews", metrics["high_risk_reviews"])
row1[2].metric("Medium-Risk Reviews", metrics["medium_risk_reviews"])
row1[3].metric("Low-Risk Reviews", metrics["low_risk_reviews"])

row2 = st.columns(4)
row2[0].metric("Human-Review Required", metrics["human_review_required"])
row2[1].metric("Open Escalations", metrics["open_escalations"])
row2[2].metric("Missing-Document Count", metrics["missing_document_count"])
row2[3].metric("Governance Maturity Score", f"{metrics['governance_maturity_score']}/100")

# -----------------------------
# Charts
# -----------------------------
left, right = st.columns(2)

with left:
    st.subheader("Risk Distribution")
    risk_dist = results_df["risk_bucket"].value_counts().reindex(["High", "Medium", "Low"], fill_value=0)
    st.bar_chart(risk_dist)

with right:
    st.subheader("Workflow Type Volume")
    workflow_dist = results_df["workflow"].value_counts().sort_values(ascending=False)
    st.bar_chart(workflow_dist)

# -----------------------------
# Operational details
# -----------------------------
st.subheader("Recent Audit-Ready Workflow Records")
st.dataframe(audit_log.head(8), use_container_width=True)

with st.expander("Show scored workflow dataset"):
    st.dataframe(results_df.sort_values(["score", "workflow"], ascending=[False, True]), use_container_width=True)

st.info(
    f"Evaluation pass rate is {ev_summary['pass_rate']}% across {ev_summary['total']} tests. "
    "This is a simulated governance signal intended for portfolio review and control-design discussion, not legal or compliance advice."
)
