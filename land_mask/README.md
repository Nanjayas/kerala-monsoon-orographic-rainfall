This folder contains scripts and data processing files
related to land masking for the Kerala monsoon
orographic rainfall project.


# 1. ERA5 Land-Only Winds — Kerala and Western Ghats (JJAS 2020)
Overview
This dataset contains daily mean ERA5 horizontal wind components at 700 hPa for June–September (JJAS) 2020 over the Kerala–Western Ghats study region. The winds have been masked to retain predominantly land-covered grid cells for comparison with SRTM terrain elevation and gradients.

The purpose of this preprocessing step is to align atmospheric circulation data with the land-based terrain analysis. It is not a rainfall prediction or an estimate of surface wind.
Data source and study domain
- Source: ERA5 reanalysis, accessed through the Freie Universität Berlin Institute of Meteorology data archive.
- Variables: ua (eastward wind, u) and va (northward wind, v).
- Pressure level: 700 hPa.
- Period: 1 June–30 September 2020 (122 daily time steps).
- Units: m/s.
- Regional bounds requested: 72–79°E, 7–14°N.
- Working grid: 25 × 25 Gaussian latitude–longitude grid (625 cells), with longitude centers from 72°E to 78.75°E and latitude centers approximately 7.166°N to 13.911°N.
Files
File	Contents
ua_700hPa_daily_JJAS2020_landonly.nc	Land-masked daily eastward wind (ua)
va_700hPa_daily_JJAS2020_landonly.nc	Land-masked daily northward wind (va)
ua_700hPa_daily_JJAS2020.nc	Unmasked daily eastward wind, retained as an intermediate dataset
va_700hPa_daily_JJAS2020.nc	Unmasked daily northward wind, retained as an intermediate dataset
../common_grid/land_mask_kerala.nc	Binary land mask (1 = predominantly land; 0 = otherwise)


These paths are relative to the data/era5/ directory in the working project. The original monthly wind data were preserved.
Processing workflow
1. Extract the regional 700-hPa ua and va fields from the ERA5 archive.
2. Calculate daily means from the original hourly wind data.
3. Merge the four monthly daily-mean files for June, July, August, and September into separate 122-day files for ua and va using CDO mergetime.
4. Obtain ERA5 land-area fraction (sftlf) from the institute archive, on the same Gaussian grid.
5. Create a binary mask where sftlf > 50%. The original fraction is stored in percent, not on a 0–1 scale.
6. Apply that mask to each daily wind field with xarray (wind.where(mask == 1)), storing excluded cells as missing values (NaN). Save new files without overwriting the unmasked datasets.
Land-mask result
Grid-cell classification	Number of cells
Total	625
Predominantly land (sftlf > 50%)	225
Excluded (sftlf <= 50%)	400


The expected number of valid values per wind component is 122 × 225 = 27,450, assuming that none of the selected land cells has missing wind data. This count should be verified from each saved file.
Initial wind characteristics
The plotting workflow calculated these spatially unweighted averages of the JJAS 2020 mean wind components over the retained land cells:
- Mean eastward wind, u: approximately +7.22 m/s.
- Mean northward wind, v: approximately −0.54 m/s.
The positive u indicates predominantly eastward (westerly) flow in this regional mean. The slightly negative v indicates a comparatively small southward component. Individual days and locations can differ from these averages.
Visualization
The land-only ERA5 wind figure displays:
- Background shading: magnitude of the JJAS-mean horizontal wind vector, sqrt(mean(u)^2 + mean(v)^2) (m/s).
- Arrows: direction and relative strength of the JJAS-mean horizontal wind.
- Blank cells: excluded by the land mask.# Land Masking

  Scientific interpretation and limitations
- 700 hPa is an atmospheric pressure level, not a measurement of near-surface wind. Winds at this level should not automatically be interpreted as flow following local slopes.
- The mask is used to support land-based statistical comparisons. Excluded offshore winds remain relevant for understanding Arabian Sea moisture transport and should be retained in the unmasked files.
- The domain includes land outside Kerala; the 225 selected cells are not a Kerala-only administrative boundary.
- The 50% land-fraction threshold can exclude partially coastal cells; it is a documented methodological choice rather than an exact coastline.
- Winds alone cannot explain rainfall. Subsequent analyses will incorporate specific humidity, terrain gradients, and GPM IMERG precipitation.
Next steps
1. Check that ERA5 wind, specific-humidity, and terrain grids and timestamps align exactly.
2. Integrate GPM IMERG precipitation on the common grid.
3. Examine circulation, moisture availability, and terrain-related uplift in relation to observed rainfall, while noting the limitations of using 700-hPa winds for terrain-following ascent.

  
---

