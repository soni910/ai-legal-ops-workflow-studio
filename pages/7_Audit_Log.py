import streamlit as st

from utils.audit import init_session_audit_log, session_audit_df, build_audit_log
from utils.app_common import intake_hero, kpi_card, page_header

page_header("Audit Log", "Workflow Traceability and Decision Evidence", "Structured auditability for simulated AI-assisted workflows. Not legal advice.")

intake_hero(
    "Audit evidence and traceability center",
    "Review timestamped workflow records, risk rationale, escalation routes, and reviewer checkpoints for governance oversight.",
    ["Decision evidence", "Reviewer accountability", "Exportable logs", "Governance monitoring"],
)

init_session_audit_log(st.session_state)

# Seed the session audit log with deterministic seed records only if empty.
if not st.session_state.workflow_audit_log:
    for _, row in build_audit_log().iterrows():
        st.session_state.workflow_audit_log.append(row.to_dict())

log_df = session_audit_df(st.session_state)

st.subheader("Why audit logs matter")
st.write(
    "Audit logs support traceability, accountability, and quality governance in AI-assisted workflows by "
    "recording decisions, risk rationale, and human-review checkpoints for later oversight and improvement."
)

metric_cols = st.columns(4)
with metric_cols[0]:
    kpi_card("Total records", len(log_df), "All captured audit events currently in session scope.", "blue")
with metric_cols[1]:
    kpi_card("Human review", int(log_df["human_review_required"].sum()) if len(log_df) else 0, "Events that required accountable reviewer confirmation.", "medium")
with metric_cols[2]:
    kpi_card("High-risk records", int((log_df["risk_level"] == "High").sum()) if len(log_df) else 0, "Events routed through elevated escalation criteria.", "high")
with metric_cols[3]:
    kpi_card("Unique modules", int(log_df["module"].nunique()) if len(log_df) else 0, "Workflow modules represented in current audit evidence.", "slate")

st.subheader("Audit Log Records")
st.caption("These records demonstrate traceability fields used for governance, oversight, and post-decision review.")
st.dataframe(log_df, width='stretch', hide_index=True)

csv_data = log_df.to_csv(index=False).encode("utf-8")
json_data = log_df.to_json(orient="records", indent=2).encode("utf-8")

c1, c2 = st.columns(2)
with c1:
    st.download_button(
        "Download Audit Log (CSV)",
        data=csv_data,
        file_name="ai_workflow_audit_log.csv",
        mime="text/csv",
    )
with c2:
    st.download_button(
        "Download Audit Log (JSON)",
        data=json_data,
        file_name="ai_workflow_audit_log.json",
        mime="application/json",
    )
