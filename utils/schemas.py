"""Shared schema-like constants for workflow modules."""

CONTRACT_FIELDS = [
    "contract_id",
    "counterparty",
    "contract_type",
    "value_usd",
    "term_months",
    "auto_renewal",
    "termination_days",
    "governing_law",
    "indemnity_scope",
    "liability_cap",
    "data_processing",
    "assignment_restricted",
    "payment_terms_days",
]

VENDOR_FIELDS = [
    "vendor_id",
    "vendor_name",
    "service_type",
    "contract_value_usd",
    "criticality",
    "data_access",
    "soc2_status",
    "privacy_exposure",
    "operational_dependency",
    "missing_docs",
]

LEASE_FIELDS = [
    "lease_id",
    "site_name",
    "region",
    "monthly_rent_usd",
    "rent_issue",
    "repair_obligation_clear",
    "insurance_proof",
    "access_constraints",
    "documentation_complete",
    "missing_fields",
]
