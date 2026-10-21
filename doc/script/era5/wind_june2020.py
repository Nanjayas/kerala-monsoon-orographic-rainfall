for file in folder.iterdir():
    print(repr(file.name))
    
import xarray as xr
u = xr.open_dataset(folder / "ua_700hPa_kerala_202006.nc")["ua"]
v = xr.open_dataset(folder / "va_700hPa_kerala_202006.nc")["va"]
print("u shape:", u.shape)
print("v shape:",v.shape)
print("time matches;",u.time.equals(v.time))
print("lon matches :",u.lon.equals(v.lon))
print("lat matches:",u.lat.equals(v.lat))
import numpy as np
wind_speed = np.sqrt(u**2+v**2)
print("wind speed shape:",wind_speed.shape)
print("mean wind speed:",float(wind_speed.mean().values))
print("maximum wind speed:",floatwind_speed.max().values))
print("maximum wind speed:",float(wind_speed.max().values))
u_mean = u.mean(dim="time")
v_mean = v.mean(dim ="time")
mean_vector_speed = np.sqrt(u_mean**2 + v_mean**2)
print("meanu shape:",u_mean.shape)
print("meanu shape:",u_mean.shape)
print("mean_vector_speed shape:",mean_vector_speed.shape)
import matplotlib 
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.figure(figsize = (8,6))
mean_vector_speed.plot(x = "lon",y= "lat",cmap ="viridis",add_colorbar = True)
plt.quiver(u_mean["lon"].values,u_mean["lat"].values,u_mean.values,v_mean.values,color ="white",scale=200)
plt.title("ERA5 Mean Wind Vector -June 2020,700hPa")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig(str(Path.home() / "kerala_project/wind_vector_700hPa_202006.png"),dpi = 150,bbox_inches="tight")
plt.close()
print((Path.home() / "kerala_project/wind_vector_700hPa_202006.png").exists())
