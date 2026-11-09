
from pathlib import Path
import numpy as np
import xarray as xr

# ==========================================
# Kerala Monsoon Project - JJAS 2020
# Orographic and moisture diagnostics
# ==========================================

base = Path.home() / "kerala_project/data"

# STEP 1: Load daily ERA5 wind and humidity

with xr.open_dataset(
    base / "era5/ua_700hPa_daily_JJAS2020_landonly.nc"
) as ds:
    u = ds["ua"].load()

with xr.open_dataset(
    base / "era5/va_700hPa_daily_JJAS2020_landonly.nc"
) as ds:
    v = ds["va"].load()

with xr.open_dataset(
    base / "era5/q_700hPa_daily_JJAS2020_landonly.nc"
) as ds:
    q = ds["q"].load()

# STEP 2: Load terrain gradients

with xr.open_dataset(
    base / "srtm/srtm_gradients_landonly_era5grid.nc"
) as ds:
    dh_dx = ds["dh_dx"].load()
    dh_dy = ds["dh_dy"].load()

# STEP 3: Check calendar dates

u_dates = u.time.values.astype("datetime64[D]")
v_dates = v.time.values.astype("datetime64[D]")
q_dates = q.time.values.astype("datetime64[D]")

if not (
    np.array_equal(u_dates, v_dates)
    and np.array_equal(u_dates, q_dates)
):
    raise ValueError("Calendar dates do not match!")

# Daily statistics represent matching calendar days.
# Assign common time labels without changing the values.

q = q.assign_coords(time=u.time)

# STEP 4: Check exact coordinate alignment

u, v, q, dh_dx, dh_dy = xr.align(
    u, v, q, dh_dx, dh_dy, join="exact"
)

# Make dimension order consistent

u = u.transpose("time", "lat", "lon")
v = v.transpose("time", "lat", "lon")
q = q.transpose("time", "lat", "lon")

dh_dx = dh_dx.transpose("lat", "lon")
dh_dy = dh_dy.transpose("lat", "lon")

print("Coordinates aligned successfully!")
print("Wind shape:", u.shape)
print("Humidity shape:", q.shape)

# STEP 5: Orographic vertical-motion proxy

w_oro = u * dh_dx + v * dh_dy

# STEP 6: Terrain slope magnitude

slope = np.hypot(dh_dx, dh_dy)

# STEP 7: Upslope wind component

v_upslope = xr.where(
    slope > 1e-6,
    w_oro / slope,
    np.nan
)

# STEP 8: Moisture-weighted horizontal wind

q_u = q * u
q_v = q * v

# STEP 9: Positive moist-upslope index

moist_upslope = q * w_oro.clip(min=0)

# STEP 10: Create calculated dataset

calculated = xr.Dataset({
    "w_oro": w_oro,
    "v_upslope": v_upslope,
    "q_u": q_u,
    "q_v": q_v,
    "moist_upslope": moist_upslope,
})

# STEP 11: Load original results

with xr.open_dataset(
    base / "derived/orographic_moisture_JJAS2020.nc"
) as ds:
    previous = ds.load()

# Confirm coordinates agree
calculated, previous = xr.align(
    calculated, previous, join="exact"
)

# STEP 12: Verify all five variables

print("\nComparison with previous results:")

for variable in calculated.data_vars:

    old = previous[variable]

    # Ensure identical dimension order
    new = calculated[variable].transpose(*old.dims)

    matches = np.allclose(
        new.values,
        old.values,
        rtol=1e-6,
        atol=1e-9,
        equal_nan=True
    )

    if matches:
        print(f"{variable}: MATCH")
    else:
        print(f"{variable}: DIFFERENT")

# STEP 13: Print summary statistics

print("\nNumber of days:", w_oro.sizes["time"])

print(
    "Mean orographic forcing:",
    float(w_oro.mean()),
    "m/s"
)

print(
    "Mean moist-upslope index:",
    float(moist_upslope.mean()),
    "m/s"
)

print("\nVerification completed!")
