# GPM IMERG rainfall processing (JJAS 2020)

Notebook: `01_imreg_download_june2020.ipynb` (updated to cover JJAS 2020). Output map: `docs/figures/imerg_jjas2020_total.png`.

## Data
| Item | Detail |
|---|---|
| Product | GPM IMERG V07 Final Run, daily (`GPM_3IMERGDF`) |
| Source | NASA GES DISC, downloaded with the `earthaccess` Python package |
| Variable | `precipitation` (mm/day) |
| Resolution | 0.1° |
| Domain | 72-79°E, 7-14°N (40 x 50 grid points) |
| Period | 1 June - 30 September 2020 (122 days) |

## Method
1. Log in to NASA Earthdata and search for the daily files (122 expected).
2. Check that the file count matches the number of days.
3. Download the files and crop them to the study domain.
4. Check the values (range and missing data) and save the cropped file.
5. Sum over time to get the seasonal total and plot it.

## Result
The JJAS 2020 total reaches about 3600 mm in the north-west of the domain (around 12.5-13°N, 74.5-75.5°E). A sharp diagonal edge runs from the north-west to the south-east along the Western Ghats, and totals fall below about 500 mm on the leeward side in the east. This is consistent with orographic enhancement on the windward side and a rain shadow behind the Ghats.

## Limitations
- IMERG is a satellite estimate. It can underestimate rainfall over steep terrain and may miss rain from shallow clouds.
- Only one season (2020) has been processed so far.
- The domain (74-78°E, 8-13°N) is smaller than the box in `doc/methodology.md` (72-79°E, 7-14°N). One box needs to be agreed for all datasets.

## How to reproduce
1. Create a free NASA Earthdata account and authorise "NASA GESDISC DATA ARCHIVE".
2. Install: `pip install earthaccess xarray netCDF4 dask matplotlib`
3. Run the notebook. Data is downloaded to `data/raw/imerg/` and is not stored in Git.

## Next steps
- Add SRTM elevation and compare rainfall with terrain.
- Regrid to the common grid with ERA5.
- Extend to more years.
