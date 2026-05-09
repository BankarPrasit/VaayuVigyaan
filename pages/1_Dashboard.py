"""VaayuVigyaan AI — Dashboard Page
Interactive analytics with city maps, trends, and AQI comparisons
"""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.styles import inject_css, aqi_category, section_header, glass_metric
from utils.data_generator import get_current_city_data, generate_historical_data, CITY_DATA

st.set_page_config(page_title="Dashboard — VaayuVigyaan AI", page_icon="📊", layout="wide")
inject_css()

# Sidebar nav
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
    selected_city = st.selectbox("🏙️ Focus City", list(CITY_DATA.keys()), index=0)
    time_range = st.selectbox(
        "📅 Time Range", ["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year"], index=0
    )

# Page header
st.markdown(
    """
<div style='display:flex;align-items:center;gap:16px;margin-bottom:1.5rem'>
    <div>
        <h1 style='font-family:Rajdhani,sans-serif;font-size:2.4rem;font-weight:800;margin:0;background:linear-gradient(90deg,#e2e8f0,#00d4ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text'>
            Air Quality Dashboard
        </h1>
        <p style='color:#64748b;margin:0;font-size:0.9rem'>Real-time environmental monitoring across India</p>
    </div>
    <div style='margin-left:auto;background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.3);border-radius:10px;padding:8px 16px;font-family:Rajdhani,sans-serif;color:#00d4ff;font-size:0.85rem;font-weight:600'>
        ● LIVE DATA
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ─── LOAD DATA ────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def load_data():
    return generate_historical_data(365)


df_hist = load_data()
city_data = get_current_city_data()
days_map = {
    "Last 30 Days": 30,
    "Last 90 Days": 90,
    "Last 6 Months": 180,
    "Last Year": 365,
}
days = days_map[time_range]

# ─── TOP METRICS ──────────────────────────────────────────────
pm25_vals = [float(d.get("pm25", 0.0)) for d in city_data.values()]
valid_aqi_labels = [aqi_category(d.get("pm25", 0.0))[0] for d in city_data.values()]
# NOTE: aqi_category() returns a TEXT label at index 0; do NOT average labels.
# Compute a numeric AQI proxy instead, derived directly from PM2.5.
valid_aqi_numeric = []
for d in city_data.values():
    pm25 = float(d.get("pm25", 0.0))
    # Numeric proxy (monotonic) for aggregation.
    valid_aqi_numeric.append(pm25)
avg_aqi = float(np.mean(valid_aqi_numeric)) if valid_aqi_numeric else 0.0

worst_city = max(city_data, key=lambda c: city_data[c]["pm25"])
best_city = min(city_data, key=lambda c: city_data[c]["pm25"])
unhealthy = sum(1 for v in pm25_vals if v > 60)

cols = st.columns(4)
metrics_data = [
    ("National Avg PM2.5", f"{np.mean(pm25_vals):.1f}", "µg/m³", "🌫️"),
    ("Avg India AQI", f"{avg_aqi:.0f}", "NAQI Scale", "📊"),
    ("Most Polluted", worst_city, f"PM2.5: {city_data[worst_city]['pm25']:.0f}", "🔴"),
    ("Unhealthy Cities", str(unhealthy), "PM2.5 > 60 µg/m³", "⚠️"),
]

for col, (label, val, sub, icon) in zip(cols, metrics_data):
    col.markdown(glass_metric(label, val, sub, icon), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── MAP + CITY COMPARISON ────────────────────────────────────
col_map, col_bar = st.columns([3, 2])

with col_map:
    st.markdown(section_header("India PM2.5 Map", "LIVE", "🗺️"), unsafe_allow_html=True)
    map_df = pd.DataFrame(
        [
            {
                "city": c,
"lat": d.get("lat", 0.0),
                "lon": d["lon"],
                "pm25": d["pm25"],
"aqi": aqi_category(d["pm25"])[0],

                "state": d["state"],
                "category": aqi_category(d["pm25"])[0],
                "color": aqi_category(d["pm25"])[1],
            }
            for c, d in city_data.items()
        ]
    )

    fig_map = px.scatter_mapbox(
        map_df,
        lat="lat",
        lon="lon",
        size="pm25",
        color="pm25",
        hover_name="city",
        hover_data={
            "pm25": ":.0f",
            "aqi": ":.0f",
            "category": True,
            "lat": False,
            "lon": False,
        },
        color_continuous_scale=[
            [0, "#10b981"],
            [0.3, "#f59e0b"],
            [0.6, "#f97316"],
            [0.8, "#ef4444"],
            [1, "#7c3aed"],
        ],
        size_max=35,
        zoom=4.2,
        center={"lat": 22, "lon": 80},
        mapbox_style="carto-darkmatter",
        title="",
        labels={"pm25": "PM2.5 (µg/m³)"},
    )
    fig_map.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(
            bgcolor="rgba(10,20,40,0.7)",
            tickfont=dict(color="#94a3b8"),
            titlefont=dict(color="#94a3b8"),
            title="PM2.5",
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col_bar:
    st.markdown(section_header("City Ranking", "PM2.5", "🏆"), unsafe_allow_html=True)
    sorted_cities = sorted(city_data.items(), key=lambda x: x[1]["pm25"], reverse=True)
    bar_cities = [c for c, _ in sorted_cities]
    bar_vals = [d["pm25"] for _, d in sorted_cities]

    fig_bar = go.Figure(
        go.Bar(
            x=bar_vals,
            y=bar_cities,
            orientation="h",
            marker=dict(
                color=bar_vals,
                colorscale=[
                    [0, "#10b981"],
                    [0.3, "#f59e0b"],
                    [0.6, "#f97316"],
                    [0.8, "#ef4444"],
                    [1, "#7c3aed"],
                ],
                line=dict(width=0),
            ),
            text=[f"{v:.0f}" for v in bar_vals],
            textposition="outside",
            textfont=dict(color="#94a3b8", size=11),
            hovertemplate="<b>%{y}</b><br>PM2.5: %{x:.0f} µg/m³<extra></extra>",
        )
    )

    fig_bar.add_vline(
        x=60,
        line_color="#f59e0b",
        line_dash="dot",
        annotation_text="Moderate",
        annotation_font_color="#f59e0b",
    )
    fig_bar.add_vline(
        x=120,
        line_color="#ef4444",
        line_dash="dot",
        annotation_text="Unhealthy",
        annotation_font_color="#ef4444",
    )

    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            color="#64748b",
            gridcolor="rgba(0,212,255,0.08)",
            title="PM2.5 (µg/m³)",
            title_font_color="#64748b",
        ),
        yaxis=dict(color="#94a3b8"),
        margin=dict(l=0, r=50, t=10, b=20),
        height=380,
        bargap=0.3,
        showlegend=False,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ─── TREND CHARTS ─────────────────────────────────────────────
st.markdown(section_header(f"PM2.5 Trend — {selected_city}", time_range, "📈"), unsafe_allow_html=True)

df_city = df_hist[df_hist["city"] == selected_city].tail(days).copy()
df_city["date"] = pd.to_datetime(df_city["date"])

col_trend, col_heatmap = st.columns([3, 2])

with col_trend:
    df_city["pm25_7d"] = df_city["pm25"].rolling(7, min_periods=1).mean()

    fig_trend = go.Figure()
    fig_trend.add_trace(
        go.Scatter(
            x=df_city["date"],
            y=df_city["pm25"],
            mode="lines",
            name="Daily PM2.5",
            line=dict(color="rgba(0,212,255,0.4)", width=1),
            fill="tozeroy",
            fillcolor="rgba(0,212,255,0.05)",
        )
    )
    fig_trend.add_trace(
        go.Scatter(
            x=df_city["date"],
            y=df_city["pm25_7d"],
            mode="lines",
            name="7-Day Avg",
            line=dict(color="#00d4ff", width=2.5),
        )
    )

    fig_trend.add_hrect(
        y0=0, y1=30, fillcolor="rgba(16,185,129,0.05)", line_width=0, annotation_text="Good"
    )
    fig_trend.add_hrect(y0=30, y1=60, fillcolor="rgba(132,204,22,0.04)", line_width=0)
    fig_trend.add_hrect(y0=60, y1=90, fillcolor="rgba(245,158,11,0.04)", line_width=0)
    fig_trend.add_hrect(y0=90, y1=500, fillcolor="rgba(239,68,68,0.04)", line_width=0)

    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#64748b", gridcolor="rgba(0,212,255,0.06)"),
        yaxis=dict(
            color="#64748b",
            gridcolor="rgba(0,212,255,0.06)",
            title="PM2.5 (µg/m³)",
            title_font_color="#64748b",
        ),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
        margin=dict(l=0, r=0, t=10, b=0),
        height=280,
        hovermode="x unified",
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col_heatmap:
    st.markdown(
        "<div style='font-size:0.85rem;color:#94a3b8;margin-bottom:8px'>Monthly Average PM2.5</div>",
        unsafe_allow_html=True,
    )

    monthly = df_city.copy()
    monthly["month"] = monthly["date"].dt.month
    monthly["month_name"] = monthly["date"].dt.strftime("%b")
    monthly_avg = monthly.groupby("month_name")["pm25"].mean().reset_index()

    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_avg["month_name"] = pd.Categorical(
        monthly_avg["month_name"], categories=month_order, ordered=True
    )
    monthly_avg = monthly_avg.sort_values("month_name")

    fig_monthly = px.bar(
        monthly_avg,
        x="month_name",
        y="pm25",
        color="pm25",
        color_continuous_scale=[[0, "#10b981"], [0.4, "#f59e0b"], [0.7, "#ef4444"], [1, "#7c3aed"]],
    )
    fig_monthly.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#64748b", title=""),
        yaxis=dict(
            color="#64748b",
            gridcolor="rgba(0,212,255,0.06)",
            title="Avg PM2.5",
        ),
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0),
        height=280,
        showlegend=False,
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

# ─── MULTI-CITY COMPARISON ────────────────────────────────────
st.markdown("<hr class='cyber-divider'>", unsafe_allow_html=True)
st.markdown(section_header("Multi-City Comparison", "TREND", "⚖️"), unsafe_allow_html=True)

compare_cities = st.multiselect(
    "Select cities to compare",
    list(CITY_DATA.keys()),
    default=["Delhi", "Mumbai", "Pune", "Bengaluru", "Kolkata"],
)

if compare_cities:
    df_compare = df_hist[df_hist["city"].isin(compare_cities)].tail(days * len(compare_cities)).copy()
    df_compare["date"] = pd.to_datetime(df_compare["date"])
    df_compare = df_compare.groupby(["date", "city"])["pm25"].mean().reset_index()

    colors = ["#00d4ff", "#00f5c8", "#f59e0b", "#ef4444", "#3b82f6", "#10b981", "#8b5cf6", "#f97316"]

    fig_compare = go.Figure()
    for i, city in enumerate(compare_cities):
        c_df = df_compare[df_compare["city"] == city].sort_values("date")
        c_df["pm25_7d"] = c_df["pm25"].rolling(7, min_periods=1).mean()

        fig_compare.add_trace(
            go.Scatter(
                x=c_df["date"],
                y=c_df["pm25_7d"],
                mode="lines",
                name=city,
                line=dict(color=colors[i % len(colors)], width=2),
                hovertemplate=f"<b>{city}</b><br>PM2.5: %{{y:.0f}} µg/m³<extra></extra>",
            )
        )

    fig_compare.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#64748b", gridcolor="rgba(0,212,255,0.06)"),
        yaxis=dict(
            color="#64748b",
            gridcolor="rgba(0,212,255,0.06)",
            title="PM2.5 (µg/m³)",
            title_font_color="#64748b",
        ),
        legend=dict(
            bgcolor="rgba(10,20,40,0.6)",
            font=dict(color="#94a3b8"),
            bordercolor="rgba(0,212,255,0.2)",
            borderwidth=1,
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        height=320,
        hovermode="x unified",
    )

    st.plotly_chart(fig_compare, use_container_width=True)

# ─── WEATHER CORRELATION ──────────────────────────────────────
st.markdown(
    section_header("Weather × Pollution Correlation", "ANALYTICS", "🌤️"), unsafe_allow_html=True
)

col_w1, col_w2 = st.columns(2)
df_city_recent = df_hist[df_hist["city"] == selected_city].tail(90)

with col_w1:
    fig_scatter = px.scatter(
        df_city_recent,
        x="wind_speed",
        y="pm25",
        color="humidity",
        size="pm25",
        color_continuous_scale=[[0, "#ef4444"], [0.5, "#f59e0b"], [1, "#10b981"]],
        labels={"wind_speed": "Wind Speed (m/s)", "pm25": "PM2.5 (µg/m³)", "humidity": "Humidity (%)"},
        title="Wind Speed vs PM2.5",
        trendline="lowess",
    )
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#64748b", gridcolor="rgba(0,212,255,0.06)"),
        yaxis=dict(color="#64748b", gridcolor="rgba(0,212,255,0.06)"),
        coloraxis_colorbar=dict(
            bgcolor="rgba(10,20,40,0.6)",
            tickfont=dict(color="#64748b"),
            titlefont=dict(color="#64748b"),
        ),
        title_font_color="#94a3b8",
        margin=dict(l=0, r=0, t=40, b=0),
        height=280,
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_w2:
    fig_rain = px.scatter(
        df_city_recent,
        x="rainfall",
        y="pm25",
        color="temperature",
        color_continuous_scale=[[0, "#3b82f6"], [0.5, "#f59e0b"], [1, "#ef4444"]],
        labels={"rainfall": "Rainfall (mm)", "pm25": "PM2.5 (µg/m³)", "temperature": "Temp (°C)"},
        title="Rainfall vs PM2.5",
    )
    fig_rain.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#64748b", gridcolor="rgba(0,212,255,0.06)"),
        yaxis=dict(color="#64748b", gridcolor="rgba(0,212,255,0.06)"),
        coloraxis_colorbar=dict(
            bgcolor="rgba(10,20,40,0.6)",
            tickfont=dict(color="#64748b"),
            titlefont=dict(color="#64748b"),
        ),
        title_font_color="#94a3b8",
        margin=dict(l=0, r=0, t=40, b=0),
        height=280,
    )
    st.plotly_chart(fig_rain, use_container_width=True)

