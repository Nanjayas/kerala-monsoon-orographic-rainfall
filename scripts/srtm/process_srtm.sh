
#!/bin/bash
set -euo pipefail

# SRTM processing for Kerala and the Western Ghats
# Input: NASA SRTMGL1_NC V003 NetCDF tiles
# Study region: 72–79 E, 7–14 N

cd ~/kerala_project/data/srtm

# 1. Combine individual NetCDF tiles into a virtual mosaic
gdalbuildvrt -overwrite srtm_westernghats.vrt ./*.nc

# 2. Crop the study region and create a 0.01-degree preview
gdalwarp \
  -overwrite \
  -te 72 7 79 14 \
  -tr 0.01 0.01 \
  -r average \
  -srcnodata -32768 \
  -dstnodata -9999 \
  -co COMPRESS=LZW \
  srtm_westernghats.vrt \
  srtm_kerala_preview.tif

# 3. Reproject to UTM Zone 43N with 1-km grid spacing
gdalwarp \
  -overwrite \
  -t_srs EPSG:32643 \
  -tr 1000 1000 \
  -r bilinear \
  -srcnodata -9999 \
  -dstnodata -9999 \
  srtm_kerala_preview.tif \
  srtm_kerala_utm_preview.tif

# 4. Calculate terrain slope in degrees
gdaldem slope \
  srtm_kerala_utm_preview.tif \
  srtm_kerala_slope_preview.tif \
  -of GTiff \
  -co COMPRESS=LZW

echo "SRTM preprocessing completed."
