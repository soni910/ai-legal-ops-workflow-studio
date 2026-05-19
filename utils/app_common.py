"""Shared app utilities for robust loading, formatting, and UI consistency."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent


def apply_global_style() -> None:
    """Apply a restrained professional visual system across Streamlit pages."""
    st.markdown(
        """
        <style>
        :root {
            --studio-navy: #172033;
            --studio-blue: #1f4e79;
            --studio-slate: #526071;
            --studio-border: #d9e2ec;
            --studio-soft: #f6f8fb;
            --studio-card: #ffffff;
        }

        .stApp {
            background: linear-gradient(180deg, #f8fafc 0%, #eef3f8 100%);
            color: var(--studio-navy);
        }

        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }

        h1 {
            color: var(--studio-navy);
            font-weight: 760;
            letter-spacing: -0.035em;
            margin-bottom: 0.25rem;
        }

        h2, h3 {
            color: var(--studio-navy);
            letter-spacing: -0.015em;
        }

        p, li, .stCaption, label {
            color: #344054;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--studio-border);
        }

        [data-testid="stMetric"] {
            background: var(--studio-card);
            border: 1px solid var(--studio-border);
            border-radius: 16px;
            padding: 1rem 1rem 0.85rem 1rem;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.045);
        }

        [data-testid="stMetricLabel"] p {
            color: var(--studio-slate);
            font-weight: 650;
        }

        [data-testid="stMetricValue"] {
            color: var(--studio-navy);
            font-weight: 760;
        }

        div[data-testid="stDataFrame"], div[data-testid="stTable"] {
            border: 1px solid var(--studio-border);
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
        }

        .stButton > button, .stDownloadButton > button, button[kind="primary"] {
            border-radius: 999px;
            border: 1px solid #1f4e79;
            background: #1f4e79;
            color: #ffffff;
            font-weight: 650;
            padding: 0.55rem 1.1rem;
        }

        .stButton > button:hover, .stDownloadButton > button:hover {
            border-color: #173a5c;
            background: #173a5c;
            color: #ffffff;
        }

        div[data-testid="stForm"] {
            background: #ffffff;
            border: 1px solid var(--studio-border);
            border-radius: 18px;
            padding: 1rem 1.15rem 1.2rem 1.15rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.045);
        }

        .studio-hero {
            background: linear-gradient(135deg, #172033 0%, #1f4e79 58%, #3a6f95 100%);
            color: #ffffff;
            padding: 2rem;
            border-radius: 22px;
            box-shadow: 0 18px 45px rgba(23, 32, 51, 0.18);
            margin-bottom: 1.25rem;
        }

        .studio-hero h1, .studio-hero h2, .studio-hero h3, .studio-hero p {
            color: #ffffff !important;
        }

        .studio-eyebrow {
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.78rem;
            font-weight: 760;
            color: #d8e7f5 !important;
            margin-bottom: 0.5rem;
        }

        .studio-card {
            background: #ffffff;
            border: 1px solid var(--studio-border);
            border-radius: 18px;
            padding: 1.05rem 1.1rem;
            min-height: 142px;
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.055);
        }

        .studio-card h3 {
            font-size: 1.02rem;
            margin-bottom: 0.35rem;
        }

        .studio-card p {
            font-size: 0.94rem;
            margin-bottom: 0;
        }

        .studio-section-label {
            color: var(--studio-blue);
            font-size: 0.82rem;
            font-weight: 760;
            letter-spacing: 0.09em;
            text-transform: uppercase;
            margin-top: 0.7rem;
            margin-bottom: 0.25rem;
        }


        .studio-dashboard-hero {
            background:
                radial-gradient(circle at 92% 8%, rgba(255,255,255,0.24), transparent 24%),
                linear-gradient(135deg, #172033 0%, #1f4e79 54%, #315f72 100%);
            color: #ffffff;
            border-radius: 24px;
            padding: 1.8rem 2rem;
            margin-bottom: 1.35rem;
            box-shadow: 0 20px 45px rgba(23, 32, 51, 0.20);
        }

        .studio-dashboard-hero p, .studio-dashboard-hero h2, .studio-dashboard-hero div {
            color: #ffffff !important;
        }

        .studio-dashboard-title {
            font-size: 1.95rem;
            line-height: 1.15;
            font-weight: 780;
            letter-spacing: -0.035em;
            margin: 0.25rem 0 0.55rem 0;
        }

        .studio-dashboard-copy {
            max-width: 760px;
            font-size: 1rem;
            line-height: 1.55;
            color: #e6eef7 !important;
            margin-bottom: 0;
        }

        .studio-pill-row {
            display: flex;
            gap: 0.45rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }

        .studio-pill {
            border: 1px solid rgba(255,255,255,0.28);
            background: rgba(255,255,255,0.12);
            color: #ffffff;
            border-radius: 999px;
            padding: 0.28rem 0.7rem;
            font-size: 0.78rem;
            font-weight: 680;
        }

        .studio-kpi-card {
            background: #ffffff;
            border: 1px solid var(--studio-border);
            border-radius: 18px;
            padding: 1rem 1rem 0.95rem 1rem;
            min-height: 132px;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.055);
        }

        .studio-kpi-label {
            color: var(--studio-slate);
            font-size: 0.78rem;
            font-weight: 760;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .studio-kpi-value {
            color: var(--studio-navy);
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.045em;
            margin-top: 0.25rem;
        }

        .studio-kpi-caption {
            color: #667085;
            font-size: 0.84rem;
            line-height: 1.35;
            margin-top: 0.35rem;
        }

        .studio-kpi-card.tone-high { border-top: 4px solid #b42318; }
        .studio-kpi-card.tone-medium { border-top: 4px solid #b54708; }
        .studio-kpi-card.tone-low { border-top: 4px solid #027a48; }
        .studio-kpi-card.tone-blue { border-top: 4px solid #1f4e79; }
        .studio-kpi-card.tone-slate { border-top: 4px solid #526071; }

        .studio-insight-card {
            background: #ffffff;
            border: 1px solid var(--studio-border);
            border-radius: 18px;
            padding: 1rem 1.05rem;
            min-height: 118px;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.045);
        }

        .studio-insight-card strong {
            color: var(--studio-navy);
        }

        .studio-insight-card p {
            color: #475467;
            font-size: 0.92rem;
            line-height: 1.45;
            margin-bottom: 0;
        }

        .studio-chart-panel {
            background: #ffffff;
            border: 1px solid var(--studio-border);
            border-radius: 18px;
            padding: 1rem 1.1rem 1.2rem 1.1rem;
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.045);
        }

        .studio-chart-title {
            color: var(--studio-navy);
            font-weight: 760;
            font-size: 1rem;
            margin-bottom: 0.2rem;
        }

        .studio-chart-caption {
            color: #667085;
            font-size: 0.84rem;
            margin-bottom: 0.8rem;
        }


        .studio-intake-hero {
            background:
                radial-gradient(circle at 88% 10%, rgba(255,255,255,0.22), transparent 22%),
                linear-gradient(135deg, #13233a 0%, #1f4e79 58%, #35617e 100%);
            color: #ffffff;
            border-radius: 22px;
            padding: 1.45rem 1.65rem;
            box-shadow: 0 16px 40px rgba(19, 35, 58, 0.18);
            margin-bottom: 1rem;
        }

        .studio-intake-hero p, .studio-intake-hero h3, .studio-intake-hero div {
            color: #ffffff !important;
        }

        .studio-intake-title {
            font-size: 1.45rem;
            font-weight: 780;
            letter-spacing: -0.03em;
            margin-bottom: 0.35rem;
        }

        .studio-intake-copy {
            font-size: 0.95rem;
            color: #e3edf8 !important;
            line-height: 1.5;
            margin-bottom: 0;
        }

        .studio-pill-row-dark {
            display: flex;
            gap: 0.45rem;
            flex-wrap: wrap;
            margin-top: 0.9rem;
        }

        .studio-pill-dark {
            border: 1px solid rgba(255,255,255,0.30);
            background: rgba(255,255,255,0.11);
            color: #ffffff;
            border-radius: 999px;
            padding: 0.24rem 0.68rem;
            font-size: 0.76rem;
            font-weight: 670;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_context() -> None:
    """Add consistent sidebar context below Streamlit's native page navigation."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("**AI Legal & Operations Workflow Studio**")
    st.sidebar.caption(
        "Simulated AI workflow prototype for structured intake, rule-based risk scoring, human review, evaluation, and auditability."
    )
    st.sidebar.markdown("**Deployment posture**")
    st.sidebar.caption("No paid APIs • No secrets • Static sample data • Not legal advice")


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
    apply_global_style()
    render_sidebar_context()
    st.markdown(f"<div class='studio-section-label'>{subtitle}</div>", unsafe_allow_html=True)
    st.title(title)
    st.caption(caption)
    st.divider()


def hero_panel(eyebrow: str, title: str, body: str) -> None:
    apply_global_style()
    st.markdown(
        f"""
        <div class="studio-hero">
            <div class="studio-eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="studio-card">
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def intake_hero(title: str, body: str, pills: Iterable[str]) -> None:
    pill_html = "".join(f"<span class='studio-pill-dark'>{escape(str(pill))}</span>" for pill in pills)
    st.markdown(
        f"""
        <div class="studio-intake-hero">
            <div class="studio-eyebrow">Structured intake workflow</div>
            <div class="studio-intake-title">{escape(title)}</div>
            <p class="studio-intake-copy">{escape(body)}</p>
            <div class="studio-pill-row-dark">{pill_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dashboard_hero(title: str, body: str, pills: Iterable[str]) -> None:
    pill_html = "".join(f"<span class='studio-pill'>{escape(str(pill))}</span>" for pill in pills)
    st.markdown(
        f"""
        <div class="studio-dashboard-hero">
            <div class="studio-eyebrow">Executive AI operations dashboard</div>
            <div class="studio-dashboard-title">{escape(title)}</div>
            <p class="studio-dashboard-copy">{escape(body)}</p>
            <div class="studio-pill-row">{pill_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str | int, caption: str, tone: str = "blue") -> None:
    safe_tone = tone if tone in {"high", "medium", "low", "blue", "slate"} else "blue"
    st.markdown(
        f"""
        <div class="studio-kpi-card tone-{safe_tone}">
            <div class="studio-kpi-label">{escape(str(label))}</div>
            <div class="studio-kpi-value">{escape(str(value))}</div>
            <div class="studio-kpi-caption">{escape(str(caption))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="studio-insight-card">
            <p><strong>{escape(str(title))}</strong><br>{escape(str(body))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_panel_header(title: str, caption: str) -> None:
    st.markdown(
        f"""
        <div class="studio-chart-title">{escape(str(title))}</div>
        <div class="studio-chart-caption">{escape(str(caption))}</div>
        """,
        unsafe_allow_html=True,
    )


def risk_badge(level: str) -> str:
    lvl = (level or "").strip().lower()
    if lvl == "high":
        return "🔴 High"
    if lvl == "medium":
        return "🟠 Medium"
    return "🟢 Low"
