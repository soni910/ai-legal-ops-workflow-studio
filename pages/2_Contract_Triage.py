import streamlit as st
import pandas as pd
from utils.app_common import page_header, safe_read_csv, risk_badge
from utils.risk_engine import score_contract_dict
from utils.audit import init_session_audit_log, create_audit_record, append_audit_record

page_header("Contract Triage", "Structured Contract Risk Intake and Escalation", "Simulated AI contract triage workflow for employer review. Not legal advice.")

# Session-state audit log bucket for cross-page workflow tracking
init_session_audit_log(st.session_state)

sample_contracts = safe_read_csv("data/sample_contracts.csv", ["contract_id","contract_type"])
contract_types = sorted(sample_contracts["contract_type"].dropna().unique().tolist())

with st.form("contract_triage_form"):
    st.subheader("Structured Intake")

    col1, col2 = st.columns(2)
    with col1:
        contract_id = st.text_input("Contract ID", value="CTR-DEMO-001")
        counterparty = st.text_input("Counterparty", value="Fictional Vendor LLC")
        contract_type = st.selectbox("Contract Type", options=contract_types)
        governing_law = st.selectbox("Governing Law", options=["British Columbia", "Ontario", "Quebec", "Alberta", "Other"])
        governing_law = st.selectbox("Governing Law", options=["Delaware", "New York", "California", "Texas", "Other"])

    with col2:
        value_usd = st.number_input("Contract Value (USD)", min_value=0, value=125000, step=5000)
        term_months = st.number_input("Term (months)", min_value=1, value=24)
        termination_days = st.number_input("Termination Notice (days)", min_value=0, value=60)
        payment_terms_days = st.number_input("Payment Terms (days)", min_value=0, value=45)

    clause_text = st.text_area(
        "Sample Clause Excerpt",
        height=140,
        value=(
            "Vendor may update service terms upon notice. Customer data may be processed by subprocessors. "
            "Liability cap is excluded for data incidents."
        ),
    )

    st.markdown("**Risk Factors (checkbox assessment)**")
    r1, r2, r3 = st.columns(3)
    with r1:
        personal_data = st.checkbox("Processes personal data", value=True)
        uncapped_liability = st.checkbox("Uncapped liability", value=False)
    with r2:
        unilateral_amendment = st.checkbox("Unilateral amendment rights", value=True)
        no_termination_right = st.checkbox("No practical termination right", value=False)
    with r3:
        subprocessor_without_consent = st.checkbox("Subprocessors without consent", value=True)
        missing_security_terms = st.checkbox("Missing security terms", value=False)

    st.subheader("Business Context")
    business_owner = st.text_input("Business Owner", value="Legal Ops Manager")
    business_use = st.text_area("Intended Business Use", value="Core procurement workflow automation for AP and legal operations.")
    criticality = st.selectbox("Business Criticality", ["Low", "Medium", "High"], index=1)

    submitted = st.form_submit_button("Run Contract Risk Assessment")

if submitted:
    # Build contract payload expected by score_contract_dict
    contract_payload = {
        "contract_id": contract_id,
        "counterparty": counterparty,
        "contract_type": contract_type,
        "value_usd": value_usd,
        "term_months": term_months,
        "termination_days": 999 if no_termination_right else termination_days,
        "governing_law": governing_law,
        "data_processing": "Yes" if personal_data else "No",
        "liability_cap": "Uncapped" if uncapped_liability else "12 months fees",
        "unilateral_amendment_rights": "Yes" if unilateral_amendment else "No",
        "subprocessor_consent_required": "No" if subprocessor_without_consent else "Yes",
        "security_terms_present": "No" if missing_security_terms else "Yes",
        "payment_terms_days": payment_terms_days,
        "business_owner": business_owner,
        "business_use": business_use,
        "criticality": criticality,
        "sample_clause_text": clause_text,
    }

    result = score_contract_dict(contract_payload)

    st.subheader("Risk Decision")
    k1, k2, k3 = st.columns(3)
    k1.metric("Risk Score", result["risk_score"])
    k2.metric("Risk Level", risk_badge(result["risk_level"]))
    k3.metric("Human Review Required", "Yes" if result["human_review_required"] else "No")

    st.write("**Escalation Route:**", result["escalation_route"])

    tabs = st.tabs([
        "Triggered Rules",
        "Missing Facts",
        "Recommended Next Steps",
        "Simulated AI Output",
    ])

    with tabs[0]:
        if result["triggered_rules"]:
            for rule in result["triggered_rules"]:
                st.write(f"- {rule}")
        else:
            st.write("- No elevated rules triggered.")

    with tabs[1]:
        if result["missing_facts"]:
            for fact in result["missing_facts"]:
                st.write(f"- {fact}")
        else:
            st.write("- No missing facts identified.")

    with tabs[2]:
        for step in result["recommended_next_steps"]:
            st.write(f"- {step}")

    with tabs[3]:
        risk_level = result["risk_level"]
        approval_recommendation = "Escalate" if risk_level == "High" else "Review" if risk_level == "Medium" else "Approve"
        st.markdown("**Plain-English Summary**")
        st.write(
            f"This simulated review assessed {contract_type} with {counterparty} at ${value_usd:,.0f}. "
            f"The contract is currently rated **{risk_level} risk** based on selected legal and operational risk factors."
        )
        st.markdown("**Issue List**")
        issues = result["triggered_rules"] or ["No major issues identified."]
        st.write("\n".join([f"- {i}" for i in issues]))
        st.markdown("**Business Impact**")
        st.write("Elevated terms can increase financial exposure, privacy/compliance overhead, and negotiation cycle time.")
        st.markdown("**Negotiation Position**")
        st.write("Request balanced liability language, clear termination rights, subprocessor consent controls, and explicit security commitments.")
        st.markdown("**Suggested Revision**")
        st.code(
            "Vendor may not materially amend terms without mutual written agreement. "
            "Vendor will maintain appropriate security safeguards and require subprocessor obligations equivalent to this agreement.",
            language="text",
        )
        st.markdown("**Approval Recommendation**")
        st.write(f"**{approval_recommendation}** with human reviewer confirmation before final disposition.")

    # Persist workflow event to session-state audit log
    decision = "Escalate" if result["risk_level"] == "High" else "Review" if result["risk_level"] == "Medium" else "Approve"
    audit_event = create_audit_record(
        workflow_id=f"WF-{contract_id}",
        module="Contract Triage",
        input_category="Contract",
        risk_result=result,
        decision_status=decision,
    )
    append_audit_record(st.session_state, audit_event)

    st.success("Workflow event added to session-state audit log.")

    report_text = f"""AI Legal & Operations Workflow Studio - Simulated Contract Triage Report
Disclaimer: Simulation only. Not legal advice.

Contract ID: {contract_id}
Counterparty: {counterparty}
Contract Type: {contract_type}
Business Owner: {business_owner}
Business Criticality: {criticality}

Risk Score: {result['risk_score']}
Risk Level: {result['risk_level']}
Human Review Required: {result['human_review_required']}
Escalation Route: {result['escalation_route']}

Triggered Rules:
- """ + "\n- ".join(result["triggered_rules"] or ["None"]) + """

Missing Facts:
- """ + "\n- ".join(result["missing_facts"] or ["None"]) + """

Recommended Next Steps:
- """ + "\n- ".join(result["recommended_next_steps"]) + """
"""

    st.download_button(
        "Download Text Report",
        data=report_text.encode("utf-8"),
        file_name=f"contract_triage_{contract_id}.txt",
        mime="text/plain",
    )

st.caption("Disclaimer: Simulated AI workflow prototype; not legal advice.")
