import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from utils.theme import apply_global_theme
from utils.ui_components import glass_container
from utils.modeling import load_or_train_xgb_model, predict_pm25_xgb

apply_global_theme()

st.markdown("<h2 style='margin:0;'>🧪 What-If Pollution Reduction Simulator</h2>", unsafe_allow_html=True)

model_pack = load_or_train_xgb_model()

with glass_container("Scenario Controls"):
    traffic_reduction = st.slider("Traffic Reduction (%)", 0, 60, 20)
    industrial_reduction = st.slider("Industrial Reduction (%)", 0, 60, 15)
    rainfall_increase = st.slider("Rainfall Increase (%)", 0, 80, 20)
    green_cover_increase = st.slider("Green Cover Increase (%)", 0, 80, 25)

# Baseline conditions (demo)
base = {
    "temperature": 30.0,
    "humidity": 64.0,
    "wind_speed": 2.6,
    "rainfall": 8.0,
    "aod": 0.34,
    "traffic": 68.0,
    "industrial": 52.0,
}

# Adjust features
adj = base.copy()
adj["traffic"] = base["traffic"] * (1 - traffic_reduction/100)
adj["industrial"] = base["industrial"] * (1 - industrial_reduction/100)
adj["rainfall"] = base["rainfall"] * (1 + rainfall_increase/100)

# Green cover effect approximations (lower AOD)
adj["aod"] = max(0.05, base["aod"] * (1 - green_cover_increase/100 * 0.6))

pm25_base, conf_base, *_ = predict_pm25_xgb(model_pack, **base)
pm25_new, conf_new, trend_new, health_level_new, _ = predict_pm25_xgb(model_pack, **adj)

pm_reduction = (pm25_base - pm25_new) / pm25_base * 100 if pm25_base > 0 else 0

# Environmental impact score
impact_score = np.clip(
    40 + 0.6 * pm_reduction + 0.15 * green_cover_increase - 0.1 * industrial_reduction,
    0,
    100,
)

risk_improvement = np.clip((pm_reduction * 0.9), -100, 100)

with glass_container("Scenario Results"):
    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric("Baseline PM2.5", f"{pm25_base:.1f} µg/m³")
    with r2:
        st.metric("Scenario PM2.5", f"{pm25_new:.1f} µg/m³")
    with r3:
        st.metric("Estimated PM Reduction", f"{pm_reduction:.1f}%")

with glass_container("Futuristic Impact Visualization"):
    values = [pm25_base, pm25_new]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Baseline", "Scenario"], y=values, marker_color=["#39e6ff", "#00ffc2"]))
    fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#d7f7ff'), yaxis_title='PM2.5 (µg/m³)')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f"""
        <div style='margin-top:10px; color:#8db7c7; font-weight:900;'>
          Environmental Impact Score: <span style='color:#39e6ff; font-size:24px; font-weight:1100;'>{impact_score:.0f}/100</span><br/>
          Trend Prediction: <span style='color:#00ffc2;'>{trend_new}</span><br/>
          Health Impact Level: <span style='color:#ffd166;'>{health_level_new}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Recommendation
with glass_container("AI Scenario Recommendations"):
    tips=[]
    if traffic_reduction < 20:
        tips.append("Traffic reduction is small—consider stronger LEZ enforcement and peak-hour public transport.")
    if industrial_reduction < 20:
        tips.append("Industrial reduction can be increased via process optimization and particulate controls.")
    if green_cover_increase < 20:
        tips.append("Increase green buffers near hotspots to reduce aerosol loading and resuspension.")
    if rainfall_increase < 20:
        tips.append("Rainfall is a natural factor—focus on emission control while maintaining readiness for washout periods.")
    if not tips:
        tips.append("Scenario looks well-balanced—monitor PM2.5 windows and maintain mitigation during stable stagnation hours.")

    for t in tips:
        st.markdown(f"• {t}")

st.caption("What-if outputs are derived from the offline XGBoost synthetic model + deterministic feature adjustments.")

