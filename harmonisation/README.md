# 1. Harmonisation of GPM IMERG rainfall onto the ERA5 grid (JJAS 2020)

Notebook: `harmonisation/scripts/grid_harmoniasation_gpm.ipynb`. Figure: `figures/harmonized/harmonised_gpm_tdps_jjas2020.png`.

## Purpose
IMERG rainfall and ERA5 fields come on different grids and with different time stamps. To relate rainfall to atmospheric variables, each grid cell needs a rainfall value and an atmospheric value for the same day. This step puts IMERG on the ERA5 grid.

## Inputs
| | GPM IMERG V07 Final Run (daily) | ERA5 (daily, university archive) |
|---|---|---|
| Variable | `precipitation` (mm/day) | `tdps`, used here only to provide the grid and dates |
| Grid | regular, 0.1° (about 11 km), 70 x 70 | Gaussian, 0.28125° (about 31 km), 25 x 25 |
| Dimension order | time, lon, lat | time, lat, lon |
| Time stamp | 00:00 UTC | 12:00 UTC (marks the daily mean) |
| Domain | 72-79°E, 7-14°N | 72-79°E, 7-14°N |
| Period | 1 June - 30 September 2020 (122 days) | same |

## Method
1. **Same domain.** Both datasets are cut to 72-79°E, 7-14°N. No new download was needed, because the raw IMERG files are global.
2. **Same dimension order.** IMERG was reordered to (time, lat, lon), as in ERA5.
3. **Same dates.** The ERA5 time stamps were reduced from 12:00 to the date. Both products describe the same UTC day, so only the label differed.
4. **Common grid: the ERA5 grid.** IMERG is finer, so it is averaged down. Interpolating ERA5 up to 0.1° would look sharper but add no information.
5. **Cell edges.** ERA5 latitudes are not exactly evenly spaced (Gaussian grid), so the edges of each cell were taken as the midpoints between neighbouring grid points.
6. **Averaging, not interpolation.** Rainfall is an amount over an area, so each ERA5 cell takes the mean of the IMERG cells inside it (about 8 per cell). Units stay mm/day.

## Checks
- Rain and the ERA5 field both have shape (122, 25, 25), with identical dates.
- Mean rainfall changed from 10.49 to 10.65 mm/day (about +1.5%).

## Result
The harmonised seasonal total keeps the pattern of the native map: a wet strip along the coast and windward slopes (about 3,500 mm at roughly 12-14°N, 74-75.5°E, which is north of Kerala), a steep drop to the east, and the driest area (below 500 mm) in the south-east corner. The maximum falls from about 4,000 mm (native) to about 3,600 mm, because the narrow wet strip is averaged with drier neighbours.

## Limitations
- Averaging by cell edges is an approximation of exact area weighting. The outer ERA5 cells extend slightly beyond the IMERG box and are averaged from fewer cells, which explains the 1.5% shift. A tool such as xESMF would be more exact.
- Detail is lost: rainfall is represented at about 31 km instead of 11 km, which matters for narrow orographic features such as the Ghats.
- The 0.1° IMERG grid is finer than the true resolution of the underlying satellite measurements.
- IMERG is a satellite estimate and may underestimate rainfall over steep terrain.
- Only one season (2020) has been processed.
- The common grid (ERA5 native, about 0.28°) differs from the regular 0.25° proposed in `doc/methodology.md`, and still has to be agreed with the project partner.
- Descriptive only: no correlation or regression has been run yet.

## Output
`data/processed/harmonised_rain_tdps_jjas2020.nc` (variables `rain` in mm/day and `tdps` in °C), stored locally and not in Git.

## Land masking (done)
The sea has been masked on the full 72-79°E, 7-14°N grid. The grid itself was not cropped, so ocean cells are kept as missing values (NaN) and the grid still lines up with the other ERA5 fields.
- Mask: ERA5 land-sea mask (`lsm`), keeping cells with `lsm > 0.5`. This gives 225 land cells out of 625, the same cells as the ERA5 wind land mask.
- Notebook: `land_mask/landmask_gpm.ipynb`. Figure: `landonly/gpm_land_only_jjas2020_total.png`.
- Check: 122 days x 225 cells = 27,450 valid values.
- Cells that are less than 50% land are excluded, so some partly coastal cells (including part of the heaviest coastal rainfall) are masked out.

## Next steps
- Replace the dew point with specific humidity once the professor provides the information. The IMERG part does not change, but the ERA5 grid should be checked against the new variable.
- Add SRTM elevation and extend to more years.
- Agree the common grid with the project partner (see Limitations).
