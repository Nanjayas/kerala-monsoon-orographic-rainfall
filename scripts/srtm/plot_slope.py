from pathlib import Path
import rasterio
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Project paths
project = Path.home() / "kerala_project"

input_file = project / "data/srtm/srtm_kerala_slope_preview.tif"
output_file = project / "srtm_kerala_slope.png"

# Read slope raster
with rasterio.open(input_file) as src:
    slope = src.read(1, masked=True)
    bounds = src.bounds

# Create figure
plt.figure(figsize=(9, 7))

plt.imshow(
    slope,
    extent=[
        bounds.left,
        bounds.right,
        bounds.bottom,
        bounds.top
    ],
    origin="upper",
    cmap="YlOrRd",
    vmin=0
)

plt.colorbar(label="Terrain slope (degrees)")
plt.xlabel("UTM Easting (m)")
plt.ylabel("UTM Northing (m)")
plt.title("SRTM Terrain Slope — Kerala and Western Ghats")

plt.savefig(output_file, dpi=200, bbox_inches="tight")
plt.close()

print("Slope map saved to:", output_file)
print("Maximum slope:", slope.max(), "degrees")
print("Mean slope:", slope.mean(), "degrees")
