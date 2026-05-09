import xarray as xr
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Load your .nc file
ds = xr.open_dataset("g4.timeAvgMap.OMAERUVd_003_FinalAerosolOpticalDepth500.20250601-20250706.67E_5N_90E_37N.nc")
aod = ds['OMAERUVd_003_FinalAerosolOpticalDepth500'].values
lats = ds['lat'].values
lons = ds['lon'].values

lat_grid, lon_grid = np.meshgrid(lats, lons, indexing='ij')
df = pd.DataFrame({
    'latitude': lat_grid.flatten(),
    'longitude': lon_grid.flatten(),
    'AOD': aod.flatten()
})
df = df.dropna()

# Add dummy weather features
np.random.seed(42)
df['temp'] = np.random.uniform(20, 35, size=len(df))
df['rh'] = np.random.uniform(40, 80, size=len(df))

# Synthetic PM2.5 based on formula
df['pm25'] = df['AOD'] * 200 + df['temp'] * 1.5 + (100 - df['rh']) * 0.8 + np.random.normal(0, 5, len(df))

# Train Random Forest
X = df[['AOD', 'temp', 'rh']]
y = df['pm25']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "pm25_rf_model.pkl")
print("✅ Model trained and saved as pm25_rf_model.pkl")
