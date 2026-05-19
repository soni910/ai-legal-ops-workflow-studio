import streamlit as st

st.set_page_config(page_title="AI Legal & Operations Workflow Studio", page_icon="⚖️", layout="wide")

st.title("AI Legal & Operations Workflow Studio")
st.markdown("### AI Operations Portfolio: Legal, Vendor Risk, Lease, Governance, and Controls")
st.markdown(
    "This application presents a **simulated AI workflow prototype** focused on operational credibility: "
    "structured intake, rule-based risk scoring, human-review controls, evaluation discipline, and audit-ready records."
)

st.divider()

st.markdown("### What to Review First")
col1, col2, col3 = st.columns(3)
with col1:
    feature_card(
        "Executive Dashboard",
        "Review portfolio-level throughput, risk distribution, human-review demand, escalation pressure, and governance maturity signals.",
    )
with col2:
    feature_card(
        "Workflow Modules",
        "Run structured contract, vendor, and lease intake scenarios with deterministic risk scoring and reviewer-ready next steps.",
    )
with col3:
    feature_card(
        "Controls Evidence",
        "Inspect governance mappings, evaluation test coverage, and exportable audit logs that show implementation judgment.",
    )

st.markdown("### Methodology and Boundaries")
with st.expander("Read the prototype boundaries", expanded=True):
    st.markdown(
        """
- Uses **deterministic simulated outputs** and **rule-based risk scoring** only.
- Demonstrates workflow design, governance controls, evaluation thinking, and auditability.
- Does **not** connect to paid APIs, live client systems, external databases, or confidential production data.
- Intended for portfolio review and implementation discussion, not legal advice or compliance attestation.
"""
    )

st.info(
    "Suggested path: Executive Dashboard → Contract Triage → Vendor Risk Intake → Lease Operations → Governance Controls → Evaluation Lab → Audit Log → Case Study & Roadmap."
)
