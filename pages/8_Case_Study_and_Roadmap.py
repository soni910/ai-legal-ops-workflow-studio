import streamlit as st
import pandas as pd
from utils.app_common import page_header

page_header("Case Study and Roadmap", "Employer-Facing Project Narrative and Production Path", "Employer-facing portfolio case study. Simulated AI workflow prototype; not legal advice.")

st.subheader("1) Project Overview")
st.write(
    "AI Legal & Operations Workflow Studio is a deterministic Streamlit portfolio project that showcases "
    "how AI-assisted legal and operations workflows can be structured with governance controls, risk triage, "
    "evaluation checks, and auditable decision logging."
)

st.subheader("2) Problem Statement")
st.write(
    "Legal and operations teams often manage high-volume intake with inconsistent data quality, limited "
    "risk triage consistency, and weak visibility into why decisions were made or escalated."
)

st.subheader("3) Solution")
st.write(
    "This project presents an enterprise-style workflow approach: structured intake, rule-based risk scoring, "
    "human-review gates, governance mappings, evaluation test cases, and exportable audit records."
)

st.subheader("4) Modules")
modules_df = pd.DataFrame(
    [
        ["Executive Dashboard", "Portfolio-level risk/throughput view and governance indicators"],
        ["Contract Triage", "Clause risk checks, escalation logic, and next-step recommendations"],
        ["Vendor Risk Intake", "Third-party risk intake with privacy/security control signals"],
        ["Lease Operations", "Readiness checks for operational and legal intake completeness"],
        ["Governance Controls", "Educational mapping to governance and security control frameworks"],
        ["Evaluation Lab", "Deterministic quality-control matrix and pass/fail coverage"],
        ["Audit Log", "Structured decision history with exportable records"],
        ["Case Study & Roadmap", "Business narrative, architecture, and production upgrade plan"],
    ],
    columns=["Module", "Purpose"],
)
st.dataframe(modules_df, width='stretch', hide_index=True)

st.subheader("5) Skills Demonstrated")
st.markdown(
    """
- AI workflow design for legal/ops contexts
- Risk policy translation into deterministic scoring logic
- Human-in-the-loop governance and escalation design
- Evaluation mindset (quality, safety, and control testing)
- Auditability and stakeholder-facing reporting
- Product framing and communication for non-technical partners
"""
)

st.subheader("6) Why the Current Version is Simulated")
st.write(
    "The current version is intentionally simulated to keep the simulated AI workflow prototype reproducible, safe, low-cost, "
    "and deployable without secrets, paid APIs, or production data dependencies."
)

st.subheader("7) Production Upgrade Path")
roadmap_df = pd.DataFrame(
    [
        ["Stage 1: Simulated prototype", "Current", "Deterministic rules, static sample data, session audit logs"],
        ["Stage 2: Controlled live LLM pilot", "Next", "Limited-scope API integration, guarded prompts, approved test datasets, reviewer queue"],
        ["Stage 3: Production workflow system", "Target", "Hardened orchestration, RBAC, persistent audit DB, monitoring, continuous evaluation"],
    ],
    columns=["Stage", "Status", "Capabilities"],
)
st.dataframe(roadmap_df, width='stretch', hide_index=True)

st.subheader("8) Architecture Diagram (Conceptual)")
st.markdown(
    """
```text
[User Intake Form]
      |
      v
[Validation + Rule Engine] ---> [Evaluation Lab Checks]
      |
      v
[Risk Decision + Next Steps] ---> [Human Review Gate]
      |                                |
      v                                v
[Session Audit Log] ------------> [Audit Export (CSV/JSON)]
      |
      v
[Executive Dashboard + Reporting]
```
"""
)

st.subheader("Simulation vs Production Comparison")
comparison_df = pd.DataFrame(
    [
        ["AI Output Generation", "Static/deterministic outputs", "Live LLM with guardrails and prompt/version controls"],
        ["Audit Storage", "Session-state audit log", "Persistent database-backed immutable audit log"],
        ["Document Inputs", "Sample documents/datasets", "Approved enterprise document repository"],
        ["Evaluation", "Manual in-app evaluation table", "Automated evaluation harness with regression suites"],
        ["Access Control", "No authentication", "Role-based permissions (RBAC/SSO)"],
        ["Retrieval", "Simulated RAG behavior", "Real retrieval over approved sources with citations"],
    ],
    columns=["Dimension", "Current Prototype", "Production Target"],
)
st.dataframe(comparison_df, width='stretch', hide_index=True)

st.subheader("9) Limitations")
st.markdown(
    """
- No live LLM integrations or external service orchestration
- No real-time document ingestion pipeline
- No production authentication/authorization stack
- No persistent database in this prototype deployment
- Educational governance mappings, not formal compliance attestations
"""
)

st.subheader("10) Suggested Resume Bullet")
st.code(
    "Designed and built a Streamlit-based AI Legal & Operations Workflow Studio demonstrating deterministic "
    "risk triage, governance controls, evaluation testing, and structured audit logging across contract, vendor, and lease workflows.",
    language="text",
)

st.subheader("11) Suggested Interview Explanation")
st.write(
    "I designed this as a production-minded simulation to demonstrate implementation judgment beyond UI development. "
    "I translated legal/ops risk concepts into deterministic workflows with review gates, evaluation controls, "
    "and auditability. Then I defined a realistic roadmap from prototype to controlled pilot to production "
    "system with LLM integration, RBAC, persistent logs, and automated evaluation."
)

st.info("This case study is a portfolio prototype for educational demonstration and does not provide legal advice.")
