ERA5 Land-Only Winds — Kerala and Western Ghats (JJAS 2020)
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

This folder contains scripts and data processing files
related to land masking for the Kerala monsoon
orographic rainfall project.

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
