# ERA5 Near-Surface Moisture Processing (JJAS 2020)

Script: `doc/script/era5/tdps_map.py`. Output map: `docs/figures/era5/tdps_jjas2020_mean.png`.

This file complements the main `doc/methodology.md`. Harmonisation with IMERG is documented in `doc/methodology_harmonisation.md`.

## Data
| Item | Detail |
|---|---|
| Dataset | ERA5 reanalysis, daily means (university archive) |
| Variable | `tdps`, 2 m dew point temperature (K in the file) |
| Path | `/daten/erafive/arch/data/dkrz-sync/ERA5/day/atmos/tdps/r1i1p1/` |
| Grid | Gaussian, about 0.28° (global 1280 x 640) |
| Domain | 72-79°E, 7-14°N (25 x 25 grid points) |
| Period | 1 June - 30 September 2020 (122 days) |
| Time stamp | 12:00 UTC (marks the daily mean) |

## Method
1. Located `tdps` in the daily ERA5 archive. Daily specific humidity (`hus`) and total column water vapour (`prw`) were not found there.
2. Opened the 2020 yearly file with xarray (data stays on the server).
3. Selected JJAS 2020 and the study box (grid points whose centres lie inside the box).
4. Converted from Kelvin to °C (subtract 273.15).
5. Averaged over the 122 days to get the mean seasonal pattern, and plotted it.

## Why dew point
The dew point is essentially set by the amount of water vapour in the air, not by the air temperature, so it measures moisture better than relative humidity. It could be converted to specific humidity, which also needs the surface pressure.

## Result
The seasonal mean dew point of the grid cells ranges from about 17.9 to 25.4 °C. It is uniformly high (about 24-25 °C) over the Arabian Sea and along the coast, and lower (about 19-22 °C) over the interior in the north-east. Local minima over high ground (for example near 11.3°N, 76.6°E) probably reflect the height of the surface. The dew point shows the same west-east contrast as the rainfall, but it is almost flat over the sea while rainfall peaks near the coast, so near-surface moisture alone does not explain where the rain falls.

## Limitations
- `tdps` is measured 2 m above the model surface, not at a fixed height above sea level. Over mountains it is cooler and drier because the surface is higher, so it mixes moisture with terrain height.
- It is a surface variable and only a proxy for the moisture carried at 925-850 hPa. It is also not at the same level as the 700 hPa wind.
- ERA5 cells are about 31 km wide and the model terrain is smoothed, so narrow ridges are not resolved.
- Only one season (2020) has been processed so far.

## Next steps
- Check for pressure-level humidity (for example in the hourly archive) to calculate moisture flux.
- Plot the ERA5 orography next to the dew point to test the height explanation.
- Extend to more years.
