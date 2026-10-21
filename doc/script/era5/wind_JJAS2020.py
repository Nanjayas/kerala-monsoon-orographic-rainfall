from pathlib import Path
>>> import xarray as xr
>>> import numpy as np
>>> import matplotlib
>>> matplotlib.use("Agg")
>>> import matplotlib.pyplot as plt
>>> folder = Path.home() /"kerala_project/data/era5"
>>> u = xr.open_dataset(folder/ "ua_700hPa_JJAS2020_mean.nc")["ua"]
>>> v = xr.open_dataset(folder/ "va_700hPa_JJAS2020_mean.nc")["va"]
>>> print("u shape :",u.shape)
u shape : (1, 25, 25)
>>> print("V shappe:",v.shape)
V shappe: (1, 25, 25)
>>> print("time matches:",u.time.equals(v.time))
time matches: True
>>> print("lon matches:",u.lon.equals(v.lon))
lon matches: True
>>> print(" lat matches:",u.lat.equals(v.lat))
 lat matches: True
>>> mean_vector_speed = np.sqrt(u**2 + v**2)
>>> plt.figure(figsize = (8,6))
<Figure size 800x600 with 0 Axes>
>>> mean_vector_speed.plot(x = "lon",y= "lat",cmap = "viridis",add_colorbar = True)
... 
... 
<matplotlib.collections.QuadMesh object at 0x7f3c3d8b67b0>
>>> 
>>> plt.quiver(u["lon"].values,u["lat"].values,u.values.squeeze(),v.values.squeeze(),color = "white",\
                                                                                                      <matplotlib.quiver.Quiver object at 0x7f3c3d8b7620>
>>> plt.title("ERA5 Mean Wind Vector - JJAS 2020, 700 hPa")
Text(0.5, 1.0, 'ERA5 Mean Wind Vector - JJAS 2020, 700 hPa')
>>> plt.xlabel("Longitude")
... 
Text(0.5, 0, 'Longitude')
>>> plt.ylabel("Latitude")
... 
Text(0, 0.5, 'Latitude')
>>> outfile = Path.home() / "kerala_project/wind_vector_700hPa_JJAS2020.png"
... 
>>> plt.savefig(str(outfile), dpi=150, bbox_inches="tight")
... 
>>> plt.close()
... 
>>> print(outfile.exists())
... 
True
