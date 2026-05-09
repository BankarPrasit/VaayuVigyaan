import numpy as np


def pm25_to_aqi_category(pm25: float):
    """Convert PM2.5 to a simple AQI-like category for UI."""
    v = float(pm25)
    if v <= 50:
        return {"label": "Good", "severity": "Low health impact", "band": "good"}
    if v <= 100:
        return {"label": "Moderate", "severity": "Sensitive groups may notice", "band": "moderate"}
    if v <= 150:
        return {"label": "Unhealthy (SG)", "severity": "Limit outdoor activity", "band": "unhealthy_sg"}
    if v <= 250:
        return {"label": "Unhealthy", "severity": "Health warnings", "band": "unhealthy"}
    return {"label": "Very Unhealthy", "severity": "Avoid exposure", "band": "very_unhealthy"}

