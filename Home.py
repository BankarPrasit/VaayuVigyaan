"""VaayuVigyaan AI — Home Page
India's Premier AI Environmental Intelligence Platform
"""

import os
import sys

import streamlit as st

# Ensure local imports work when running from Streamlit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.styles import inject_css, aqi_category, glass_metric, section_header

st.set_page_config(
    page_title="VaayuVigyaan AI — India's Air Intelligence Platform",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ─── SIDEBAR ────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
    <div style='text-align:center;padding:1rem 0 0.5rem'>
        <div style='font-size:2.5rem;margin-bottom:4px'>🌫️</div>
        <div style='font-family:Rajdhani,sans-serif;font-size:1.4rem;font-weight:700;color:#00d4ff;letter-spacing:1px'>VaayuVigyaan</div>
        <div style='font-size:0.72rem;color:#94a3b8;letter-spacing:2px;text-transform:uppercase'>AI Environmental Intelligence</div>
    </div>
    <hr style='border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(0,212,255,0.4),transparent);margin:0.8rem 0'>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style='padding:0.3rem 0'>
        <div style='color:#94a3b8;font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.5rem'>Navigation</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.page_link("Home.py", label="🏠  Home", use_container_width=True)
    st.page_link("pages/1_Dashboard.py", label="📊  Dashboard", use_container_width=True)
    st.page_link("pages/2_AI_Predictor.py", label="🤖  AI Predictor", use_container_width=True)
    st.page_link("pages/3_Health_Impact.py", label="🏥  Health Impact", use_container_width=True)
    st.page_link("pages/4_AI_Insights.py", label="💡  AI Insights", use_container_width=True)
    st.page_link("pages/5_Future_Forecast.py", label="📈  Future Forecast", use_container_width=True)
    st.page_link("pages/6_What_If_Simulator.py", label="⚗️  What-If Simulator", use_container_width=True)

    st.markdown(
        """
    <hr style='border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(0,212,255,0.3),transparent);margin:1rem 0'>
    <div style='text-align:center;font-size:0.7rem;color:#475569'>
        <span style='color:#00d4ff'>●</span> System Online<br>
        <span style='color:#64748b'>Data refreshed daily</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ─── HERO SECTION ───────────────────────────────────────────
st.markdown(
    """
<div style='
    background: linear-gradient(135deg, rgba(0,212,255,0.06) 0%, rgba(0,245,200,0.03) 50%, rgba(59,130,246,0.05) 100%);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 20px;
    padding: 3.5rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
'>
    <div style='position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#00d4ff,#00f5c8,#3b82f6)'></div>
    <div style='position:absolute;top:-60px;right:-60px;width:200px;height:200px;background:radial-gradient(circle,rgba(0,212,255,0.08),transparent);border-radius:50%'></div>
    <div style='position:absolute;bottom:-40px;left:-40px;width:150px;height:150px;background:radial-gradient(circle,rgba(0,245,200,0.06),transparent);border-radius:50%'></div>

    <div style='display:flex;align-items:center;gap:12px;margin-bottom:0.8rem'>
        <span style='font-size:0.75rem;background:rgba(0,212,255,0.15);color:#00d4ff;border:1px solid rgba(0,212,255,0.3);border-radius:20px;padding:3px 14px;letter-spacing:2px;text-transform:uppercase;font-family:Rajdhani,sans-serif'>INDIA ● AI-POWERED ● REAL-TIME</span>
    </div>

    <h1 style='font-family:Rajdhani,sans-serif;font-size:3.2rem;font-weight:800;line-height:1.1;margin:0.5rem 0;background:linear-gradient(90deg,#e2e8f0,#00d4ff,#00f5c8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text'>
        VaayuVigyaan AI
    </h1>
    <h2 style='font-family:Rajdhani,sans-serif;font-size:1.5rem;font-weight:500;color:#94a3b8;margin:0;letter-spacing:0.5px'>
        India's Environmental Intelligence Platform
    </h2>
    <p style='color:#64748b;margin:1rem 0 1.5rem;max-width:600px;line-height:1.7;font-size:0.95rem'>
        Advanced AI-driven air quality prediction, health risk assessment, and environmental forecasting 
        powered by satellite data, ground sensors, and machine learning.
    </p>

    <div style='display:flex;gap:12px;flex-wrap:wrap'>
        <div style='background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.3);border-radius:8px;padding:6px 16px;font-size:0.82rem;color:#00d4ff;font-family:Rajdhani,sans-serif;font-weight:600'>
            🤖 XGBoost AI Model
        </div>
        <div style='background:rgba(0,245,200,0.08);border:1px solid rgba(0,245,200,0.25);border-radius:8px;padding:6px 16px;font-size:0.82rem;color:#00f5c8;font-family:Rajdhani,sans-serif;font-weight:600'>
            📡 CPCB Data Integration
        </div>
        <div style='background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.25);border-radius:8px;padding:6px 16px;font-size:0.82rem;color:#3b82f6;font-family:Rajdhani,sans-serif;font-weight:600'>
            🛰️ MERRA-2 Satellite AOD
        </div>
        <div style='background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);border-radius:8px;padding:6px 16px;font-size:0.82rem;color:#10b981;font-family:Rajdhani,sans-serif;font-weight:600'>
            🏥 Health Intelligence
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ─── LIVE AQI TICKER ───────────────────────────────────────
from utils.data_generator import get_current_city_data

city_data = get_current_city_data()

alerts = []
for city, d in city_data.items():
    cat, color, icon = aqi_category(d["pm25"])
    alerts.append(f"{icon} <b>{city}</b>: PM2.5 {d['pm25']} µg/m³ ({cat})")

ticker_text = "  &nbsp;&nbsp;|&nbsp;&nbsp;  ".join(alerts)

st.markdown(
    f"""
<div class="alert-ticker">
    <span class="alert-ticker-inner">🌍 LIVE AQI MONITOR &nbsp;&nbsp;|&nbsp;&nbsp; {ticker_text} &nbsp;&nbsp;|&nbsp;&nbsp; 🌍 LIVE AQI MONITOR &nbsp;&nbsp;|&nbsp;&nbsp; {ticker_text}</span>
</div>
""",
    unsafe_allow_html=True,
)

# ─── KEY METRICS ───────────────────────────────────────────
st.markdown(
    section_header("India Air Quality Overview", "LIVE DATA", "📊"),
    unsafe_allow_html=True,
)

import numpy as np

pm25_values = [d["pm25"] for d in city_data.values()]
avg_pm25 = np.mean(pm25_values)
max_city = max(city_data, key=lambda c: city_data[c]["pm25"])
min_city = min(city_data, key=lambda c: city_data[c]["pm25"])
dangerous_count = sum(1 for v in pm25_values if v > 100)

cols = st.columns(4)
metrics = [
    ("Avg National PM2.5", f"{avg_pm25:.0f}", "µg/m³ today", "🌫️"),
    ("Most Polluted", max_city, f"PM2.5: {city_data[max_city]['pm25']:.0f}", "🔴"),
    ("Cleanest City", min_city, f"PM2.5: {city_data[min_city]['pm25']:.0f}", "🟢"),
    ("Cities > 100 PM2.5", str(dangerous_count), f"of {len(city_data)} monitored", "⚠️"),
]

for col, (label, value, sub, icon) in zip(cols, metrics):
    col.markdown(glass_metric(label, value, sub, icon), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── CITY AQI CARDS ─────────────────────────────────────────
st.markdown(
    section_header("City-wise Air Quality Status", "12 CITIES", "🏙️"),
    unsafe_allow_html=True,
)

cities_list = list(city_data.items())
for row_start in range(0, len(cities_list), 4):
    cols = st.columns(4)
    for col, (city, data) in zip(cols, cities_list[row_start : row_start + 4]):
        cat, color, icon = aqi_category(data["pm25"])

        if data["pm25"] > 120:
            risk, risk_color = "High Risk", "#ef4444"
        elif data["pm25"] > 60:
            risk, risk_color = "Moderate", "#f59e0b"
        else:
            risk, risk_color = "Low Risk", "#10b981"

        col.markdown(
            f"""
<div class="glass-card" style='padding:1rem;text-align:center'>
    <div style='font-size:1.4rem'>{icon}</div>
    <div style='font-family:Rajdhani,sans-serif;font-size:1.05rem;font-weight:600;color:#e2e8f0;margin:4px 0'>{city}</div>
    <div style='font-size:2rem;font-weight:700;color:{color};font-family:Rajdhani,sans-serif;text-shadow:0 0 15px {color}55'>{data['pm25']:.0f}</div>
    <div style='font-size:0.7rem;color:#64748b;margin-bottom:6px'>µg/m³ PM2.5</div>
    <div style='display:inline-block;padding:2px 10px;border-radius:20px;border:1px solid {color}44;background:{color}15;color:{color};font-size:0.75rem;font-weight:600'>{cat}</div>
</div>
""",
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ─── FEATURES SHOWCASE ─────────────────────────────────────
st.markdown(
    section_header("Platform Capabilities", "AI-POWERED", "⚡"),
    unsafe_allow_html=True,
)

features = [
    (
        "🤖",
        "AI PM2.5 Predictor",
        "XGBoost model with 92.6% accuracy. Input weather, traffic, and satellite data for instant predictions with confidence scores.",
    ),
    (
        "🗺️",
        "Interactive Pollution Map",
        "Real-time geographic visualization of PM2.5 across India with heatmaps, city markers, and trend overlays.",
    ),
    (
        "🏥",
        "Health Impact Engine",
        "Personalized risk assessment for asthma patients, children, elderly, and outdoor workers with mask recommendations.",
    ),
    (
        "💡",
        "AI Insight Generator",
        "Explainable AI analysis identifying root causes: wind stagnation, humidity trapping, traffic spikes, and seasonal patterns.",
    ),
    (
        "📈",
        "72-Hour Forecast",
        "Machine learning forecast curves with confidence intervals for 6h, 24h, and 3-day pollution outlooks.",
    ),
    (
        "⚗️",
        "What-If Simulator",
        "Model the impact of traffic reduction, industrial controls, reforestation, and rainfall on air quality.",
    ),
]

for i in range(0, len(features), 3):
    cols = st.columns(3)
    for col, (icon, title, desc) in zip(cols, features[i : i + 3]):
        col.markdown(
            f"""
<div class="glass-card" style='height:100%'>
    <div style='font-size:2rem;margin-bottom:0.6rem'>{icon}</div>
    <div style='font-family:Rajdhani,sans-serif;font-size:1.1rem;font-weight:600;color:#00d4ff;margin-bottom:0.5rem'>{title}</div>
    <div style='font-size:0.85rem;color:#64748b;line-height:1.6'>{desc}</div>
</div>
""",
            unsafe_allow_html=True,
        )
    st.markdown("<br>", unsafe_allow_html=True)

# ─── FOOTER ────────────────────────────────────────────────
st.markdown(
    """
<hr style='border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(0,212,255,0.3),transparent);margin:2rem 0 1rem'>
<div style='text-align:center;color:#374151;font-size:0.8rem;padding-bottom:1rem'>
    <span style='color:#00d4ff;font-family:Rajdhani,sans-serif;font-size:0.9rem;font-weight:600'>VaayuVigyaan AI</span>
    &nbsp;·&nbsp; India Environmental Intelligence Platform
    &nbsp;·&nbsp; Built with XGBoost + CPCB + MERRA-2 Data
    &nbsp;·&nbsp; <span style='color:#10b981'>● System Online</span>
</div>
""",
    unsafe_allow_html=True,
)

