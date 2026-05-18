"""Shared app utilities for robust loading, formatting, and UI consistency."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent


def safe_read_csv(relative_path: str, required_columns: Iterable[str] | None = None) -> pd.DataFrame:
    path = ROOT / relative_path
    if not path.exists():
        st.error(f"Required data file is missing: {relative_path}")
        st.stop()
    try:
        df = pd.read_csv(path)
    except Exception as exc:
        st.error(f"Unable to read {relative_path}: {exc}")
        st.stop()

    if required_columns:
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            st.error(f"{relative_path} is missing expected columns: {', '.join(missing)}")
            st.stop()
    return df


def page_header(title: str, subtitle: str, caption: str) -> None:
    st.title(title)
    st.markdown(f"### {subtitle}")
    st.divider()
    st.caption(caption)


def risk_badge(level: str) -> str:
    lvl = (level or "").strip().lower()
    if lvl == "high":
        return "🔴 High"
    if lvl == "medium":
        return "🟠 Medium"
    return "🟢 Low"
