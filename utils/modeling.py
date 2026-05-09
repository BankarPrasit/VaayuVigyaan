import os
import joblib
import numpy as np
import pandas as pd

import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score


MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "xgb_pm25_model.joblib")
SCALER_PATH = os.path.join(MODEL_DIR, "xgb_scaler.joblib")


def _build_synthetic_dataset(n: int = 6000, seed: int = 42):
    rng = np.random.default_rng(seed)

    # Features required by the prompt
    temperature = rng.uniform(10, 50, n)
    humidity = rng.uniform(10, 95, n)
    wind_speed = rng.uniform(0.1, 12, n)
    rainfall = rng.uniform(0, 120, n)
    aod = rng.uniform(0.05, 1.2, n)
    traffic = rng.uniform(0, 100, n)
    industrial = rng.uniform(0, 100, n)

    # A realistic-ish synthetic PM2.5 formula with interactions
    # - Higher AOD increases PM2.5
    # - Higher wind reduces accumulation
    # - Rain reduces via washout
    # - Humidity can trap particulates
    # - Traffic/industrial increase emissions
    pm25 = (
        aod * 240
        + temperature * 0.9
        + (humidity / 100) * 35
        - wind_speed * 6.5
        - (rainfall / 120) * 18
        + (traffic / 100) * 55
        + (industrial / 100) * 70
        + rng.normal(0, 12, n)
    )
    pm25 = np.clip(pm25, 5, 520)

    df = pd.DataFrame(
        {
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "rainfall": rainfall,
            "aod": aod,
            "traffic": traffic,
            "industrial": industrial,
            "pm25": pm25,
        }
    )
    return df


def load_or_train_xgb_model(force_retrain: bool = False):
    os.makedirs(MODEL_DIR, exist_ok=True)

    if (not force_retrain) and os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        model_pack = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        return {"model": model_pack, "scaler": scaler}

    df = _build_synthetic_dataset()
    X = df[["temperature", "humidity", "wind_speed", "rainfall", "aod", "traffic", "industrial"]]
    y = df["pm25"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    model = xgb.XGBRegressor(
        n_estimators=700,
        learning_rate=0.03,
        max_depth=5,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_alpha=0.0,
        reg_lambda=1.5,
        random_state=42,
        tree_method="hist",
    )

    model.fit(X_train_s, y_train)

    preds = model.predict(X_test_s)
    mae = float(mean_absolute_error(y_test, preds))
    r2 = float(r2_score(y_test, preds))

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    # Store minimal metadata for UI/debug
    meta_path = os.path.join(MODEL_DIR, "xgb_training_meta.joblib")
    joblib.dump({"mae": mae, "r2": r2}, meta_path)

    return {"model": model, "scaler": scaler}


def predict_pm25_xgb(model_pack, temperature, humidity, wind_speed, rainfall, aod, traffic, industrial):
    model = model_pack["model"]
    scaler = model_pack["scaler"]

    X = pd.DataFrame(
        [[temperature, humidity, wind_speed, rainfall, aod, traffic, industrial]],
        columns=["temperature", "humidity", "wind_speed", "rainfall", "aod", "traffic", "industrial"],
    )

    Xs = scaler.transform(X)

    # Point prediction
    pm25_pred = float(model.predict(Xs)[0])

    # Confidence proxy: use distance from training mean and model sensitivity.
    # (Hackathon-friendly approximation; keeps it fully offline.)
    mean = scaler.mean_
    std = np.maximum(scaler.scale_, 1e-6)
    z = (X.values[0] - mean) / std
    z_norm = float(np.linalg.norm(z))
    conf = max(25.0, 95.0 - z_norm * 6.0)  # 25-95%

    # Trend direction heuristic based on wind and rain influence
    if wind_speed < 2.0 and rainfall < 5.0:
        trend = "Rising"
    elif wind_speed > 6.0 or rainfall > 35.0:
        trend = "Falling"
    else:
        trend = "Stable"

    # Health level
    if pm25_pred < 80:
        health_level = "Low"
    elif pm25_pred < 140:
        health_level = "Moderate"
    elif pm25_pred < 220:
        health_level = "High"
    else:
        health_level = "Severe"

    return pm25_pred, conf, trend, health_level, X.iloc[0].to_dict()

