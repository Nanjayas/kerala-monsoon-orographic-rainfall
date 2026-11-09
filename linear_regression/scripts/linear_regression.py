"""
Simple linear regression: total JJAS 2020 GPM rainfall vs seasonal-mean
moist-upslope index over the 225 land cells.

Usage:
    python linear_regression.py RAIN_FILE MOIST_FILE

RAIN_FILE   NetCDF with daily land-masked rainfall, variable 'rain' (mm/day)
MOIST_FILE  NetCDF with daily moist-upslope index, variable 'moist_upslope'
"""
import sys

import numpy as np
import xarray as xr
from scipy import stats

if len(sys.argv) != 3:
    sys.exit("Usage: python linear_regression.py RAIN_FILE MOIST_FILE")

rain_file, moist_file = sys.argv[1], sys.argv[2]

# Seasonal total rainfall (mm) and seasonal-mean moist-upslope index.
# skipna=False: a missing day gives NaN instead of a silently low total.
with xr.open_dataset(rain_file) as ds:
    P_map = ds["rain"].sum(dim="time", skipna=False).load()
with xr.open_dataset(moist_file) as ds:
    M_map = ds["moist_upslope"].mean(dim="time", skipna=False).load()

# The two grids must match exactly, otherwise cells would be paired wrongly
P_map, M_map = xr.align(P_map, M_map, join="exact")

# Keep only cells that are valid in both fields
valid = np.isfinite(P_map.values) & np.isfinite(M_map.values)
P = P_map.values[valid]
M = M_map.values[valid] * 1000  # scaled x1000 for readable units

print(f"Valid land cells : {len(P)}")
print(f"Rainfall range   : {P.min():.1f} to {P.max():.1f} mm (mean {P.mean():.1f} mm)")
print(f"M range (x1000)  : {M.min():.4g} to {M.max():.4g}")
print(f"Cells with M == 0: {int((M == 0).sum())}")

# Correlations
r = stats.pearsonr(M, P)[0]
rho = stats.spearmanr(M, P)[0]

# Fit P_hat = b0 + b1 * M by least squares
b1, b0 = np.polyfit(M, P, 1)
P_hat = b0 + b1 * M
resid = P - P_hat
ss_res = np.sum(resid**2)
ss_tot = np.sum((P - P.mean()) ** 2)
r2 = 1 - ss_res / ss_tot
rmse = np.sqrt(np.mean(resid**2))

print("\n===== Regression results =====")
print(f"Intercept b0 : {b0:.2f} mm")
print(f"Slope b1     : {b1:.1f} mm per unit of (1000 x M)")
print(f"R^2          : {r2:.4f}")
print(f"RMSE         : {rmse:.2f} mm ({100 * rmse / P.mean():.1f} % of mean rainfall)")

print("\n===== Correlations and checks =====")
print(f"Pearson r    : {r:.4f}  (r^2 = {r**2:.4f}, must equal R^2)")
print(f"Spearman rho : {rho:.4f}")
print(f"Mean residual: {resid.mean():.2e}  (should be about 0)")