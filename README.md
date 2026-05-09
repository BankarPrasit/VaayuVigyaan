<<<<<<< HEAD
# VaayuVigyaan AI — India Air Pollution Intelligence Platform

**VaayuVigyaan AI** is a futuristic, hackathon-ready **Streamlit** platform that predicts **PM2.5**, converts it to **AQI-like categories**, generates **health recommendations**, produces **AI insights**, forecasts short-term pollution risk, and simulates **what-if reduction scenarios**.

> This build is **fully deployable** and runs **offline** with synthetic data + an **offline XGBoost model** trained on a synthetic but realistic environmental feature space.

---

## Features (Multipage)

- **Home**: Animated hero + live synthetic AQI preview cards + alerts
- **Dashboard**: Interactive city AQI visualization + heatmap + historical trend (demo)
- **AI Predictor**: XGBoost PM2.5 prediction + confidence proxy + explanation snapshot
- **Health Impact**: Asthma risk, elderly safety, child safety, mask + outdoor guidance
- **AI Insights**: Explainable environmental reasoning + insight timeline (simulated)
- **Future Forecast**: Next 6h / 24h / 3-day synthetic forecast curves
- **What-If Simulator**: Sliders for traffic/industrial/rain/green cover impact

---

## Quick Start (Local)

### 1) Setup virtual environment
```bash
python -m venv venv
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Run Streamlit
```bash
streamlit run app.py
```

On first run, if the XGBoost model artifacts are missing, the app will train them automatically.

---

## Deployment

### Streamlit Cloud
1. Create a new **Streamlit Community Cloud** app
2. Connect your GitHub repo (recommended) or upload the project
3. Entry file: **`app.py`**
4. Streamlit Cloud will install dependencies from `requirements.txt`

### Render (Web Service)
1. Create a new **Web Service**
2. Use Python environment
3. Start Command:
   ```bash
   streamlit run app.py --server.port $PORT
   ```
4. Build Command (optional):
   ```bash
   pip install -r requirements.txt
   ```

---

## Notes
- Synthetic data is used so the project is deployable without external API keys.
- The ML model is trained on synthetic feature relationships and packaged for repeatable predictions.


=======
# VaayuVigyaan
VaayuVigyaan is an AI-driven environmental monitoring platform that predicts PM2.5 pollution levels, analyzes AQI trends, provides health impact insights, and visualizes air quality data through interactive dashboards built with Python, Machine Learning, and Streamlit.
>>>>>>> c64f6283f9ecdb52c0ff56c870625a52323ecddb
