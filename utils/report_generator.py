"""Simple helpers for shared metrics and evaluation summaries."""

import pandas as pd


def summarize_evaluations(df: pd.DataFrame) -> dict:
    total = len(df)
    passed = int((df["status"] == "Pass").sum())
    failed = total - passed
    pass_rate = round((passed / total) * 100, 1) if total else 0
    return {"total": total, "passed": passed, "failed": failed, "pass_rate": pass_rate}
