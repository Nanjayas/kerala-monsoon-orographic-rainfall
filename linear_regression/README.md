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