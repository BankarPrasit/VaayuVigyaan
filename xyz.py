import xarray as xr

# Load the NetCDF file
ds = xr.open_dataset("g4.timeAvgMap.OMAERUVd_003_FinalAerosolOpticalDepth500.20250601-20250706.67E_5N_90E_37N.nc")

# See what variables are inside
print(ds)

# To see a specific variable like 'AOD'
print(ds['AOD'])  # or use ds.data_vars to list all

# Extract values
aod_data = ds['AOD'].values
lat = ds['latitude'].values
lon = ds['longitude'].values

# Show first few AOD values
print(aod_data[:5])
