"""Pre-deployment sanity checks for Streamlit Community Cloud.

Run from the repository root:
    python scripts/predeploy_check.py
"""

from __future__ import annotations

import compileall
from pathlib import Path
import sys

REQUIRED_FILES = [
    "app.py",
    "requirements.txt",
    "runtime.txt",
    "pages/1_Executive_Dashboard.py",
    "pages/2_Contract_Triage.py",
    "pages/3_Vendor_Risk_Intake.py",
    "pages/4_Lease_Operations.py",
    "pages/5_Governance_Controls.py",
    "pages/6_Evaluation_Lab.py",
    "pages/7_Audit_Log.py",
    "pages/8_Case_Study_and_Roadmap.py",
    "data/sample_contracts.csv",
    "data/sample_vendors.csv",
    "data/sample_lease_intakes.csv",
    "data/evaluation_tests.csv",
    "data/risk_rules.yaml",
]

CONFLICT_MARKERS = ("<" * 7, "=" * 7, ">" * 7)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not Path(path).exists()]
    if missing:
        fail(f"Missing required files: {missing}")


def check_conflict_markers() -> None:
    search_roots = [Path("app.py"), Path("pages"), Path("utils"), Path("README.md")]
    for root in search_roots:
        paths = [root] if root.is_file() else root.rglob("*.py")
        for path in paths:
            text = path.read_text(encoding="utf-8")
            if any(marker in text for marker in CONFLICT_MARKERS):
                fail(f"Merge conflict marker found in {path}")


def check_python_compiles() -> None:
    if not compileall.compile_file("app.py", quiet=1):
        fail("app.py did not compile")
    for folder in ("pages", "utils"):
        if not compileall.compile_dir(folder, quiet=1):
            fail(f"{folder}/ did not compile")


def main() -> None:
    check_required_files()
    check_conflict_markers()
    check_python_compiles()
    print("Pre-deployment checks passed.")


if __name__ == "__main__":
    main()
