"""styles.py

This project originally referenced `utils.styles` from multiple pages.
The repository currently contains `utils/theme.py` and `utils/ui_components.py`.

To keep the app runnable without restructuring, this module provides the
expected helper functions by delegating to existing utilities where possible,
or by providing lightweight fallbacks.
"""

from __future__ import annotations

import streamlit as st


def inject_css() -> None:
    """Inject global CSS for the Streamlit UI."""
    try:
        # Prefer the project's existing theme if available.
        from utils.theme import apply_global_theme

        apply_global_theme()
        return
    except Exception:
        # Fallback: minimal styling.
        st.markdown(
            """
            <style>
            body { background: #0b1220; color: #e5f0ff; }
            </style>
            """,
            unsafe_allow_html=True,
        )


def aqi_category(pm25: float):
    """Return (label, color, icon) for a given PM2.5.

    Uses a simple AQI-like categorization for UI.
    """
    pm25 = float(pm25)
    if pm25 < 30:
        return ("Good", "#10b981", "🟢")
    if pm25 < 60:
        return ("Moderate", "#39e6ff", "🟦")
    if pm25 < 90:
        return ("Unhealthy (Sensitive)", "#ffd166", "🟨")
    if pm25 < 120:
        return ("Unhealthy", "#ff4d6d", "🟥")
    return ("Very Unhealthy", "#ef4444", "🔥")


def section_header(title: str, subtitle: str = "", icon: str = "") -> str:
    """Generate a styled section header HTML."""
    icon_html = f"<span style='margin-right:10px'>{icon}</span>" if icon else ""
    subtitle_html = f"<div style='color:#8db7c7;font-weight:800;margin-top:4px'>{subtitle}</div>" if subtitle else ""

    return (
        """
        <div style='margin: 14px 0 10px 0;'>
          <div style='font-size: 1.2rem; font-weight: 1000; color: #e2f0ff; letter-spacing: .2px;'>
            %s%s
          </div>
          %s
        </div>
        """
        % (icon_html, title, subtitle_html)
    )


def glass_metric(label: str, value, sub: str = "", icon: str = "") -> str:
    """Metric card HTML."""
    icon_html = f"<span style='font-size:18px;margin-right:8px'>{icon}</span>" if icon else ""
    return (
        """
        <div style='padding:14px 16px; border-radius:18px; border:1px solid rgba(120,255,255,.18); background: rgba(0,0,0,.18);'
             >
          <div style='color:#8db7c7; font-weight:900; font-size:12px; text-transform:uppercase; letter-spacing:1px'>%s%s</div>
          <div style='color:#39e6ff; font-size:26px; font-weight:1100; margin-top:6px'>%s</div>
          %s
        </div>
        """
        % (icon_html, label, value, f"<div style='color:#d7f7ff; font-weight:800; font-size:12px; margin-top:4px'>{sub}</div>" if sub else "")
    )


def health_risk(pm25: float):
    """Return (risk_label, color) based on PM2.5."""
    pm25 = float(pm25)
    if pm25 < 60:
        return ("Low", "#10b981")
    if pm25 < 100:
        return ("Moderate", "#f59e0b")
    return ("High", "#ef4444")

