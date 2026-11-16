# Linear regression: GPM rainfall vs moist-upslope forcing

Preliminary statistical baseline for the Kerala–Western Ghats monsoon project (JJAS 2020).

## Aim

Quantify, with one simple linear regression, how total southwest-monsoon rainfall is associated with the moist-upslope forcing index across the land grid cells. This is the interpretable baseline described in the project proposal.

## Data

All fields are on the same 25 × 25 ERA5 grid, land cells only (225 cells), June–September 2020 (122 daily steps).

| Quantity | Source | Variable |
|---|---|---|
| Rainfall | GPM IMERG daily, land-masked | `rain` |
| Moist-upslope index | ERA5 winds and specific humidity (700 hPa) with SRTM terrain gradients | `moist_upslope` |

The moist-upslope index is built from the orographic forcing

w_oro = u · ∂h/∂x + v · ∂h/∂y

and is defined as M_oro = q · max(w_oro, 0). It is an approximate terrain-related forcing diagnostic, not a measured vertical velocity or rainfall.

## Method

For each land cell *i*:

- P_i = total JJAS 2020 GPM rainfall (mm), the sum over the 122 days
- M_i = seasonal-mean moist-upslope index (multiplied by 1000 for readable units)

Model: P̂_i = β₀ + β₁ M_i, fitted by ordinary least squares over the 225 cells.

Reported: intercept, slope, R², RMSE, plus Pearson and Spearman correlations as consistency checks.

## Results

### Data summary

| Quantity | Value |
|---|---|
| Land grid cells | 225 |
| Cells with M = 0 | 0 (the seasonal-mean index is positive everywhere) |
| Total JJAS 2020 rainfall | 195 to 3596 mm across cells, mean 1015 mm |
| Seasonal-mean moist-upslope index M | 7.8 × 10⁻⁷ to 1.49 × 10⁻³ (0.0008 to 1.49 after multiplying by 1000) |

### Correlation checks

| Relationship | Pearson r | Spearman ρ |
|---|---:|---:|
| Rainfall vs orographic forcing (w_oro) | 0.6284 | 0.5974 |
| Rainfall vs moist-upslope index (M) | 0.6637 | 0.7262 |

Both indices are positively associated with rainfall, and the moist-upslope index shows the stronger association. For M, Spearman (0.73) is higher than Pearson (0.66), so the relationship is more consistent in rank order than it is linear. The reason has not been examined yet.

### Regression fit

Model: P̂ = β₀ + β₁ M, fitted by ordinary least squares over the 225 land cells (M multiplied by 1000).

| Quantity | Value | Meaning |
|---|---|---|
| Intercept β₀ | 722.5 mm | Fitted rainfall where M is close to zero |
| Slope β₁ | 1634 mm per unit of (1000 × M) | Fitted rainfall increase per unit increase of the scaled index |
| R² | 0.4406 | Fraction of the spatial variance in rainfall accounted for by the line |
| RMSE | 570.3 mm | Typical size of the fitted rainfall error |
| RMSE / mean rainfall | 56 % | Error relative to the mean (1015 mm) |

### Interpretation

- **Strength of the association.** The line accounts for about 44 % of the spatial variance in JJAS 2020 rainfall. As a check, R² equals Pearson r squared (0.6637² = 0.4406), as it must for one predictor.
- **Size of the effect.** M spans about 1.49 on the scaled axis, so the fitted rainfall rises by roughly 2400 mm from the lowest-M cells (about 720 mm) to the highest-M cells (about 3150 mm).
- **Size of the error.** Rainfall varies from cell to cell with a standard deviation of about 760 mm. The regression reduces the typical error to 570 mm, a reduction of about one quarter. A typical cell is still off by more than half the mean rainfall, so the line is a rough guide and not a precise predictor for individual cells.
- **What remains unexplained.** The other 56 % of the variance is not captured by M. Possible sources include the coast, convection, other terrain effects and satellite rainfall uncertainty over complex terrain. Their contributions have not been tested here.
- **Residual check.** The mean residual is zero (about 10⁻¹³), as expected for a least-squares fit with an intercept.


## Usage

```bash
python scripts/linear_regression.py RAIN_FILE MOIST_FILE OUT_DIR
```

`RAIN_FILE` and `MOIST_FILE` are the NetCDF files named in the Data section, and `OUT_DIR` is the folder for the figures.

## Limitations

- Association, not causation: the result does not say that orographic forcing causes a given share of the rainfall.
- Neighbouring grid cells are not independent, so p-values and confidence intervals are not reported.
- R² is in-sample: it describes the fit to the same cells, not predictive skill.
- One season and one predictor only. Wind direction, moisture and distance from the coast are not included.

  # Per-cell daily regression: GPM rainfall vs moist-upslope index

Maps of a separate linear regression and correlation at every land grid cell, for the Kerala–Western Ghats monsoon project (JJAS 2020).

## Aim

