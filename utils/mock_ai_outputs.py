"""Deterministic mock AI outputs for simulated workflow modules."""


def mock_contract_extraction(contract: dict) -> dict:
    return {
        "Parties": f"{contract['counterparty']} and Your Company",
        "Contract Type": contract["contract_type"],
        "Term": f"{contract['term_months']} months",
        "Auto-Renewal": contract["auto_renewal"],
        "Termination Notice": f"{contract['termination_days']} days",
        "Governing Law": contract["governing_law"],
        "Indemnity": contract["indemnity_scope"],
        "Liability Cap": contract["liability_cap"],
        "Data Processing": contract["data_processing"],
        "Payment Terms": f"Net {contract['payment_terms_days']}"
    }


def mock_explanation(workflow: str, action: str, score: int) -> str:
    return (
        f"Simulated AI assessment for {workflow}: risk score {score} leads to '{action}' based on configured "
        "rules, missing-information checks, and escalation thresholds. Human reviewer validation is required."
    )
