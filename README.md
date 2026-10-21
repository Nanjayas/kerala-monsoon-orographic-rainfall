# Kerala_monsoon_orographic_rainfall

# GPM IMERG rainfall processing

## What this folder contains
- `01_imerg_download_june2020.ipynb`: downloads and crops IMERG rainfall, makes the June 2020 map

## Data
| Item | Detail |
|---|---|
| Product | GPM IMERG V07 Final Run, daily (GPM_3IMERGDF) |
| Source | NASA GES DISC via `earthaccess` |
| Domain | 74-78°E, 8-13°N |
| Period | June 2020 |
| Resolution | 0.1° |

## How to reproduce
1. Create a free NASA Earthdata account and authorise "NASA GESDISC DATA ARCHIVE".
2. Install: `pip install earthaccess xarray netCDF4 dask matplotlib`
3. Run the notebook. Data is downloaded to `data/raw/imerg/` and is not stored in Git.

## Notes and limitations
- IMERG can underestimate rainfall over steep terrain.
- Results apply to June 2020 only. # did this as an initial step
