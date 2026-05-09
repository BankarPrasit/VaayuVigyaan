import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from utils.theme import apply_global_theme
from utils.ui_components import glass_container

apply_global_theme()

st.markdown("<h2 style='margin:0;'>🔮 Future Forecast (Next 6h / 24h / 3 days)</h2>", unsafe_allow_html=True)

with glass_container("Forecast Inputs"):
    current_pm25 = st.number_input("Current PM2.5 (µg/m³)", 10.0, 520.0, 145.0, 1.0)
    wind_speed = st.number_input("Wind Speed (m/s)", 0.0, 25.0, 2.3, 0.1)
    rainfall = st.number_input("Rainfall (mm)", 0.0, 200.0, 6.0, 1.0)
    confidence = st.slider("Model confidence proxy", 40, 95, 70)

# Simulate curves
rng = np.random.default_rng(4)

accum_strength = np.clip(3.2 - wind_speed, 0.2, 3.2)
washout = np.clip(rainfall / 60, 0, 1.2)

risk_dir = "Rising" if (accum_strength - washout) > 1.0 else "Falling" if washout > 0.6 else "Stable"

st.markdown(
    f"""
    <div style='color:#8db7c7; font-weight:900;'>Predicted pattern: <span style='color:#00ffc2;'>{risk_dir}</span></div>
    """,
    unsafe_allow_html=True,
)

band = (100 - confidence) / 100 * 28

# 6h
with glass_container("Next 6 Hours Forecast"):
    xs = np.arange(6)
    if risk_dir == "Rising":
        ys = current_pm25 + xs * (7 + 0.25 * confidence) * (0.8 + accum_strength/3)
    elif risk_dir == "Falling":
        ys = current_pm25 - xs * (6 + 0.2 * confidence) * (0.7 + washout)
    else:
        ys = current_pm25 + np.sin(xs/1.6) * 4
    ys = np.clip(ys, 5, 520)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines+markers', line=dict(color='#39e6ff', width=3), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=np.concatenate([xs, xs[::-1]]), y=np.concatenate([ys-band, (ys+band)[::-1]]),
                               fill='toself', fillcolor='rgba(57,230,255,.15)', line=dict(color='rgba(0,0,0,0)')))
    fig.update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#d7f7ff'), xaxis_title='Hour', yaxis_title='PM2.5')
    st.plotly_chart(fig, use_container_width=True)

# 24h
with glass_container("Next 24 Hours Forecast"):
    xs = np.arange(24)
    daily_wave = np.sin(xs/24 * np.pi) * (5 + rng.uniform(0, 4))
    if risk_dir == "Rising":
        ys = current_pm25 + xs * (2.2 + 0.05 * confidence) * (0.9 + accum_strength/3) + daily_wave
    elif risk_dir == "Falling":
        ys = current_pm25 - xs * (1.9 + 0.04 * confidence) * (0.8 + washout) + daily_wave
    else:
        ys = current_pm25 + daily_wave * 2
    ys = np.clip(ys, 5, 520)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color='#00ffc2', width=3)))
    fig.add_trace(go.Scatter(x=np.concatenate([xs, xs[::-1]]), y=np.concatenate([ys-band, (ys+band)[::-1]]),
                               fill='toself', fillcolor='rgba(0,255,194,.12)', line=dict(color='rgba(0,0,0,0)')))
    fig.update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#d7f7ff'), xaxis_title='Hour', yaxis_title='PM2.5')
    st.plotly_chart(fig, use_container_width=True)

# 3 day
with glass_container("Next 3-Day Risk Timeline"):
    days = np.arange(1, 4)
    if risk_dir == "Rising":
        ys = current_pm25 + days * (18 + 0.2 * confidence) * (0.8 + accum_strength/3)
    elif risk_dir == "Falling":
        ys = current_pm25 - days * (15 + 0.18 * confidence) * (0.7 + washout)
    else:
        ys = current_pm25 + days * rng.uniform(-8, 10)
    ys = np.clip(ys, 5, 520)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=days, y=ys, marker_color='#ffd166'))
    fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#d7f7ff'), xaxis_title='Day', yaxis_title='PM2.5')
    st.plotly_chart(fig, use_container_width=True)

st.caption("Forecast curves are synthetic but designed to feel realistic and deployable offline.")

