import streamlit as st
from utils.risk_engine import score_vendor_dict
from utils.app_common import page_header, risk_badge
from utils.audit import init_session_audit_log, create_audit_record, append_audit_record

page_header("Vendor Risk Intake", "Third-Party Risk Assessment and Approval Controls", "Simulated vendor risk intake workflow. Simulated AI workflow prototype; not legal advice.")

init_session_audit_log(st.session_state)

with st.form("vendor_risk_form"):
    st.subheader("Vendor Intake Form")
    c1, c2 = st.columns(2)

    with c1:
        vendor_id = st.text_input("Vendor ID", value="VND-DEMO-001")
        vendor_name = st.text_input("Vendor Name", value="Fictional Data Services LLC")
        vendor_type = st.selectbox("Vendor Type", ["SaaS", "Consulting", "Infrastructure", "BPO", "Other"])
        service_description = st.text_area("Service Description", value="Provides workflow automation and analytics support.")
        business_owner = st.text_input("Business Owner", value="Procurement Lead")

    with c2:
        handles_personal_data = st.checkbox("Handles personal data (PII/PHI)", value=True)
        handles_confidential_data = st.checkbox("Handles confidential/business-critical data", value=True)
        soc2_status = st.selectbox("SOC 2 Status", ["Current", "Expired", "Pending", "None"], index=1)
        dpa_status = st.selectbox("DPA Status", ["In Place", "Missing", "In Review"], index=1)
        insurance_status = st.selectbox("Insurance Status", ["Current", "Expired", "Missing"], index=0)

    c3, c4 = st.columns(2)
    with c3:
        retention_clarity = st.selectbox("Data retention/deletion clarity", ["Clear", "Partial", "Unknown"], index=2)
        subcontractor_access = st.selectbox("Subcontractor access", ["None", "Limited", "Broad", "Unknown"], index=2)

    with c4:
        missing_docs = st.multiselect(
            "Missing documents",
            ["DPA", "SOC2 report", "Security questionnaire", "Insurance certificate", "Data retention policy"],
            default=["DPA", "SOC2 report"],
        )

    submitted = st.form_submit_button("Run Vendor Risk Assessment")

if submitted:
    data_access = "None"
    if handles_personal_data:
        data_access = "PII"
    elif handles_confidential_data:
        data_access = "Confidential"
    elif not handles_personal_data and not handles_confidential_data:
        data_access = "Unknown" if subcontractor_access == "Unknown" else "Internal"

    payload = {
        "vendor_id": vendor_id,
        "vendor_name": vendor_name,
        "vendor_type": vendor_type,
        "service_description": service_description,
        "data_access": data_access,
        "soc2_status": soc2_status if soc2_status != "None" else "Missing",
        "dpa_in_place": "Yes" if dpa_status == "In Place" else "No",
        "insurance_status": insurance_status,
        "business_owner": business_owner,
        "retention_clarity": retention_clarity,
        "subcontractor_access": subcontractor_access,
        "missing_docs": ";".join(missing_docs) if missing_docs else "None",
    }

    result = score_vendor_dict(payload)

    st.subheader("Risk Outcome")
    m1, m2, m3 = st.columns(3)
    m1.metric("Risk Score", result["risk_score"])
    m2.metric("Risk Level", risk_badge(result["risk_level"]))
    m3.metric("Human Review Required", "Yes" if result["human_review_required"] else "No")

    st.write("**Escalation Route:**", result["escalation_route"])

    t1, t2, t3, t4 = st.tabs(["Triggered Rules", "Missing Information", "Recommendation", "Approval Checklist"])

    with t1:
        for rule in result["triggered_rules"] or ["No elevated rules triggered."]:
            st.write(f"- {rule}")

    with t2:
        for fact in result["missing_facts"] or ["No missing information identified."]:
            st.write(f"- {fact}")

    with t3:
        for step in result["recommended_next_steps"]:
            st.write(f"- {step}")

    with t4:
        checklist = [
            "Business owner confirmed",
            "Data classification validated",
            "DPA reviewed/approved",
            "SOC 2 evidence reviewed",
            "Insurance coverage confirmed",
            "Retention/deletion terms confirmed",
            "Subcontractor obligations validated",
        ]
        for item in checklist:
            st.checkbox(item, value=False, key=f"check_{vendor_id}_{item}")

    st.subheader("Simulated AI Output")
    decision = "Escalate" if result["risk_level"] == "High" else "Review" if result["risk_level"] == "Medium" else "Approve"
    st.markdown("**Vendor Summary**")
    st.write(f"{vendor_name} ({vendor_type}) provides: {service_description}")

    st.markdown("**Risk Analysis**")
    st.write(
        f"The intake is rated **{result['risk_level']} risk** with score **{result['risk_score']}** due to "
        f"{len(result['triggered_rules'])} triggered rule(s)."
    )

    st.markdown("**Missing Information**")
    st.write("\n".join([f"- {x}" for x in (result["missing_facts"] or ["None identified"]) ]))

    st.markdown("**Approval Conditions**")
    conditions = [
        "Complete all required security/privacy documentation.",
        "Confirm accountable business owner and review cadence.",
        "Document residual risks and sign-off path.",
    ]
    st.write("\n".join([f"- {x}" for x in conditions]))

    st.markdown("**Recommended Decision**")
    st.write(f"**{decision}** pending human validation and completion of required conditions.")

    audit_event = create_audit_record(
        workflow_id=f"WF-{vendor_id}",
        module="Vendor Risk Intake",
        input_category="Vendor",
        risk_result=result,
        decision_status=decision,
    )
    append_audit_record(st.session_state, audit_event)
    st.success("Vendor assessment added to session-state audit log.")

    report_text = f"""AI Legal & Operations Workflow Studio - Simulated Vendor Risk Report
Disclaimer: Simulation only. Not legal advice.

Vendor ID: {vendor_id}
Vendor Name: {vendor_name}
Vendor Type: {vendor_type}
Business Owner: {business_owner}

Risk Score: {result['risk_score']}
Risk Level: {result['risk_level']}
Human Review Required: {result['human_review_required']}
Escalation Route: {result['escalation_route']}
Recommended Decision: {decision}

Triggered Rules:
- """ + "\n- ".join(result["triggered_rules"] or ["None"]) + """

Missing Information:
- """ + "\n- ".join(result["missing_facts"] or ["None"]) + """

Recommended Next Steps:
- """ + "\n- ".join(result["recommended_next_steps"]) + """
"""

    st.download_button(
        "Download Vendor Risk Report",
        data=report_text.encode("utf-8"),
        file_name=f"vendor_risk_{vendor_id}.txt",
        mime="text/plain",
    )

st.caption("Disclaimer: Simulated AI workflow prototype; not legal advice.")

