
from pathlib import Path
import xarray as xr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Project paths
folder = Path.home() / "kerala_project/data/srtm"

input_file = folder / "srtm_elevation_era5grid.nc"
output_file = folder / "srtm_coverage_era5grid.png"

# Open regridded SRTM data
ds = xr.open_dataset(input_file)

# Automatically identify the elevation variable
variable = next(iter(ds.data_vars))
elevation = ds[variable].squeeze(drop=True)

# 1 = valid elevation, 0 = missing elevation
coverage = elevation.notnull().astype(int)

print("Total cells:", coverage.size)
print("Valid cells:", int(coverage.sum()))
print("Missing cells:", int((coverage == 0).sum()))

# Plot spatial coverage
plt.figure(figsize=(8, 6))

coverage.plot(
    x="lon",
    y="lat",
    cmap="viridis",
    vmin=0,
    vmax=1,
    cbar_kwargs={"label": "0 = Missing, 1 = Valid"}
)

plt.title("SRTM Coverage on ERA5 Grid — Kerala")
plt.savefig(output_file, dpi=200, bbox_inches="tight")
plt.close()

print("Coverage map saved to:", output_file)
