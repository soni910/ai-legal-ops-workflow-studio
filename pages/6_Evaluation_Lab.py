import streamlit as st
import pandas as pd
from utils.app_common import chart_panel_header, intake_hero, kpi_card, page_header

page_header("Evaluation Lab", "Quality-Control and Policy Testing Matrix", "Employer-facing simulation of AI workflow quality controls. Not legal advice.")

intake_hero(
    "Evaluation and assurance command center",
    "Assess deterministic workflow behavior for escalation accuracy, policy boundaries, security controls, and output completeness.",
    ["Deterministic test suite", "Policy controls", "Safety checks", "Quality metrics"],
)

st.markdown(
    "This evaluation view demonstrates how a legal/operations AI workflow can be tested for policy adherence, "
    "escalation accuracy, safety behavior, and structured output reliability."
)

# Deterministic test suite for employer review
test_cases = [
    {
        "test_id": "EV-001",
        "module": "Contract Triage",
        "scenario": "Contract includes unilateral amendment rights.",
        "expected_behavior": "Flag clause as elevated risk and require review.",
        "simulated_result": "Flagged in triggered rules; routed to review.",
        "pass_fail": "Pass",
        "control_category": "Clause Risk Detection",
        "notes": "Detects asymmetric change-control terms.",
    },
    {
        "test_id": "EV-002",
        "module": "Contract Triage",
        "scenario": "Liability cap is uncapped.",
        "expected_behavior": "Escalate due to high commercial/legal exposure.",
        "simulated_result": "Escalation recommendation generated.",
        "pass_fail": "Pass",
        "control_category": "Escalation Accuracy",
        "notes": "High-severity contractual risk threshold.",
    },
    {
        "test_id": "EV-003",
        "module": "Vendor Risk",
        "scenario": "Vendor handles personal data but DPA is missing.",
        "expected_behavior": "Escalate and require DPA completion.",
        "simulated_result": "Escalation triggered; DPA listed in missing information.",
        "pass_fail": "Pass",
        "control_category": "Privacy Control",
        "notes": "Validates privacy contract guardrail.",
    },
    {
        "test_id": "EV-004",
        "module": "Vendor Risk",
        "scenario": "Vendor has no current SOC 2 evidence.",
        "expected_behavior": "Flag elevated security risk.",
        "simulated_result": "Security evidence gap flagged in triggered rules.",
        "pass_fail": "Pass",
        "control_category": "Security Assurance",
        "notes": "Tests third-party assurance check.",
    },
    {
        "test_id": "EV-005",
        "module": "Lease Operations",
        "scenario": "Legal names are missing from lease intake.",
        "expected_behavior": "Block readiness and require missing data completion.",
        "simulated_result": "Not-ready condition recorded in missing facts.",
        "pass_fail": "Pass",
        "control_category": "Intake Completeness",
        "notes": "Prevents downstream processing on incomplete identity data.",
    },
    {
        "test_id": "EV-006",
        "module": "Lease Operations",
        "scenario": "Deposit status is not confirmed.",
        "expected_behavior": "Block readiness and trigger follow-up.",
        "simulated_result": "Deposit status missing; follow-up step included.",
        "pass_fail": "Pass",
        "control_category": "Financial Readiness",
        "notes": "Ensures move-in finance prerequisites are captured.",
    },
    {
        "test_id": "EV-007",
        "module": "Vendor Risk",
        "scenario": "Vendor accesses confidential data.",
        "expected_behavior": "Show confidentiality warning and tighter review path.",
        "simulated_result": "Risk warning shown with conditional review routing.",
        "pass_fail": "Pass",
        "control_category": "Confidentiality Control",
        "notes": "Demonstrates sensitivity-aware governance.",
    },
    {
        "test_id": "EV-008",
        "module": "Governance",
        "scenario": "Prompt injection attempt in free-text input.",
        "expected_behavior": "Treat input as untrusted and block unsafe actioning.",
        "simulated_result": "Blocked in policy simulation and marked for reviewer check.",
        "pass_fail": "Pass",
        "control_category": "LLM Security",
        "notes": "Educational OWASP-style control mapping.",
    },
    {
        "test_id": "EV-009",
        "module": "Contract Triage",
        "scenario": "User requests legal advice instead of workflow triage.",
        "expected_behavior": "Route to human review and show non-legal-advice boundary.",
        "simulated_result": "Human-review route required with disclaimer.",
        "pass_fail": "Pass",
        "control_category": "Policy Boundary",
        "notes": "Protects against unauthorized advice generation.",
    },
    {
        "test_id": "EV-010",
        "module": "All Modules",
        "scenario": "Output payload missing required fields.",
        "expected_behavior": "Fail schema check and block completion.",
        "simulated_result": "Schema validator flagged missing fields and halted flow.",
        "pass_fail": "Pass",
        "control_category": "Output Quality",
        "notes": "Ensures reliable structured downstream processing.",
    },
]

df = pd.DataFrame(test_cases)

# Summary metrics
total_tests = len(df)
passed_tests = int((df["pass_fail"] == "Pass").sum())
failed_tests = total_tests - passed_tests
pass_rate = round((passed_tests / total_tests) * 100, 1) if total_tests else 0.0
categories_covered = df["control_category"].nunique()

metric_cols = st.columns(5)
with metric_cols[0]:
    kpi_card("Total tests", total_tests, "Deterministic evaluation scenarios in current suite.", "blue")
with metric_cols[1]:
    kpi_card("Passed tests", passed_tests, "Scenarios meeting expected policy and quality outcomes.", "low")
with metric_cols[2]:
    kpi_card("Failed tests", failed_tests, "Scenarios requiring control, rule, or logic remediation.", "high")
with metric_cols[3]:
    kpi_card("Pass rate", f"{pass_rate}%", "Aggregate quality signal for current simulated workflow behavior.", "blue")
with metric_cols[4]:
    kpi_card("Categories", categories_covered, "Distinct control categories covered by the test suite.", "slate")

st.subheader("Evaluation Test Matrix")
st.caption("Structured test evidence for employer review across contract, vendor, lease, governance, and cross-module controls.")
st.dataframe(df, width='stretch', hide_index=True)

left, right = st.columns(2)
with left:
    chart_panel_header("Pass / fail distribution", "Quick view of outcome balance across deterministic evaluation scenarios.")
    st.bar_chart(df["pass_fail"].value_counts())

with right:
    chart_panel_header("Control category coverage", "Breadth of governance, security, and quality controls represented in testing.")
    st.bar_chart(df["control_category"].value_counts())

st.caption("Disclaimer: Educational simulation; not legal advice, certification, or compliance attestation.")
