# GPM IMERG rainfall processing (JJAS 2020)

Notebook: `<name of the notebook with the JJAS code>`. Output map: `docs/figures/imerg_jjas2020_total.png`.

## Data
| Item | Detail |
|---|---|
| Product | GPM IMERG V07 Final Run, daily (`GPM_3IMERGDF`) |
| Source | NASA GES DISC, downloaded with the `earthaccess` Python package |
| Variable | `precipitation` (mm/day) |
| Grid | 0.1° |
| Domain | 72-79°E, 7-14°N (70 x 70 grid points) |
| Period | 1 June - 30 September 2020 (122 days, UTC days) |

## Method
1. Log in to NASA Earthdata and search for the daily files (122 expected).
2. Check that the file count matches the number of days.
3. Download the global daily files and crop them to the study domain.
4. Check the values (range and missing data) and save the cropped file.
5. Sum the daily values over time to get the seasonal total (mm) and plot it.

## Result
The JJAS 2020 total reaches about 4000 mm along the coast at roughly 13-14°N, 74-75°E, which lies north of Kerala (Kerala ends near 12.8°N). Rainfall drops sharply across a diagonal edge running from about 75°E at 13-14°N to about 77°E at 8°N. East of this edge totals are roughly 500-1000 mm, and the driest area (<500 mm) is the south-east corner. Over the open sea west of the coast, totals are about 1000-2000 mm. This pattern is consistent with orographic enhancement on the windward side and a rain shadow behind the Western Ghats. The alignment with the terrain still has to be checked against the SRTM elevation data.

## Limitations
- IMERG is a satellite estimate and may underestimate rainfall over steep terrain and from shallow clouds.
- The 0.1° grid is not the true resolution of the underlying satellite measurements, which is coarser.
- Only one season (2020) has been processed so far.

## How to reproduce
1. Create a free NASA Earthdata account and authorise "NASA GESDISC DATA ARCHIVE".
2. Install: `pip install earthaccess xarray netCDF4 dask matplotlib`
3. Run the notebook. Data is downloaded to `data/raw/imerg/` and is not stored in Git.
