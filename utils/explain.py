import numpy as np


def explain_prediction(model_pack, features: dict):
    """Return an HTML string for AI explanation box."""
    model = model_pack["model"]

    # Feature importance
    try:
        importances = model.feature_importances_
        # XGBRegressor feature order matches training columns used in modeling.py
        feature_order = ["temperature", "humidity", "wind_speed", "rainfall", "aod", "traffic", "industrial"]
        imp_sorted = sorted(zip(feature_order, importances), key=lambda x: x[1], reverse=True)[:4]
    except Exception:
        imp_sorted = []

    # Rule-based environmental observations
    obs = []
    aod = float(features.get("aod", 0))
    wind = float(features.get("wind_speed", 0))
    hum = float(features.get("humidity", 0))
    traffic = float(features.get("traffic", 0))
    industrial = float(features.get("industrial", 0))
    rainfall = float(features.get("rainfall", 0))

    if wind < 2.0:
        obs.append("Low wind speed can cause pollutant accumulation near ground levels.")
    if hum > 70:
        obs.append("High humidity may trap particulate matter, increasing effective PM2.5 mass.")
    if rainfall < 8:
        obs.append("Low rainfall reduces atmospheric washout, allowing particulates to persist longer.")
    if traffic > 60:
        obs.append("Traffic congestion likely contributes to a PM2.5 spike via vehicle emissions and resuspension.")
    if industrial > 55:
        obs.append("Elevated industrial activity suggests higher regional emissions and slower dilution.")
    if aod > 0.6:
        obs.append("High AOD indicates elevated aerosol loading, strongly aligning with higher PM2.5.")

    if not obs:
        obs.append("Meteorology and emissions are balanced; expect a steadier pollution pattern.")

    # Compose HTML
    top_imp_html = "".join(
        [
            f"<div style='display:flex; justify-content:space-between; margin-top:6px;'><span style='color:#8db7c7; font-weight:900;'>{k}</span><span style='font-weight:1100; color:#39e6ff;'>{v:.3f}</span></div>"
            for k, v in imp_sorted
        ]
    )

    obs_html = "<ul style='margin:8px 0 0 18px; color:#d7f7ff; font-weight:700;'>" + "".join(
        [f"<li style='margin:6px 0;'>{o}</li>" for o in obs[:5]]
    ) + "</ul>"

    return f"""
    <div style='padding:14px; border-radius:16px; border:1px solid rgba(120,255,255,.18); background: rgba(0,0,0,.18);'>
      <div style='font-weight:1100; color:#39e6ff; font-size:16px;'>AI Explainability Snapshot</div>
      <div style='color:#8db7c7; font-weight:900; margin-top:6px;'>Top drivers (model-based)</div>
      {top_imp_html or '<div style="color:#8db7c7; font-weight:900; margin-top:6px;">Feature importance unavailable</div>'}
      <div style='color:#8db7c7; font-weight:900; margin-top:10px;'>Environmental observations (reasoning layer)</div>
      {obs_html}
      <div style='margin-top:10px; color:#8db7c7; font-weight:900; font-size:12px;'>Note: Explanation is synthetic/hackathon demo but remains consistent with the modeled PM2.5 factors.</div>
    </div>
    """