The region-wide regression in the parent folder compares cells with each other, using seasonal totals. This analysis holds the location fixed and asks a different question: **at a given cell, does it rain more on days when the moist-upslope forcing is stronger?** Terrain, distance from the coast and local climate do not change from day to day, so they cannot explain differences between days at one cell. The maps show where this relationship is present and where it is not.

## Data

| Quantity | Source | Variable |
|---|---|---|
| Daily rainfall | GPM IMERG, land-masked, on the ERA5 grid | `rain` (mm/day) |
| Daily moist-upslope index | ERA5 winds and specific humidity (700 hPa) with SRTM terrain gradients | `moist_upslope` |

- 25 × 25 grid, 225 land cells, 122 days (1 June to 30 September 2020).
- The two files carry different time-of-day stamps (00:00 for rainfall, 11:30 for the daily-mean index). Both were labelled by calendar date and checked to match on all 122 days.
- Daily rainfall over the land cells ranges from 0 to 169.3 mm/day with a mean of 8.32 mm/day. 6.2 % of land-cell-days have no rain.
- The moist-upslope index is M = q · max(w_oro, 0), where w_oro = u · ∂h/∂x + v · ∂h/∂y. It is zero whenever the flow is not directed upslope. For readable units, M is multiplied by 1000.

## Method

At each land cell, the 122 daily pairs (M, rainfall) are used to compute:

- the least-squares line: rainfall = intercept + slope · M
- Pearson r, Spearman ρ and R² of the fit
- RMSE of the fit (mm/day)
- the number of days with M = 0

All quantities are computed per cell, so each map has 225 values.

## Maps

All maps are in this folder. The white area is the masked ocean.

| File | Quantity |
|---|---|
| `pearson_r_map.png` | Pearson r between daily rainfall and M |
| `spearman_rho_map.png` | Spearman ρ between daily rainfall and M |
| `r2_map.png` | R² of the per-cell linear fit |
| `slope_map.png` | Regression slope (mm/day per unit of 1000 × M) |
| `intercept_map.png` | Regression intercept (mm/day) |
| `rmse_map.png` | RMSE of the per-cell fit (mm/day) |
| `n_zero_M_days_map.png` | Number of days with M = 0 (of 122) |

## Results

### Summary over the 225 cells

| Quantity | Minimum | Median | Maximum |
|---|---:|---:|---:|
| Pearson r | −0.257 | 0.039 | 0.549 |
| Spearman ρ | −0.241 | 0.074 | 0.580 |
| R² | 0.000 | 0.007 | 0.302 |
| Slope (mm/day per unit of 1000 × M) | −88.4 | 4.8 | 238.5 |
| Intercept (mm/day) | 0.6 | 5.2 | 14.3 |
| RMSE (mm/day) | 3.6 | 8.1 | 26.5 |
| Days with M = 0 (of 122) | 5 | 91 | 118 |

135 of 225 cells have r > 0, 41 have r > 0.3 and 12 have r > 0.5. The highest r (0.549, R² = 0.302) is at 13.35°N, 74.81°E.

### What the maps show

- **The daily relationship is strongest on the western, windward side.** Pearson r and Spearman ρ are highest (about 0.4 to 0.6) in the north-west corner, around 74.7 to 76°E and 12.3 to 14°N, and moderately positive along the western edge further south. East of about 77.5°E, r is close to zero or slightly negative. R² follows the same pattern and is below 0.05 at most cells.
- **At a typical cell, daily M explains very little of daily rainfall.** The median R² is 0.007.
- **The zero-M map mirrors the r map.** In the west M is zero on only a few days, while in the east it is zero on 100 to 118 days. At cells where M is almost always zero, a relationship cannot show up, so r is close to zero there. This is a property of the index, not evidence that terrain does not matter in the east.
- **Intercept and RMSE are largest on the windward coast** (intercept 8 to 14 mm/day, RMSE 20 to 26 mm/day) and smallest in the east. They follow how much it rains, so RMSE should not be read as fit quality on its own. R² is the measure of fit quality.
- **The slope map is noisy.** Several cells hit the colour limit, and some of them have M above zero on only a few days, so the fit rests on few points. Slopes are not comparable between cells because the range of M differs from cell to cell. Conclusions should be based on r, ρ and R².

## Relation to the region-wide regression

The region-wide fit (seasonal totals over the 225 cells) gives R² = 0.44, so places with more moist-upslope forcing receive more rain in total. The per-cell maps show that within a single place, the daily link is weak at most cells and clearly present mainly on the windward side. The two results answer different questions and do not contradict each other.

## Limitations

- Association, not causation.
- Consecutive days are correlated, and with 122 days a correlation below about 0.18 in magnitude cannot be told apart from zero. Consecutive-day dependence raises this threshold, so p-values are not reported.
- Daily rainfall is skewed and has many small values, and M is zero on many days. A straight line fits this poorly, and the fitted line can go below zero at high M.
- The grid cells are about 30 km wide, so the terrain is smoothed. The winds are daily means at 700 hPa and rainfall is a daily total, with no time lag between them.
- GPM rainfall has extra uncertainty over complex terrain.
- One season (JJAS 2020) and one predictor only.
