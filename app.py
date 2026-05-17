import streamlit as st

st.set_page_config(page_title="AI Legal & Operations Workflow Studio", page_icon="⚖️", layout="wide")

st.title("AI Legal & Operations Workflow Studio")
st.markdown("### Enterprise Workflow Simulation for Legal, Operations, and AI Governance")
st.markdown(
    "This portfolio application demonstrates **structured AI workflow design** across contract triage, "
    "vendor risk, lease operations, governance controls, evaluation, and auditability."
)

st.divider()

with st.expander("Methodology and Boundaries"):
    st.markdown("""
- This app uses **deterministic simulated outputs** and **rule-based risk scoring**.
- It demonstrates workflow design, governance controls, evaluation thinking, and auditability.
- It does **not** connect to paid APIs, live client systems, or confidential production data.
- It is intended for portfolio review, not legal advice or compliance attestation.
""")

st.info(
    "Navigation: use the left sidebar to access workflow modules, governance controls, evaluation lab, and audit records."
)

st.caption(
    "Disclaimer: This is a simulated educational prototype for portfolio review. "
    "It does not provide legal advice or compliance determinations."
)
