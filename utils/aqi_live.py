import numpy as np


def get_live_aqi_preview():
    """Return synthetic live AQI preview content for the landing page."""
    rng = np.random.default_rng(7)

    nation_pm25 = 145 + rng.normal(0, 10)
    nation_delta = float(rng.uniform(-6, 8))

    aqi_risk_index = 78 + rng.normal(0, 4)
    risk_delta = float(rng.uniform(-5, 6))

    forecast_delta = float(rng.uniform(-4, 6))
    forecast_label = rng.choice(["High risk window", "Moderate risk window", "Localized risk spike"])

    alerts = [
        {"city": "Delhi", "aqi": int(240 + rng.integers(-35, 35)), "msg": "Stagnant conditions", "level": "bad"},
        {"city": "Mumbai", "aqi": int(110 + rng.integers(-25, 25)), "msg": "Coastal mixing", "level": "warn"},
        {"city": "Pune", "aqi": int(160 + rng.integers(-25, 25)), "msg": "Traffic-driven rise", "level": "risk"},
        {"city": "Bengaluru", "aqi": int(95 + rng.integers(-20, 20)), "msg": "Lower accumulation", "level": "warn"},
        {"city": "Hyderabad", "aqi": int(135 + rng.integers(-25, 25)), "msg": "Humidity retention", "level": "risk"},
    ]

    highlights = [
        {"title": "6-hour PM2.5", "value": f"{int(nation_pm25 + 10)} µg/m³", "desc": "Short-term accumulation signal"},
        {"title": "24-hour AQI", "value": f"{int(aqi_risk_index)}", "desc": "Risk curve with confidence bands"},
        {"title": "Sensitive groups", "value": rng.choice(["Precaution", "Enhanced Mask" ,"Indoor Window"]), "desc": "Health intelligence layer"},
        {"title": "Clean-air scenario", "value": "-18% PM2.5", "desc": "Traffic + industrial reduction impact"},
    ]

    health_risk_score = int(68 + rng.integers(-8, 10))

    return {
        "nation_pm25": nation_pm25,
        "nation_delta": nation_delta,
        "aqi_risk_index": aqi_risk_index,
        "risk_delta": risk_delta,
        "forecast_delta": forecast_delta,
        "forecast_label": forecast_label,
        "alerts": alerts,
        "highlights": highlights,
        "health_risk_score": health_risk_score,
    }

