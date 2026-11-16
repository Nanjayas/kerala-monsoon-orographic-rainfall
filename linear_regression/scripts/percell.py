"""
Per-cell regression: daily GPM rainfall vs daily moist-upslope index.

At every land grid cell, a separate linear regression and correlation is
computed over the 122 days of JJAS 2020. Results are saved as a NetCDF file
and as one map (PNG) per quantity.

Usage:
    python per_cell_regression.py RAIN_FILE MOIST_FILE OUT_DIR

RAIN_FILE   NetCDF with daily land-masked rainfall, variable 'rain' (mm/day)
MOIST_FILE  NetCDF with daily moist-upslope index, variable 'moist_upslope'
OUT_DIR     folder for the results file and the maps
"""
import sys
from pathlib import Path

import numpy as np
import xarray as xr
from scipy.stats import rankdata
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

if len(sys.argv) != 4:
    sys.exit("Usage: python per_cell_regression.py RAIN_FILE MOIST_FILE OUT_DIR")

rain_file, moist_file, out_dir = sys.argv[1], sys.argv[2], Path(sys.argv[3])
out_dir.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- load
with xr.open_dataset(rain_file) as ds:
    rain = ds["rain"].load()
with xr.open_dataset(moist_file) as ds:
    moist = ds["moist_upslope"].load()

# The two files carry different time-of-day stamps (00:00 vs 11:30).
# Label both by calendar date and require an exact match.
rain["time"] = rain["time"].dt.floor("D")
moist["time"] = moist["time"].dt.floor("D")
assert (rain.time.values == moist.time.values).all(), "dates differ"
rain, moist = xr.align(rain, moist, join="exact")

land = np.isfinite(rain).all("time") & np.isfinite(moist).all("time")
n_days = rain.sizes["time"]
print(f"Land cells: {int(land.sum())}, days: {n_days}")

P = rain.where(land)             # mm/day
M = moist.where(land) * 1000     # scaled x1000 for readable units

# ------------------------------------------- per-cell least-squares fit
dP = P - P.mean("time")
dM = M - M.mean("time")
cov = (dP * dM).mean("time")
varP = (dP**2).mean("time")
varM = (dM**2).mean("time")

slope = cov / varM                                   # mm/day per unit of (1000 x M)
intercept = P.mean("time") - slope * M.mean("time")  # mm/day
r = cov / np.sqrt(varP * varM)                       # Pearson
r2 = r**2
rmse = np.sqrt(varP * (1 - r2))                      # mm/day


def ranks(a):
    """Rank along time (ocean NaNs filled before ranking, masked again after)."""
    out = rankdata(a.fillna(0).values, axis=0)
    return xr.DataArray(out, coords=a.coords, dims=a.dims).where(land)


rho = xr.corr(ranks(P), ranks(M), dim="time")        # Spearman
n_zero_M = (M == 0).sum("time").where(land)          # days with no upslope forcing

# Consistency check: our r must equal xarray's own correlation
assert np.allclose(r.values[land.values], xr.corr(P, M, dim="time").values[land.values])

res = xr.Dataset({
    "slope": slope, "intercept": intercept, "pearson_r": r, "spearman_rho": rho,
    "r2": r2, "rmse": rmse, "n_zero_M_days": n_zero_M,
})
res["slope"].attrs["units"] = "mm/day per unit of (1000 x moist_upslope)"
res["intercept"].attrs["units"] = "mm/day"
res["rmse"].attrs["units"] = "mm/day"
res_file = out_dir / "per_cell_regression_jjas2020.nc"
res.to_netcdf(res_file)
print("saved:", res_file)

# ------------------------------------------------------------ summary
print(f"\nPer-cell results over {int(land.sum())} land cells ({n_days} daily pairs each):")
for name, a in [("Pearson r", r), ("Spearman rho", rho), ("R^2", r2), ("slope", slope),
                ("intercept", intercept), ("RMSE mm/day", rmse), ("days with M=0", n_zero_M)]:
    v = a.values[land.values]
    print(f"{name:14s} min {v.min():9.3f}  median {np.median(v):9.3f}  max {v.max():9.3f}")

rv = r.values[land.values]
print(f"\ncells with r > 0   : {int((rv > 0).sum())} of {rv.size}")
print(f"cells with r > 0.3 : {int((rv > 0.3).sum())}")
print(f"cells with r > 0.5 : {int((rv > 0.5).sum())}")

# --------------------------------------------------------------- maps
# name, title, colormap, vmin, vmax (None = set below), colorbar label
panels = [
    ("pearson_r", "Pearson r: daily rainfall vs moist-upslope index", "RdBu_r", -0.6, 0.6, "r"),
    ("spearman_rho", "Spearman rho: daily rainfall vs moist-upslope index", "RdBu_r", -0.6, 0.6, "rho"),
    ("r2", "R$^2$ of the per-cell linear fit", "viridis", 0.0, 0.35, "R$^2$"),
    ("slope", "Regression slope", "RdBu_r", None, None, "mm/day per unit of (1000 x M)"),
    ("intercept", "Regression intercept", "viridis", None, None, "mm/day"),
    ("rmse", "RMSE of the per-cell fit", "magma_r", None, None, "mm/day"),
    ("n_zero_M_days", f"Days with M = 0 (of {n_days})", "magma_r", 0, n_days, "days"),
]

for name, title, cmap, vmin, vmax, label in panels:
    data = res[name]
    if name == "slope":   # symmetric around 0, robust to a few extremes
        lim = float(np.nanpercentile(np.abs(data.values), 98))
        vmin, vmax = -lim, lim
    elif vmin is None:
        vmin, vmax = float(data.min()), float(data.max())

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    pcm = ax.pcolormesh(res.lon, res.lat, data, cmap=cmap, vmin=vmin, vmax=vmax, shading="auto")
    ax.set_aspect("equal")
    ax.set_xlabel("Longitude (deg E)")
    ax.set_ylabel("Latitude (deg N)")
    ax.set_title(title + "\nJJAS 2020, land cells", fontsize=10)
    fig.colorbar(pcm, ax=ax, shrink=0.85, label=label)
    fig.tight_layout()
    fig.savefig(out_dir / f"{name}_map.png", dpi=200)
    plt.close(fig)
    print("saved:", out_dir / f"{name}_map.png")
