import streamlit as st
import pandas as pd

st.title("Governance Controls")
st.markdown("### AI Governance Design and Control Mapping")
st.divider()
st.caption("Governance blueprint for a simulated AI workflow prototype. Educational mapping only; not legal advice.")

st.warning(
    "This page provides an educational mapping of governance concepts for portfolio review. "
    "It does not claim formal compliance with NIST AI RMF, ISO/IEC 42001, SOC 2, or legal/regulatory requirements."
)

st.subheader("1) Human Review Gates")
st.markdown(
    """
- **Gate A (Intake completeness):** Missing facts block autonomous progression.
- **Gate B (Risk threshold):** Medium/High-risk outcomes require named human reviewer sign-off.
- **Gate C (Pre-action validation):** Reviewer confirms recommendation, rationale, and escalation path.
- **Gate D (Final disposition):** Approval/rejection logged with accountable owner and timestamp.
"""
)

st.subheader("2) Confidentiality and Data Controls")
st.markdown(
    """
- Data minimization: only required workflow fields are processed.
- Classification-aware handling: personal/confidential data receives stricter routing.
- Redaction-first posture for exported artifacts.
- No production secrets or live client data in this prototype.
- Access separation concept: intake users vs. approvers vs. auditors.
"""
)

st.subheader("3) AI-Use Approval Workflow")
workflow_df = pd.DataFrame(
    [
        ["Use-case proposal", "Business owner", "Define objective, risk class, data sensitivity"],
        ["Control design", "Legal/Ops + Security", "Specify guardrails, review gates, escalation"],
        ["Pilot approval", "Governance lead", "Approve limited rollout with monitoring"],
        ["Operational review", "Human reviewer", "Validate outputs, document exceptions"],
        ["Periodic re-approval", "Control owner", "Reassess drift, incidents, and test performance"],
    ],
    columns=["Stage", "Owner", "Expected Evidence"],
)
st.dataframe(workflow_df, width='stretch')

st.subheader("4) Prompt Library and Versioning")
st.markdown(
    """
- Maintain a prompt registry with: purpose, owner, approved audience, and risk tier.
- Version prompts semantically (e.g., `contract_triage_v1.2`).
- Track change reason, approver, and rollback reference per version.
- Bind prompt version to every workflow event and evaluation run.
"""
)

st.subheader("5) Audit-Log Requirements")
st.markdown(
    """
Minimum fields for each event:
- timestamp
- workflow type
- input identifier
- risk score and risk level
- action taken
- reviewer status/owner
- explanation + triggered controls
- model/prompt version (production target state)
"""
)

st.subheader("6) Escalation Triggers")
triggers = [
    "High-risk score or policy-threshold breach",
    "Missing mandatory intake facts after follow-up window",
    "Conflicting reviewer interpretations",
    "Potential privacy/security incident indicators",
    "Hallucination or unsupported-claim detection",
    "Repeated control-test failures in Evaluation Lab",
]
for t in triggers:
    st.write(f"- {t}")

st.subheader("7) NIST AI RMF-style Mapping (Educational)")
rmf_df = pd.DataFrame(
    [
        ["Govern", "Define accountable owners, policies, and risk appetite for each workflow."],
        ["Map", "Document use context, stakeholders, data sensitivity, and failure modes."],
        ["Measure", "Evaluate quality, escalation accuracy, missing-info detection, and audit completeness."],
        ["Manage", "Apply remediations, monitor drift, retrain policy logic, and tighten controls."],
    ],
    columns=["Function", "Prototype Implementation Pattern"],
)
st.dataframe(rmf_df, width='stretch')

st.subheader("8) ISO/IEC 42001-inspired Management-System Controls (Educational)")
iso_controls = [
    "Governance roles and responsibilities documented for AI-assisted workflows.",
    "Risk assessment cadence with control effectiveness review.",
    "Change management for prompts/rules and deployment settings.",
    "Incident handling workflow for harmful or unsafe outputs.",
    "Training and awareness expectations for reviewers and operators.",
    "Internal assurance artifacts (evaluation reports, audit trails, decision logs).",
]
for c in iso_controls:
    st.write(f"- {c}")

st.subheader("9) OWASP LLM-style Security Risk Controls (Educational)")
owasp_df = pd.DataFrame(
    [
        ["Prompt injection", "Treat untrusted input as data; isolate instructions from content; require human confirmation for high-impact actions."],
        ["Sensitive information disclosure", "Redact sensitive fields in outputs/logs; least-privilege data views; no secrets in prompts."],
        ["Excessive agency", "No autonomous external actions in prototype; human approval required for decisions and escalations."],
        ["Insecure output handling", "Output sanitization and reviewer validation before downstream use or export."],
        ["System prompt leakage", "Do not expose internal guardrails verbatim; keep system/control prompts restricted."],
        ["Hallucination/misinformation", "Require source-field grounding and mark uncertain outputs for review."],
        ["Unbounded usage", "Apply usage limits, review queues, and exception monitoring for scale scenarios."],
    ],
    columns=["Risk Category", "Prototype Control Pattern"],
)
st.dataframe(owasp_df, width='stretch')

st.info(
    "Prototype note: this governance page demonstrates control-design thinking and implementation judgment, "
    "not a formal certification or compliance attestation."
)
