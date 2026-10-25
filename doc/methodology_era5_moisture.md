# ERA5 Near-Surface Moisture Processing (JJAS 2020)

Script: `doc/script/era5/tdps_map.py`. Output map: `docs/figures/era5/tdps_jjas2020_mean.png`.

This file complements the main `methodology.md`.

## Data
| Item | Detail |
|---|---|
| Dataset | ERA5 reanalysis, daily means (university archive) |
| Variable | `tdps`, 2 m dew point temperature |
| Path | `/daten/erafive/arch/data/dkrz-sync/ERA5/day/atmos/tdps/r1i1p1/` |
| Grid | about 0.28° (global 1280 x 640) |
| Domain | 72-79°E, 7-14°N (18 x 14 grid points) |
| Period | 1 June - 30 September 2020 (122 days) |

## Method
1. Located `tdps` in the daily ERA5 archive. Daily specific humidity (`hus`) and total column water vapour (`prw`) were not found there.
2. Opened the 2020 yearly file with xarray.
3. Selected JJAS 2020 and the study box.
4. Converted from Kelvin to °C and averaged over time.

## Why dew point
It depends only on the amount of water vapour in the air, not on air temperature, so it is a better moisture measure than relative humidity. It can later be converted to specific humidity.

## Result
The seasonal mean dew point ranges from about 17.9 to 25.4 °C. It is highest (about 24-25 °C) in the west and south near the sea and coast, and lower (about 18-21 °C) in the north-east and interior, consistent with the IMERG rainfall pattern.

## Limitations
- `tdps` is a 2 m surface variable. It is only a proxy for moisture at 925-850 hPa and is not at the same level as the 700 hPa wind.
- ERA5 terrain is smoothed at about 31 km, so some local features may be terrain effects rather than real moisture features.
- Only one season (2020) has been processed so far.

## Next steps
- Check for pressure-level humidity (for example in the hourly archive) to calculate moisture flux.
- Agree one study box and common grid with the partner's work.
- Extend to more years.