# 2. GPM IMERG rainfall: land masking (JJAS 2020)

## Overview
This section describes the land masking of the harmonised GPM IMERG rainfall (daily, JJAS 2020), which is already on the ERA5 grid (see `harmonisation/README.md`). Ocean cells are set to missing values (NaN) so that rainfall can be compared with the land-based terrain and the land-masked ERA5 fields.

This is a preprocessing step. It does not change the rainfall values over land.

## Files
| File | Contents |
|---|---|
| `land_mask/landmask_gpm.ipynb` | Notebook: loads the mask, checks the grid, applies the mask, plots the land-only total |
| `landonly/gpm_land_only_jjas2020_total.png` | Land-only JJAS 2020 total rainfall map (mm) |
| `data/processed/harmonised_rain_tdps_jjas2020.nc` | Input: harmonised rainfall (`rain`, mm/day), stored locally, not in Git |
| `land_mask_kerala.nc` | Binary land mask (1 = land, 0 = otherwise), stored locally, not in Git |
| `rain_land_jjas2020.nc` | Output: land-masked rainfall (`rain`, mm/day), stored locally, not in Git |

## Method
1. **Land fraction.** The ERA5 land-sea mask was taken from the university archive (`sf_c172_n320.nc`, variable `var172`, which is the ERA5 land-sea mask) and cut to 72-79°E, 7-14°N with CDO (`sellonlatbox`). It is on the same 0.28125° grid as the harmonised rainfall.
2. **Threshold.** A cell counts as land if its land fraction is above 0.5. In this file the fraction runs from 0 to 1, so `> 0.5` is the same rule as `sftlf > 50%` used for the ERA5 wind mask. The binary mask was made with `cdo gtc,0.5`.
3. **Mask check.** The mask has 625 cells, of which 225 are land and 400 are excluded. This is the same count as the ERA5 wind land mask.
4. **Grid check.** The mask and the rainfall have identical latitudes and longitudes (25 x 25) and are the same length in time (122 days).
5. **Apply.** `rain.where(mask == 1)` keeps rainfall over land and stores ocean cells as NaN. The grid is not cropped, so it still lines up with the other ERA5 fields.
6. **Seasonal total.** The total is the sum over the 122 days, computed with `skipna=False` so that ocean cells stay blank instead of showing as 0 mm.

## Checks
- Valid values per day: 225.
- Valid values in total: 122 x 225 = 27,450 (confirmed from the saved file).

## Result
The land-only total keeps the pattern of the full-grid map. The wettest cells lie along the windward slopes of the Western Ghats (about 3,500 mm at roughly 13-14°N, 74.5-75°E), and rainfall falls steeply towards the east. The Arabian Sea and the Gulf of Mannar (bottom-right corner of the box) are blank.

## Limitations
- The 50% threshold excludes partly coastal cells. Part of the heaviest coastal rainfall (north-west of the box, about 74-75°E, 13.5-14°N) is therefore masked out. Cells are about 31 km wide, so the coastline is only approximate.
- The 225 selected cells are not a Kerala-only administrative boundary. They include land outside Kerala.
- The same rule is used for the ERA5 wind mask, so rainfall and winds cover identical cells. If the threshold is changed, both masks have to be changed.
- Ocean rainfall is relevant for the moisture supply from the Arabian Sea, so the unmasked harmonised file is kept.
- IMERG is a satellite estimate and may underestimate rainfall over steep terrain.
- Only one season (2020) has been processed.

## Next steps
- Add SRTM elevation on the same land cells.
- Relate land-only rainfall to elevation and the ERA5 variables.
- Check whether a lower threshold (to keep more coastal cells) changes the results.

- SRTM Topography — Land-Only Elevation and Terrain Gradients
Kerala and Western Ghats Southwest Monsoon Project | JJAS 2020 pilot study

