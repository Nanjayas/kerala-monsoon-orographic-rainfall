from pathlib import Path
import rasterio
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Define project paths
project = Path.home() / "kerala_project"

input_file = project / "data/srtm/srtm_kerala_preview.tif"
output_file = project / "srtm_kerala_elevation.png"

# Read elevation data
with rasterio.open(input_file) as src:
    elevation = src.read(1, masked=True)
    bounds = src.bounds

# Create figure
plt.figure(figsize=(9, 7))

plt.imshow(
    elevation,
    extent=[bounds.left, bounds.right,
            bounds.bottom, bounds.top],
    origin="upper",
    cmap="terrain"
)

plt.colorbar(label="Elevation above sea level (m)")

plt.xlabel("Longitude (°E)")
plt.ylabel("Latitude (°N)")
plt.title("SRTM Elevation — Kerala and Western Ghats")

plt.savefig(output_file, dpi=200, bbox_inches="tight")
plt.close()

print("Elevation map saved to:", output_file)
