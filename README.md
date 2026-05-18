# AI Legal & Operations Workflow Studio

## Overview
AI Legal & Operations Workflow Studio is an employer-facing Streamlit portfolio project that demonstrates how an organization could design, govern, and evaluate AI-assisted workflows across legal and operations functions.

The project emphasizes implementation judgment: structured intake, rule-based risk scoring, human-review controls, audit-ready workflow records, and a clear production upgrade path.

> **Disclaimer:** This repository is a **simulated AI workflow prototype** and does **not** provide legal advice or formal compliance determinations.

---

## Live Demo
- **Live app:** _[Add Streamlit Community Cloud link here]_

## Screenshots
- _[Add Executive Dashboard screenshot]_
- _[Add Contract Triage screenshot]_
- _[Add Vendor Risk Intake screenshot]_
- _[Add Lease Operations screenshot]_
- _[Add Governance / Evaluation / Audit screenshots]_

---

## What a Hiring Manager Can Evaluate Quickly
- Whether workflow design is clear and operationally realistic.
- Whether risk logic is explicit, inspectable, and deterministic.
- Whether human-review and escalation controls are embedded.
- Whether evaluation and auditability are treated as first-class concerns.
- Whether the roadmap from simulation to production is credible.

---

## Modules
1. **Executive Dashboard**  
   Portfolio-level view of review volume, risk distribution, escalation load, missing-document pressure, and governance maturity indicators.

2. **Contract Triage**  
   Structured intake for contract risk factors, deterministic rule-based scoring, escalation routing, and downloadable decision reports.

3. **Vendor Risk Intake**  
   Third-party risk workflow for privacy/security signals, documentation gaps, approval checklisting, and human-review pathways.

4. **Lease Operations**  
   Real-estate intake readiness checks for legal/operational completeness with escalation triggers and follow-up outputs.

5. **Governance Controls**  
   Educational governance mapping (NIST AI RMF-style, ISO/IEC 42001-inspired, OWASP LLM-style controls) without overclaiming certification.

6. **Evaluation Lab**  
   Deterministic quality-control matrix with pass/fail scenarios for policy adherence, escalation accuracy, safety boundaries, and schema completeness.

7. **Audit Log**  
   Structured audit-ready workflow record with risk rationale, human-review requirements, version metadata, and CSV/JSON exports.

8. **Case Study & Roadmap**  
   Employer-facing narrative, architecture summary, and staged path from simulation to controlled pilot to production system.

---

## Skills Demonstrated
- AI operations workflow design for legal and business processes
- Legal operations and vendor-risk control thinking
- Rule-based risk scoring and escalation policy translation
- Human-in-the-loop review design and decision governance
- Evaluation and quality-control planning
- Auditability, reporting, and stakeholder communication
- Product framing for startup operations and process automation contexts

---

## Technical Architecture
**Frontend/UI**
- Streamlit multipage application (`app.py` + `pages/`)

**Workflow Logic**
- Deterministic rule engine (`utils/risk_engine.py`)
- Structured audit helpers (`utils/audit.py`)
- Mock output and reporting helpers (`utils/mock_ai_outputs.py`, `utils/report_generator.py`)

**Data Layer (Static)**
- Sample CSV datasets (`data/`)
- YAML risk rules (`data/risk_rules.yaml`)

**Operational Controls**
- Human-review gates
- Evaluation matrix
- Exportable audit records

---

## Why Outputs Are Simulated
This project intentionally uses simulated outputs to keep the portfolio:
- reproducible,
- safe for public review,
- deployable without secrets,
- independent of paid APIs,
- and free of confidential production data.

It demonstrates workflow and governance design quality rather than external model performance.

---

## Governance and Risk Controls
The app includes governance concepts such as:
- structured intake and minimum required facts,
- risk thresholds and escalation routes,
- human-review-required decisions,
- confidentiality-aware workflow patterns,
- prompt/version and audit-field expectations,
- educational control mappings for governance/security frameworks.

---

## Evaluation Lab
The Evaluation Lab demonstrates quality-control thinking with deterministic test scenarios covering:
- clause risk detection,
- escalation accuracy,
- privacy/security control checks,
- intake completeness,
- policy boundary handling,
- and output-structure reliability.

---

## Audit Logging
Each completed workflow can generate an audit-ready workflow record with fields such as:
- workflow ID and timestamp,
- module and input category,
- risk score/level,
- triggered rules and missing facts,
- human-review requirement,
- escalation route,
- recommended next steps,
- prompt/schema version,
- decision status.

Exports are available in CSV and JSON for reviewer-friendly traceability.

---

## Production Upgrade Path
### Stage 1: Simulated Prototype (Current)
- Deterministic rule-based scoring
- Static datasets
- Session-state audit logging
- Manual evaluation table

### Stage 2: Controlled Live-LLM Pilot
- Guarded LLM integration for selected workflows
- Approved document set and tighter reviewer queue
- Prompt version controls + expanded safety checks
- Controlled scope, measured outcomes

### Stage 3: Production Workflow System
- Role-based permissions (RBAC/SSO)
- Persistent database-backed audit log
- Approved enterprise document repository
- Automated evaluation harness and monitoring
- Retrieval over approved sources with citation controls

---

## Limitations
- No live LLM/API integration in current version
- No production authentication/authorization stack
- No persistent production database in this prototype
- No real-time enterprise system integrations
- Educational governance mapping, not formal certification

---

## Suggested Resume Bullet
Designed and built a Streamlit-based AI Legal & Operations Workflow Studio that demonstrates structured intake, rule-based risk scoring, human-review controls, evaluation testing, and audit-ready workflow records across contract, vendor, and lease workflows.

## Suggested Interview Explanation
I built this project to demonstrate production-minded AI implementation judgment, not just UI development. I translated legal and operational risk requirements into deterministic workflows with governance gates, escalation logic, evaluation checks, and traceable audit records, then defined a realistic path to a controlled live-LLM pilot and full production workflow system.
Designed and built a Streamlit-based AI Legal & Operations Workflow Studio demonstrating structured intake, rule-based risk scoring, human-review controls, evaluation testing, and audit-ready workflow records across contract, vendor, and lease workflows.

## Suggested Interview Explanation
I built this project to show production-minded AI implementation judgment, not just UI development. I translated legal and operational risk requirements into deterministic workflows with governance gates, escalation logic, evaluation checks, and traceable audit records, then defined a realistic path to a controlled live-LLM pilot and full production workflow system.

---

## Local Run Instructions
```bash
git clone <repo-url>
cd ai-legal-ops-workflow-studio
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Deployment Instructions (Streamlit Community Cloud)
1. Push this repository to GitHub.
2. In Streamlit Community Cloud, create a new app.
3. Select this repository.
4. Set `app.py` as the entrypoint.
5. Deploy (no secrets required for this simulated prototype).
