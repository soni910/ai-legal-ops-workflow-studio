import streamlit as st
from utils.app_common import apply_global_style, feature_card, hero_panel, render_sidebar_context

st.set_page_config(page_title="AI Legal & Operations Workflow Studio", page_icon="⚖️", layout="wide")
apply_global_style()
render_sidebar_context()

hero_panel(
    "Employer-grade AI operations portfolio",
    "AI Legal & Operations Workflow Studio",
    "A simulated enterprise workflow environment for contract triage, vendor risk, lease operations, governance controls, evaluation discipline, and audit-ready decision records.",
)

st.markdown(
    "This application demonstrates how AI-assisted workflows can be designed responsibly before live LLM adoption: "
    "structured intake, deterministic rule-based scoring, human-review gates, quality checks, and traceable operating evidence."
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
