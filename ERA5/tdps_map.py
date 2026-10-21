import xarray as xr
import matplotlib
matplotlib.use("Agg")   # lets the server draw a picture without a screen
import matplotlib.pyplot as plt

f = "/daten/erafive/arch/data/dkrz-sync/ERA5/day/atmos/tdps/r1i1p1/tdps_day_reanalysis_era5_r1i1p1_20200101-20201231.nc"
ds = xr.open_dataset(f)

# JJAS 2020, Kerala box, converted from Kelvin to degrees C
t = ds["tdps"].sel(time=slice("2020-06-01", "2020-09-30"),
                   lon=slice(74, 78), lat=slice(8, 13)) - 273.15
t.attrs["units"] = "degC"

# Save the small cropped data (a few hundred KB)
t.to_netcdf("tdps_jjas2020_kerala.nc")

# Average over all days -> one value per grid point
mean = t.mean("time")
print("Mean dew point range (degC):", float(mean.min()), float(mean.max()))

mean.plot(cbar_kwargs={"label": "degC"})
plt.title("Mean 2 m dew point, JJAS 2020 (ERA5)")
plt.savefig("tdps_jjas2020_mean.png", dpi=200, bbox_inches="tight")
print("Saved map and data")
