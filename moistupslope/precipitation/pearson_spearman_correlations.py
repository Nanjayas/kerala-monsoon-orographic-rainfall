
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr

# Kerala Monsoon Project - JJAS 2020
# Pearson and Spearman spatial correlations

base = Path.home() / "kerala_project/data"

# 1. Load seasonal GPM rainfall total
with xr.open_dataset(
    base / "gpm/rain_land_jjas2020.nc"
) as ds:
    rain = ds["rain"].sum("time", skipna=False).load()

# 2. Load seasonal-mean orographic diagnostics
with xr.open_dataset(
    base / "derived/orographic_moisture_JJAS2020.nc"
) as ds:
    w_oro = ds["w_oro"].mean("time").load()
    moist = ds["moist_upslope"].mean("time").load()

# 3. Check matching spatial coordinates
rain, w_oro, moist = xr.align(
    rain, w_oro, moist, join="exact"
)

# 4. Select valid land grid cells
valid = (
    np.isfinite(rain.values)
    & np.isfinite(w_oro.values)
    & np.isfinite(moist.values)
)

# 5. Create a table with 225 spatial observations
data = pd.DataFrame({
    "rainfall": rain.values[valid],
    "w_oro": w_oro.values[valid],
    "moist_upslope": moist.values[valid],
})

print("Number of land cells:", len(data))

# 6. Pearson linear correlation
print("\nPearson correlations:")
print(data.corr(method="pearson"))

# 7. Spearman rank correlation
print("\nSpearman correlations:")
print(data.corr(method="spearman"))
