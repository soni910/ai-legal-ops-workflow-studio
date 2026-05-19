import streamlit as st
import pandas as pd
from utils.app_common import chart_panel_header, dashboard_hero, insight_card, kpi_card, page_header, safe_read_csv

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
# Executive summary and KPI cards
# -----------------------------
risk_dist = results_df["risk_bucket"].value_counts().reindex(["High", "Medium", "Low"], fill_value=0)
workflow_dist = results_df["workflow"].value_counts().sort_values(ascending=False)
priority_review_rate = int(round((metrics["human_review_required"] / metrics["total_reviews"]) * 100, 0)) if metrics["total_reviews"] else 0
escalation_rate = int(round((metrics["open_escalations"] / metrics["total_reviews"]) * 100, 0)) if metrics["total_reviews"] else 0

dashboard_hero(
    "Operational command center for governed AI-assisted workflows",
    "Monitor simulated intake volume, risk concentration, escalation pressure, documentation gaps, and evaluation performance across legal and operations workflows.",
    [
        f"{metrics['total_reviews']} simulated reviews",
        f"{priority_review_rate}% require human review",
        f"{ev_summary['pass_rate']}% evaluation pass rate",
        "No paid APIs or live confidential data",
    ],
)

st.markdown("### Executive KPI Snapshot")
kpi_row_1 = st.columns(4)
with kpi_row_1[0]:
    kpi_card("Total reviews", metrics["total_reviews"], "Combined contract, vendor, and lease workflow records.", "blue")
with kpi_row_1[1]:
    kpi_card("High risk", metrics["high_risk_reviews"], "Items meeting escalation-level rule thresholds.", "high")
with kpi_row_1[2]:
    kpi_card("Medium risk", metrics["medium_risk_reviews"], "Items needing reviewer attention before approval.", "medium")
with kpi_row_1[3]:
    kpi_card("Low risk", metrics["low_risk_reviews"], "Items with lower operational or legal-risk signals.", "low")

kpi_row_2 = st.columns(4)
with kpi_row_2[0]:
    kpi_card("Human review", metrics["human_review_required"], f"{priority_review_rate}% of simulated records route to review.", "blue")
with kpi_row_2[1]:
    kpi_card("Open escalations", metrics["open_escalations"], f"{escalation_rate}% of records require escalation routing.", "high")
with kpi_row_2[2]:
    kpi_card("Missing docs", metrics["missing_document_count"], "Incomplete intake facts or documentation gaps detected.", "slate")
with kpi_row_2[3]:
    kpi_card("Governance score", f"{metrics['governance_maturity_score']}/100", "Composite of evaluation quality and escalation control signals.", "blue")

st.markdown("### Executive Interpretation")
insight_cols = st.columns(3)
with insight_cols[0]:
    insight_card("Risk concentration", f"{metrics['high_risk_reviews']} high-risk records are visible for escalation review, helping leaders focus scarce reviewer capacity.")
with insight_cols[1]:
    insight_card("Review workload", f"{metrics['human_review_required']} records require human review, showing how governed automation still preserves accountable checkpoints.")
with insight_cols[2]:
    insight_card("Control signal", f"Evaluation coverage is summarized at {ev_summary['pass_rate']}%, creating a measurable quality-control signal for workflow governance.")

st.markdown("### Leadership Action Queue")
action_queue = pd.DataFrame(
    [
        [
            "High-risk reviews",
            metrics["high_risk_reviews"],
            "Confirm escalation owner and prioritize reviewer capacity for high-risk contract/vendor/lease records.",
        ],
        [
            "Human-review workload",
            f"{metrics['human_review_required']} records / {priority_review_rate}%",
            "Track whether reviewer volume is operationally sustainable before expanding workflow scope.",
        ],
        [
            "Missing documentation",
            metrics["missing_document_count"],
            "Tighten intake requirements and add follow-up prompts where repeated documentation gaps appear.",
        ],
        [
            "Evaluation coverage",
            f"{ev_summary['pass_rate']}% pass rate",
            "Review failed or severe test cases before piloting any live-LLM workflow component.",
        ],
    ],
    columns=["Operating Signal", "Current Snapshot", "Recommended Management Action"],
)
st.dataframe(action_queue, width="stretch", hide_index=True)

# -----------------------------
# Charts
# -----------------------------
st.markdown("### Portfolio Distribution")
left, right = st.columns(2)

with left:
    chart_panel_header("Risk distribution", "Rule-based risk bands across all simulated workflow records.")
    st.bar_chart(risk_dist)

with right:
    chart_panel_header("Workflow volume", "Review distribution across contract, vendor, and lease operations modules.")
    st.bar_chart(workflow_dist)

# -----------------------------
# Operational details
# -----------------------------
st.markdown("### Audit-Ready Operating Evidence")
st.caption("Recent workflow records show timestamped decisions, routing, scores, and explanation fields for reviewer accountability.")
audit_preview_columns = [
    "timestamp",
    "module",
    "workflow_id",
    "risk_score",
    "risk_level",
    "human_review_required",
    "escalation_route",
    "decision_status",
]
st.dataframe(audit_log[audit_preview_columns].head(8), width="stretch", hide_index=True)

dataset_expander = st.expander("Show scored workflow dataset")
dataset_expander.dataframe(
    results_df.sort_values(["score", "workflow"], ascending=[False, True]),
    width="stretch",
    hide_index=True,
)

st.info(
    f"Evaluation pass rate is {ev_summary['pass_rate']}% across {ev_summary['total']} tests. "
    "This dashboard is a simulated governance signal intended for portfolio review and control-design discussion, not legal or compliance advice."
)
