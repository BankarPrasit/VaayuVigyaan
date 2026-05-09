"""utils/data_generator.py

The app pages import from `utils.data_generator`.

This repository originally contained data-fetching logic in the root `data.py`,
but that file only downloads OpenAQ measurements and does not expose the
expected symbols (e.g., `CITY_DATA`, `get_current_city_data`).

To make the Streamlit app fully runnable offline (and resilient when the
OpenAQ API fails), this module provides deterministic synthetic
city-level PM2.5 values and simple historical series generators.

No network calls are required.
"""

from __future__ import annotations

from datetime import datetime, timedelta


import numpy as np


# Cities used across the UI
CITY_DATA = {
    "Delhi": {"pm25": 165, "state": "Delhi"},
    "Mumbai": {"pm25": 95, "state": "Maharashtra"},
    "Pune": {"pm25": 120, "state": "Maharashtra"},
    "Bangalore": {"pm25": 70, "state": "Karnataka"},
    "Hyderabad": {"pm25": 105, "state": "Telangana"},
    "Chennai": {"pm25": 85, "state": "Tamil Nadu"},
    "Kolkata": {"pm25": 110, "state": "West Bengal"},
    "Ahmedabad": {"pm25": 140, "state": "Gujarat"},
}


def get_current_city_data() -> dict:
    """Return current (synthetic) city snapshot with small deterministic noise."""
    # Deterministic noise per run (still stable across rapid refreshes).
    now = datetime.now()
    seed = now.year * 10000 + now.month * 100 + now.day
    rng = np.random.default_rng(seed)

    out = {}
    for city, meta in CITY_DATA.items():
        pm = float(meta["pm25"]) + float(rng.normal(0, 6))
        pm = float(np.clip(pm, 10, 350))
        out[city] = {"pm25": pm, "state": meta.get("state", "")}
    return out


def generate_historical_data(city: str, days: int = 14) -> list[tuple[str, float]]:
    """Generate a synthetic daily PM2.5 trend for charts."""
    now = datetime.now()
    seed = (abs(hash(city)) % 10_000) + now.month * 31 + now.day
    rng = np.random.default_rng(seed)

    base = float(CITY_DATA.get(city, {"pm25": 100}).get("pm25", 100))
    dates = [now.replace(hour=0, minute=0, second=0, microsecond=0) for _ in range(days)]

    series = []
    # Create an upward/downward seasonal trend + noise
    for i in range(days):
        dt = now - timedelta(days=(days - 1 - i))

        season = 15 * np.sin((i / max(days - 1, 1)) * np.pi)
        drift = (i - (days - 1) / 2) * (rng.normal(0, 0.8))
        val = base + season + drift + rng.normal(0, 5)
        val = float(np.clip(val, 10, 350))
        series.append((str(dt.date()), val))

    return series


