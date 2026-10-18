# Scientific Methodology

## 1. Project Title

**Quantifying the Orographic and Atmospheric Controls of Southwest Monsoon Rainfall over Kerala Using Satellite and Reanalysis Data**

## 2. Scientific Objective

To investigate how the Western Ghats' topography and atmospheric conditions influence the spatial and temporal distribution of southwest monsoon rainfall over Kerala.

The analysis will combine atmospheric reanalysis, satellite precipitation observations, and digital elevation data.

## 3. Study Region

- **Region:** Kerala, the Western Ghats, and surrounding Arabian Sea
- **Initial longitude range:** 72°E–79°E
- **Initial latitude range:** 7°N–14°N
- **Study period:**&#x20;
- **Monsoon season:** June–September (JJAS)
- **Initial processing and validation period:** 2020

### Terrain Characteristics

The Western Ghats form a major topographic barrier along India's western coast.

- Many mountain areas have elevations of approximately 600–1,500 m.
- The highest peak in Kerala, Anamudi, reaches approximately 2,695 m above mean sea level.
- Actual terrain elevation, slope, and topographic variability across the selected domain will be calculated using SRTM data.

Moisture-bearing monsoon winds approaching from the Arabian Sea can be forced upward along the western slopes. Rising air may cool, promoting condensation and precipitation under suitable atmospheric conditions.

Terrain height alone does not determine rainfall; moisture availability, atmospheric stability, wind direction, and circulation patterns also influence precipitation.

## 4. Datasets

### ERA5 — Atmospheric Reanalysis

Planned atmospheric variables:

- Eastward wind component (`ua`)
- Northward wind component (`va`)
- Atmospheric moisture, subject to verification of available humidity variables

### GPM IMERG — Precipitation

Satellite-derived precipitation data will be used to examine rainfall distribution and compare atmospheric conditions with observed precipitation estimates.

### SRTM — Terrain Elevation

Digital elevation data will be used to derive:

- Mean elevation
- Terrain slope
- Terrain variability
- Orographic gradients

## 5. Selection of Atmospheric Pressure Levels

### Importance of 700 hPa

The 700 hPa pressure level corresponds to an approximate altitude of 3 km above mean sea level, although its actual geopotential height varies with atmospheric conditions.

This level was selected for the initial investigation because:

1. The Western Ghats contain high terrain approaching 2.7 km.
2. The 700 hPa surface generally lies above this terrain.
3. It enables analysis of wind circulation over the mountain region with fewer below-ground values than lower pressure levels.
4. It provides information about lower-to-middle-tropospheric circulation that may influence orographic precipitation.

### Why also consider 850 hPa?

The 850 hPa level lies at approximately 1.5 km above sea level under typical conditions.

It is especially relevant for examining lower-tropospheric monsoon winds and moisture transport.

However, portions of the Western Ghats extend above this pressure surface, so some ERA5 values may represent below-ground levels or otherwise require terrain-aware interpretation.

The study will assess whether additional pressure levels, including 850 hPa, are required for a physically complete analysis.

**The initial use of 700 hPa is a practical methodological choice, not a claim that this level alone explains monsoon rainfall.**

## 6. Initial ERA5 Processing — June 2020

Completed steps:

1. Accessed the institutional ERA5 archive at FU Berlin.
2. Identified the hourly eastward wind field at 700 hPa.
3. Selected the study region using Climate Data Operators (CDO).
4. Inspected the Gaussian spatial grid.
5. Opened the resulting NetCDF file using Python and xarray.
6. Computed the monthly mean eastward wind component.
7. Generated an exploratory spatial map.

The June 2020 subset contains 720 hourly timesteps on a 25 × 25 regional grid.

## 7. Spatial and Temporal Harmonisation

ERA5, GPM IMERG, and SRTM have different native spatial grids and resolutions.

The initial proposed target is a regular 0.25° latitude–longitude grid, subject to validation.

Planned processing:

- Regrid ERA5 atmospheric fields using a suitable interpolation method.
- Aggregate or conservatively remap GPM precipitation with appropriate treatment of precipitation units.
- Aggregate fine-resolution SRTM elevations and derived terrain characteristics.
- Align atmospheric and precipitation data to a common daily time resolution.
- Verify coordinate systems, missing values, units, spatial boundaries, and temporal coverage.

The high-resolution SRTM terrain dataset will also be retained separately for terrain analysis.

## 8. Initial 2020 Workflow

1. Extract ERA5 eastward and northward wind components.
2. Identify and extract suitable atmospheric moisture variables.
3. Obtain GPM IMERG precipitation for the study region.
4. Obtain and process SRTM elevation.
5. Construct and validate the common spatial grid.
6. Harmonise datasets and generate comparison maps.
7. Create a reproducible Python processing workflow.

After validating the 2020 workflow, the analysis will be extended to the full 20...-2025 monsoon period.

## 9. Expected Scientific Analysis

Potential analyses include:

- Relationships between rainfall and terrain elevation
- Orographic rainfall gradients
- Relationships between wind direction, wind speed, and rainfall
- Atmospheric moisture availability and precipitation
- Spatial and temporal variations in monsoon rainfall

Any observed correlations will be interpreted cautiously and will not, by themselves, establish causation.

## 10. Project Status

**Completed:** ERA5 700 hPa eastward wind extraction and exploratory mapping for June 2020.

**Current focus:** Preparation and spatial harmonisation of ERA5, GPM, and SRTM datasets for the 2020 southwest monsoon.

