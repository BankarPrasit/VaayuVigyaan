import streamlit as st
import joblib
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import datetime
import plotly.express as px

# Load model
model = joblib.load("pm25_rf_model.pkl")

# Streamlit page config
st.set_page_config(page_title="VaayuVigyaan - PM2.5 Air Quality Predictor", layout="centered")
st.title("🌫️ VaayuVigyaan - Advanced PM2.5 Predictor")
st.markdown("Predict air pollution (PM2.5) using AOD, temperature, humidity, and location info with visual heatmaps and reports.")

# Session initialization
if "show_output" not in st.session_state:
    st.session_state.show_output = False

# 📍 Inputs
st.sidebar.header("📥 Inputs")
selected_date = st.sidebar.date_input("Prediction Date", datetime.date.today())
aod = st.sidebar.slider("AOD (Aerosol Optical Depth)", 0.1, 1.0, 0.3)
temp = st.sidebar.number_input("Temperature (°C)", min_value=10.0, max_value=50.0, value=30.0)
humidity = st.sidebar.slider("Humidity (%)", 0, 100, 60)
city = st.sidebar.selectbox("Your City", ["Aurangabad", "Pune", "Mumbai", "Nagpur", "Ahmedabad", "Vizag"])

# 🔮 Predict
if st.sidebar.button("🎯 Predict PM2.5"):
    input_df = pd.DataFrame([[aod, temp, humidity]], columns=['AOD', 'temp', 'rh'])
    prediction = model.predict(input_df)[0]
    st.session_state.prediction = prediction
    st.session_state.city = city
    st.session_state.date = selected_date
    st.session_state.show_output = True

# 🔁 Reset
if st.sidebar.button("🔄 Reset"):
    st.session_state.show_output = False

# 📊 Output section
if st.session_state.show_output:
    st.header(f"📍 Air Quality Prediction for {st.session_state.city} on {st.session_state.date}")
    prediction = st.session_state.prediction

    st.success(f"✅ Predicted PM2.5: {prediction:.2f} µg/m³")

    # 🩺 Health Risk Indicator
    if prediction < 100:
        st.markdown("🟢 **Good** – Clean air 🙂")
    elif prediction < 200:
        st.markdown("🟡 **Moderate** – Sensitive groups be cautious 😷")
    elif prediction < 300:
        st.markdown("🟠 **Unhealthy** – Limit outdoor activity ⚠️")
    else:
        st.markdown("🔴 **Hazardous** – Avoid going out 🚫")

    # 📊 Optional Trend Chart
    st.subheader("📈 PM2.5 Trend (Last 5 Days - Demo Data)")
    trend_data = pd.DataFrame({
        "Date": pd.date_range(end=st.session_state.date, periods=5),
        "PM2.5": [prediction - 15, prediction - 5, prediction, prediction + 10, prediction + 5]
    })
    fig = px.line(trend_data, x="Date", y="PM2.5", title="PM2.5 5-Day Trend", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # 📤 Report Download
    st.subheader("📥 Download Prediction Report")
    report_df = pd.DataFrame({
        "City": [st.session_state.city],
        "Date": [st.session_state.date],
        "AOD": [aod],
        "Temp": [temp],
        "Humidity": [humidity],
        "PM2.5": [round(prediction, 2)]
    })
    csv = report_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "pm25_report.csv", "text/csv")

    # 📍 Heatmap
    st.subheader("🗺️ Maharashtra PM2.5 Heatmap")
    city_coords = {
        "Aurangabad": [19.8762, 75.3433],
        "Pune": [18.5204, 73.8567],
        "Mumbai": [19.0760, 72.8777],
        "Nagpur": [21.1458, 79.0882],
        "Vizag": [17.6868, 83.2185],
        "Ahmedabad": [23.0225, 72.5714],
    }

    heat_data = [
        [city_coords[city][0], city_coords[city][1], prediction],
        [18.5204, 73.8567, 120],
        [19.0760, 72.8777, 90],
        [21.1458, 79.0882, 150],
        [17.6868, 83.2185, 180],
        [23.0225, 72.5714, 80],
    ]

    m = folium.Map(location=[19.5, 76], zoom_start=6)
    HeatMap(heat_data, radius=25, blur=20, max_zoom=10).add_to(m)
    st_folium(m, width=700, height=500)

    # 🔔 City Comparison Table
    st.subheader("📊 PM2.5 Comparison")
    df_cmp = pd.DataFrame({
        "City": ["You", "Pune", "Mumbai", "Nagpur"],
        "PM2.5": [round(prediction, 2), 120, 90, 150]
    })
    st.table(df_cmp)