This folder documents the preparation of SRTM-derived topography for the Kerala–Western Ghats study area. Elevation and terrain-gradient fields were harmonized to the regional ERA5 grid and then restricted to predominantly land-covered cells. They are intended for comparison with ERA5 winds, specific humidity, and, in a later step, GPM IMERG precipitation.
Status: Elevation and both terrain-gradient components have been processed, land-masked, checked for missing land values, and plotted. Rainfall–orography relationships have not yet been evaluated.

1. Study area and target grid
Property	Value
Study region	72–79°E, 7–14°N (Kerala, Western Ghats and surrounding area)
Target grid	Regional ERA5 Gaussian latitude–longitude grid
Grid dimensions	25 × 25 = 625 cells
Longitude centers	72.0°E to 78.75°E, in 0.28125° increments
Latitude centers	Approximately 7.166°N to 13.911°N (Gaussian spacing)
Land selection	ERA5 sftlf > 50%
Predominantly land cells	225
Excluded cells	400 (predominantly ocean, by the land-fraction rule)


The final files retain the 25 × 25 rectangular grid; excluded cells are represented as missing (NaN) rather than cropped away. The study area includes neighboring land and is not a Kerala administrative-boundary mask.
2. Source data
Topography: NASA Shuttle Radar Topography Mission (SRTM), SRTMGL1_NC Version 003, approximately 1 arc-second (~30 m nominal sampling). The processing started from 47 downloaded NetCDF elevation tiles covering the region. The SRTM data were mosaicked and processed using GDAL, CDO, Python, NumPy and xarray.

Land fraction: The institute's fixed ERA5 land-area fraction field, sftlf, with units of percent (%). Cells were retained when more than half of the grid-cell area was classified as land. The land-mask file used in this workflow was data/common_grid/land_mask_kerala.nc.

ERA5 reference grid: The regional 700-hPa ERA5 wind dataset provided the 25 × 25 target grid for regridding terrain fields.
3. Processing workflow
1. Mosaic and inspect SRTM tiles. The original SRTM tiles were combined to cover 72–79°E and 7–14°N. A high-resolution elevation mosaic was inspected for valid elevations and missing areas.
2. Harmonize elevation. The SRTM elevation was aggregated/remapped to the regional ERA5 Gaussian grid, producing srtm_elevation_era5grid.nc.
3. Calculate geographic terrain gradients. Eastward and northward partial derivatives were calculated from the ERA5-scale elevation field using NumPy finite differences and geographic distance conversion. The result was saved as srtm_gradients_era5scale.nc.
4. Construct the land mask. The static ERA5 sftlf field was extracted to the study area, and grid cells with sftlf > 50% were assigned a value of 1. Other cells were assigned 0.
5. Verify grid compatibility. The elevation and land-mask grids were checked to have identical Gaussian grid centers, cell bounds, and 25 × 25 dimensions.
6. Apply the land mask without altering originals. Elevation and gradients were kept only where the mask equals 1; masked outputs were saved separately.
7. Validate and plot. Counts of valid land elevations and gradients were checked before creating the land-only figures.
Geographic gradient definitions
Let \(h(\lambda,\phi)\) denote elevation in metres, where \(\lambda\) and \(\phi\) are longitude and latitude in radians. For Earth radius \(R\), the approximate eastward and northward terrain gradients on a geographic grid are
\[
\frac{\partial h}{\partial x}=\frac{1}{R\cos\phi}\frac{\partial h}{\partial\lambda},
\qquad
\frac{\partial h}{\partial y}=\frac{1}{R}\frac{\partial h}{\partial\phi}.
\]
The numerical derivatives were estimated with numpy.gradient, using the actual latitude and longitude coordinate values. Both components have units of m/m (dimensionless height change per unit horizontal distance):
- dh_dx > 0: terrain rises toward the east.
- dh_dx < 0: terrain falls toward the east.
- dh_dy > 0: terrain rises toward the north.
- dh_dy < 0: terrain falls toward the north.
These coarse-grid derivatives describe terrain variation at the ERA5-grid scale, not the original 30-m SRTM scale. Separate preliminary fine-scale gradient products also exist, but they should not be confused with these east/north derivatives without checking their projection and directional definitions.
4. Land-only datasets
The following filenames describe outputs on the FU server relative to the project directory ~/kerala_project/.
File	Variable	Description
data/common_grid/land_mask_kerala.nc	sftlf (binary after thresholding)	1 for land fraction > 50%, otherwise 0
data/srtm/srtm_elevation_landonly_era5grid.nc	Band1	Land-only elevation (m)
data/srtm/srtm_gradients_landonly_era5grid.nc	dh_dx, dh_dy	Land-only eastward and northward elevation gradients (m/m)


