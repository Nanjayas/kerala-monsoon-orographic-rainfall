
from pathlib import Path
import numpy as np
import xarray as xr

base = Path.home() / "kerala_project/data"


def load_variable(filename, variable=None):
    """Load scientific data, ignoring coordinate-boundary variables."""

    with xr.open_dataset(base / filename) as ds:

        if variable is None:
            candidates = [
                name for name in ds.data_vars
                if not name.endswith(("_bnds", "_bounds"))
                and name not in ("crs", "spatial_ref")
            ]

            if len(candidates) != 1:
                raise ValueError(
                    f"Cannot select variable in {filename}: "
                    f"{candidates}"
                )

            variable = candidates[0]

        return ds[variable].load()

# Load the actual land-fraction variable
land_fraction_or_mask = load_variable(
    "common_grid/land_mask_kerala.nc",
    "sftlf"
).squeeze(drop=True)

# Check whether land fraction is stored as 0-1 or 0-100
print("Land fraction units:",
      land_fraction_or_mask.attrs.get("units", "unknown"))

maximum = float(land_fraction_or_mask.max())
print("Maximum land fraction:", maximum)

# Create the land mask using the appropriate threshold
if maximum <= 1.0:
    land_mask = land_fraction_or_mask > 0.5
else:
    land_mask = land_fraction_or_mask > 50.0
print("Land cells:", int(land_mask.sum()))
print("Total cells:", land_mask.size)

if land_mask.size != 625 or int(land_mask.sum()) != 225:
    raise ValueError("Unexpected land mask: inspect its contents!")


# 2. Compare a newly masked variable with our saved result
def verify_masking(original_path, saved_path, saved_var=None):
    original = load_variable(original_path)
    saved = load_variable(saved_path, saved_var)

    # Check exact coordinate alignment
    original, saved, mask = xr.align(
        original, saved, land_mask, join="exact"
    )

    # Apply mask: land retained, ocean set to NaN
    calculated = original.where(mask)

    # Put dimensions in the same order before comparing
    calculated = calculated.transpose(*saved.dims)

    matches = np.allclose(
        calculated.values,
        saved.values,
        rtol=1e-6,
        atol=1e-9,
        equal_nan=True
    )

    print(
        f"{saved_path}: "
        f"{'MATCH' if matches else 'DIFFERENT'}"
    )


# 3. Verify ERA5 variables
print("\nERA5 LAND MASK VERIFICATION")

verify_masking(
    "era5/ua_700hPa_daily_JJAS2020.nc",
    "era5/ua_700hPa_daily_JJAS2020_landonly.nc"
)

verify_masking(
    "era5/va_700hPa_daily_JJAS2020.nc",
    "era5/va_700hPa_daily_JJAS2020_landonly.nc"
)

verify_masking(
    "era5/q_700hPa_daily_JJAS2020_era5grid.nc",
    "era5/q_700hPa_daily_JJAS2020_landonly.nc"
)


# 4. Verify SRTM elevation
print("\nSRTM LAND MASK VERIFICATION")

verify_masking(
    "srtm/srtm_elevation_era5grid.nc",
    "srtm/srtm_elevation_landonly_era5grid.nc"
)


# 5. Verify SRTM terrain gradients
verify_masking(
    "srtm/srtm_gradient_x_era5grid.nc",
    "srtm/srtm_gradients_landonly_era5grid.nc",
    "dh_dx"
)

verify_masking(
    "srtm/srtm_gradient_y_era5grid.nc",
    "srtm/srtm_gradients_landonly_era5grid.nc",
    "dh_dy"
)

print("\nLand-masking verification completed.")
