"""VaayuVigyaan AI — Health Impact Page
Personalized health risk assessment and safety recommendations
"""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import plotly.graph_objects as go

from utils.styles import inject_css, aqi_category, section_header
from utils.data_generator import get_current_city_data, CITY_DATA

st.set_page_config(
    page_title="Health Impact — VaayuVigyaan AI",
    page_icon="🏥",
    layout="wide",
)
inject_css()

with st.sidebar:
    st.markdown(
        """
    <div style='text-align:center;padding:1rem 0 0.5rem'>
        <div style='font-size:2rem'>🌫️</div>
        <div style='font-family:Rajdhani,sans-serif;font-size:1.3rem;font-weight:700;color:#00d4ff'>VaayuVigyaan</div>
        <div style='font-size:0.7rem;color:#94a3b8;letter-spacing:2px;text-transform:uppercase'>AI Platform</div>
    </div>
    <hr style='border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(0,212,255,0.4),transparent);margin:0.8rem 0'>
    """,
        unsafe_allow_html=True,
    )
    # Streamlit page_link: entrypoint-relative paths only.
    st.page_link("app.py", label="🏠 Home", use_container_width=True)


    st.page_link("pages/1_Dashboard.py", label="📊  Dashboard", use_container_width=True)


    st.page_link("pages/2_AI_Predictor.py", label="🤖  AI Predictor", use_container_width=True)
    st.page_link("pages/3_Health_Impact.py", label="🏥  Health Impact", use_container_width=True)
    st.page_link("pages/4_AI_Insights.py", label="💡  AI Insights", use_container_width=True)
    st.page_link("pages/5_Future_Forecast.py", label="📈  Future Forecast", use_container_width=True)
    st.page_link("pages/6_What_If_Simulator.py", label="⚗️  What-If Simulator", use_container_width=True)
    st.markdown(
        "<hr style='border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(0,212,255,0.3),transparent)'>",
        unsafe_allow_html=True,
    )
    city_sel = st.selectbox("📍 Your City", list(CITY_DATA.keys()), index=2)
    custom_pm25 = st.number_input(
        "Or enter PM2.5 value",
        min_value=0.0,

        max_value=500.0,
        value=0.0,
        help="Set to 0 to use live city data",
    )

st.markdown(
    """
<div style='margin-bottom:1.5rem'>
    <h1 style='font-family:Rajdhani,sans-serif;font-size:2.4rem;font-weight:800;margin:0;background:linear-gradient(90deg,#e2e8f0,#00d4ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text'>
        Health Impact Intelligence
    </h1>
    <p style='color:#64748b;margin:4px 0 0;font-size:0.9rem'>Personalized health risk assessment based on current air quality</p>
</div>
""",
    unsafe_allow_html=True,
)

city_data = get_current_city_data()

pm25 = custom_pm25 if custom_pm25 > 0 else city_data[city_sel]["pm25"]
cat, color, icon_cat = aqi_category(pm25)

# ─── AQI STATUS BANNER ────────────────────────────────────────
trend = "↑ Worsening" if pm25 > 100 else "→ Stable" if pm25 > 40 else "↓ Improving"