Upstream/intermediate products retained: data/srtm/srtm_elevation_era5grid.nc and data/srtm/srtm_gradients_era5scale.nc. Original SRTM tiles and other higher-resolution intermediates were not overwritten.
The table describes local scientific data files. They may not all be committed to GitHub, depending on the repository's data-storage policy and .gitignore configuration.

5. Quality-control results
Check	Result
Total ERA5 grid cells	625
Land cells under sftlf > 50%	225
Valid SRTM elevation values on land	225 / 225
Missing SRTM elevation values on land	0
Valid dh_dx values on land	225 / 225
Valid dh_dy values on land	225 / 225
Cells with both gradients valid on land	225 / 225


For the land-only elevation field, the values printed during plotting were:
Statistic	Elevation
Minimum	7 m
Maximum	1,581 m
Mean across the 225 selected cells	502.14 m


Before masking, the 25 × 25 harmonized elevation field had 195 missing cells across the full geographic box. None of those missing values fell within the 225 selected land cells. This does not imply full original-SRTM coverage everywhere in the broader domain, and the maximum on the coarse grid is not the highest individual mountain summit.
6. Figures and interpretation
The land-only plots produced during processing include:
- Elevation map: data/srtm/srtm_elevation_landonly_era5grid.png — spatial distribution of terrain height over the selected land region.
- Two-panel gradient figure: data/srtm/srtm_gradients_landonly_era5grid.png — eastward (dh_dx) and northward (dh_dy) gradients, displayed with a zero-centered diverging color scale.
Other gradient figures were also saved in the project's plotting workflow. Check the actual filenames in figures/ or data/srtm/ before constructing relative Markdown image links in GitHub.

Initial interpretation: Low terrain appears near the western coast, with higher terrain farther inland, consistent with the Western Ghats. The gradient maps indicate where elevation changes with eastward or northward displacement; they do not, by themselves, measure upward atmospheric motion or rainfall.
7. Why gradients are useful for the monsoon study
A simplified directional measure of terrain-forced vertical motion is
\[
w_{\mathrm{oro}}\approx u\frac{\partial h}{\partial x}
+v\frac{\partial h}{\partial y},
\]
where \(u\) and \(v\) are the eastward and northward wind components (m/s), and \(\partial h/\partial x\), \(\partial h/\partial y\) are the dimensionless terrain gradients.

A positive value indicates air flowing toward rising terrain under this simplified kinematic approximation. It is not an observation of vertical wind, and using ERA5 winds at 700 hPa involves a substantial physical limitation: winds aloft may not represent the near-surface flow deflected upward by the mountains. Moisture, atmospheric stability, flow blocking and precipitation dynamics must be considered before interpreting rainfall effects.
9. Limitations and next steps
- Spatial representativeness: A 25 × 25 regional grid smooths narrow valleys, sharp ridgelines and individual summits. The grid-cell mean elevation is not point elevation.
- Land selection: The >50% rule excludes predominantly ocean cells, including some mixed coastal cells. It is not a precise coastline or state-boundary delineation.
- Differentiation near boundaries: Coarse gradients can be sensitive to coastline treatment and missing neighbors. The 225 selected land cells passed the missing-value check, but derivative quality still deserves assessment.
- Wind–terrain interpretation: 700-hPa ERA5 winds should not automatically be interpreted as boundary-layer or slope-following winds.
- Pending analysis: Combine these fields with the already prepared daily ERA5 ua, va and specific humidity q; incorporate GPM IMERG daily rainfall once harmonized; test associations rather than assume causation.
10. Data acknowledgement
- SRTM: NASA Shuttle Radar Topography Mission, SRTMGL1_NC Version 003 (via NASA Earthdata / LP DAAC).
- ERA5 land fraction and target wind grid: ECMWF ERA5 data accessed through the Freie Universität Berlin Institute of Meteorology archive.
- Tools: GDAL, Climate Data Operators (CDO), Python, NumPy, xarray and Matplotlib.