st.markdown(
    f"""
<div style='
    background: linear-gradient(135deg, {color}12, {color}06);
    border: 1px solid {color}40;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
'>
    <div style='position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,transparent,{color},{color}44,transparent)'></div>
    <div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem'>
        <div>
            <div style='font-size:0.78rem;color:#64748b;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:4px'>Current Air Quality — {city_sel}</div>
            <div style='font-family:Rajdhani,sans-serif;font-size:2.8rem;font-weight:800;color:{color};text-shadow:0 0 20px {color}55;line-height:1'>{pm25:.1f} <span style='font-size:1rem;font-weight:400'>µg/m³ PM2.5</span></div>
            <div style='font-family:Rajdhani,sans-serif;font-size:1.3rem;color:{color};margin-top:4px'>{icon_cat} {cat}</div>
        </div>
        <div style='text-align:right'>
            <div style='font-size:0.75rem;color:#64748b;margin-bottom:4px'>Trend</div>
            <div style='font-family:Rajdhani,sans-serif;font-size:1.2rem;color:#94a3b8'>{trend}</div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ─── HEALTH RISK FUNCTIONS ────────────────────────────────────

def get_population_risks(pm25_val: float):
    """Calculate health risk scores for different population groups."""

    def risk_score(base_sensitivity: float, pm25_inner: float) -> float:
        return min(100.0, (pm25_inner / 250.0) * 100.0 * base_sensitivity)

    return {
        "Children (0–12)": {
            "score": risk_score(1.4, pm25_val),
            "icon": "👶",
            "safe_limit": 25,
        },
        "Elderly (60+)": {
            "score": risk_score(1.5, pm25_val),
            "icon": "👴",
            "safe_limit": 20,
        },
        "Asthma Patients": {
            "score": risk_score(1.8, pm25_val),
            "icon": "🫁",
            "safe_limit": 15,
        },
        "Heart Patients": {
            "score": risk_score(1.6, pm25_val),
            "icon": "❤️",
            "safe_limit": 20,
        },
        "Healthy Adults": {
            "score": risk_score(1.0, pm25_val),
            "icon": "🧑",
            "safe_limit": 35,
        },
        "Athletes / Outdoor Workers": {
            "score": risk_score(1.2, pm25_val),
            "icon": "🏃",
            "safe_limit": 30,
        },
    }


def score_color(score: float) -> str:
    if score < 30:
        return "#10b981"
    if score < 60:
        return "#f59e0b"
    if score < 80:
        return "#f97316"
    return "#ef4444"


def risk_label(score: float) -> str:
    if score < 30:
        return "Low Risk"
    if score < 60:
        return "Moderate"
    if score < 80:
        return "High Risk"
    return "Severe"


# ─── POPULATION RISK CARDS ────────────────────────────────────
st.markdown(section_header("Population Health Risk Assessment", "AI ANALYSIS", "🏥"), unsafe_allow_html=True)

risks = get_population_risks(pm25)
risk_items = list(risks.items())

for row_start in range(0, len(risk_items), 3):
    cols = st.columns(3)
    for col, (group, info) in zip(cols, risk_items[row_start : row_start + 3]):
        score = float(info["score"])
        sc = score_color(score)
        rl = risk_label(score)
        col.markdown(
            f"""
        <div class='glass-card' style='height:100%'>
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:0.8rem'>
                <span style='font-size:1.5rem'>{info['icon']}</span>
                <span style='font-family:Rajdhani,sans-serif;font-size:1rem;font-weight:600;color:#e2e8f0'>{group}</span>
            </div>
            <div style='font-family:Rajdhani,sans-serif;font-size:2rem;font-weight:700;color:{sc};margin-bottom:4px'>{score:.0f}%</div>
            <div style='font-size:0.8rem;color:{sc};margin-bottom:8px;font-weight:600'>{rl}</div>
            <div style='background:rgba(255,255,255,0.05);border-radius:10px;height:6px;overflow:hidden;margin-bottom:8px'>
                <div style='width:{score}%;height:100%;background:linear-gradient(90deg,{sc}88,{sc});border-radius:10px;transition:width 1s ease'></div>
            </div>
            <div style='font-size:0.72rem;color:#4b5563'>Safe limit: {info['safe_limit']} µg/m³</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    st.markdown("<br>", unsafe_allow_html=True)

# ─── ACTIVITY RECOMMENDATIONS ─────────────────────────────────
st.markdown("<hr class='cyber-divider'>", unsafe_allow_html=True)
st.markdown(section_header("Activity Safety Recommendations", "TODAY", "🏃"), unsafe_allow_html=True)

col_act, col_mask = st.columns([3, 2])

with col_act:
    if pm25 <= 30:
        activities = [
            ("✅", "Outdoor Running", "Safe for all durations", "#10b981"),
            ("✅", "Cycling", "Excellent conditions", "#10b981"),
            ("✅", "Children Outdoor Play", "Safe all day", "#10b981"),
            ("✅", "Morning Walks", "Highly recommended", "#10b981"),
            ("✅", "Sports Events", "Proceed normally", "#10b981"),
        ]
    elif pm25 <= 60:
        activities = [
            ("✅", "Outdoor Running", "Limit to 60 min sessions", "#84cc16"),
            ("⚠️", "Cycling (Long)", "Take breaks; hydrate well", "#f59e0b"),
            ("✅", "Children Outdoor Play", "Limit to 2 hours", "#84cc16"),
            ("✅", "Morning Walks", "Suitable for most people", "#84cc16"),
            ("⚠️", "High-Intensity Exercise", "Sensitive groups should limit", "#f59e0b"),
        ]
    elif pm25 <= 90:
        activities = [
            ("⚠️", "Outdoor Running", "Wear N95; limit to 30 min", "#f59e0b"),
            ("🔴", "Cycling (Long Distance)", "Avoid — high exposure route", "#ef4444"),
            ("⚠️", "Children Outdoor Play", "Limit to 30–45 min; N95 mask", "#f59e0b"),
            ("✅", "Indoor Exercise", "Preferred over outdoor", "#10b981"),
            ("🔴", "High-Intensity Outdoor", "Reschedule; unhealthy for most", "#ef4444"),
        ]
    else:
        activities = [
            ("🔴", "Any Outdoor Exercise", "Avoid all outdoor exertion", "#ef4444"),
            ("🔴", "Children Outdoor", "Keep indoors — health risk", "#ef4444"),
            ("🔴", "Elderly Outdoor", "Strictly avoid", "#ef4444"),
            ("✅", "Indoor Yoga/Stretching", "Use HEPA-filtered room", "#10b981"),
            ("🔴", "Morning Walks", "Reschedule or stay indoors", "#ef4444"),
        ]

    for status, activity, desc, c in activities:
        st.markdown(
            f"""
        <div style='display:flex;align-items:center;gap:12px;padding:10px 14px;background:rgba({','.join(str(int(c.lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.08);border:1px solid rgba({','.join(str(int(c.lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.25);border-radius:10px;margin-bottom:6px'>
            <span style='font-size:1.1rem'>{status}</span>
            <div style='flex:1'>
                <div style='font-weight:600;color:#e2e8f0;font-size:0.9rem'>{activity}</div>
                <div style='color:#64748b;font-size:0.78rem;margin-top:2px'>{desc}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

with col_mask:
    st.markdown(section_header("Protection Guide", "MASKS", "😷"), unsafe_allow_html=True)

    if pm25 <= 30:
        mask_recs = [
            ("No Mask Needed", "Air quality is good. No protection necessary for healthy adults.", "#10b981", "😊")
        ]
    elif pm25 <= 60:
        mask_recs = [
            ("Optional Surgical Mask", "Sensitive groups may benefit from a basic surgical mask outdoors.", "#84cc16", "😷")
        ]
    elif pm25 <= 90:
        mask_recs = [
            ("N95 Recommended", "Wear N95 respirator for outdoor activities, especially for children and elderly.", "#f59e0b", "😷"),
            ("Limit Outdoor Time", "Reduce time spent outdoors, especially during peak traffic hours.", "#f59e0b", "⏱️"),
        ]
    else:
        mask_recs = [
            ("N95 Mandatory", "N95 or N99 respirator mandatory for all outdoor exposure.", "#ef4444", "🚨"),
            ("Stay Indoors", "Use air purifier with HEPA filter indoors. Keep windows closed.", "#ef4444", "🏠"),
            ("Medical Attention", "Those with respiratory conditions should consult a doctor if symptoms worsen.", "#dc2626", "🏥"),
        ]

    for title, desc, c, ico in mask_recs:
        st.markdown(
            f"""
        <div class='glass-card' style='margin-bottom:0.8rem;border-color:{c}44'>
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:6px'>
                <span style='font-size:1.3rem'>{ico}</span>
                <span style='font-family:Rajdhani,sans-serif;font-weight:600;color:{c}'>{title}</span>
            </div>
            <div style='font-size:0.82rem;color:#64748b;line-height:1.5'>{desc}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Radar chart for overall health score
    cats = ["Respiratory", "Cardiovascular", "Neurological", "Immune", "Ocular", "Sleep Quality"]
    base_scores = [
        max(10, 100 - pm25 * 0.4),
        max(10, 100 - pm25 * 0.35),
        max(10, 100 - pm25 * 0.25),
        max(10, 100 - pm25 * 0.28),
        max(10, 100 - pm25 * 0.3),
        max(10, 100 - pm25 * 0.2),
    ]

    fig_radar = go.Figure(
        go.Scatterpolar(
            r=base_scores + [base_scores[0]],
            theta=cats + [cats[0]],
            fill="toself",
            fillcolor="rgba(0,212,255,0.1)",
            line=dict(color="#00d4ff", width=2),
            marker=dict(size=6, color="#00d4ff"),
        )
    )
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color="#4b5563",
                gridcolor="rgba(0,212,255,0.1)",
            ),
            angularaxis=dict(color="#94a3b8"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20),
        height=280,
        title=dict(
            text="Body System Health Scores",
            font=dict(color="#94a3b8", size=12),
            x=0.5,
        ),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ─── AI HEALTH ADVISORY ───────────────────────────────────────
st.markdown("<hr class='cyber-divider'>", unsafe_allow_html=True)
st.markdown(section_header("AI Health Advisory", "PERSONALIZED", "💊"), unsafe_allow_html=True)

advisory_class = "danger" if pm25 > 100 else "warning" if pm25 > 60 else "good"

if pm25 > 120:
    advisory_lines = [
        "🚨 <b>HAZARDOUS CONDITIONS</b>: Avoid all non-essential outdoor activities.",
        "💊 Pre-medicate with inhalers if you have asthma before any short outdoor exposure.",
        "🏠 Keep all windows and doors closed; run HEPA air purifiers on maximum.",
        "💧 Stay well-hydrated; drink 3+ litres of water to help flush particulates.",
        "🏥 Seek immediate medical attention if you experience chest pain, shortness of breath, or dizziness.",
        "📱 Alert vulnerable family members and neighbors — especially elderly and young children.",
    ]
elif pm25 > 60:
    advisory_lines = [
        "⚠️ <b>ELEVATED RISK</b>: Limit outdoor exposure to under 30 minutes.",
        "😷 Wear N95 or better mask for any outdoor activity.",
        "🚗 Use car AC on recirculation mode when commuting.",
        "🌿 Keep indoor plants like peace lilies to help improve indoor air.",
        "🏃 Postpone outdoor workouts to early morning or evening when traffic is lower.",
    ]
else:
    advisory_lines = [
        "✅ <b>AIR QUALITY IS ACCEPTABLE</b>: Most activities can proceed normally.",
        "🌬️ Good ventilation is possible — open windows in the morning.",
        "🏃 Ideal conditions for outdoor exercise and recreational activities.",
        "🧒 Children can safely play outdoors for extended periods.",
        "🌱 Great day to support green cover: water plants, trees, gardens.",
    ]

for line in advisory_lines:
    st.markdown(
        f"""
    <div class='insight-card {advisory_class}'>
        <div style='font-size:0.9rem;color:#e2e8f0;line-height:1.5'>{line}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

