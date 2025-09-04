import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pyproj import Transformer
import cartopy.crs as ccrs
import cartopy.feature as cfeature


df = pd.read_csv(
    "E:/Ania/Earthquakes/Seismicity_IPGP/FINAL_final_filtered_catalogue_H_less_11_D_6_all.csv",
    sep=";", engine="python"
)
df.columns = df.columns.str.strip().str.lower()
df["magnitude"] = df["magnitude"].astype(str).str.replace(",", ".").astype(float)
df.dropna(subset=["latitude", "longitude", "depth", "magnitude"], inplace=True)


start = (14.0, -64.0)
end = (15.0, -57.0)
max_dist_km = 50  # perpendicular 

transformer = Transformer.from_crs("epsg:4326", "epsg:32620", always_xy=True)

start_utm = np.array(transformer.transform(start[1], start[0]))
end_utm = np.array(transformer.transform(end[1], end[0]))

df["x"], df["y"] = transformer.transform(df["longitude"].values, df["latitude"].values)

def project_point_utm(x, y, start_utm, end_utm):
    direction = end_utm - start_utm
    direction /= np.linalg.norm(direction)
    rel_vector = np.array([x, y]) - start_utm
    dist_along = np.dot(rel_vector, direction)
    dist_perp = np.linalg.norm(rel_vector - dist_along * direction)
    return dist_along, dist_perp

distances, depths, mags, xs, ys, lats, lons = [], [], [], [], [], [], []

for _, row in df.iterrows():
    dist_along, dist_perp = project_point_utm(row["x"], row["y"], start_utm, end_utm)
    if abs(dist_perp) <= max_dist_km * 1000:  # filter by 50 km
        distances.append(dist_along / 1000)  # meters to km
        depths.append(row["depth"])
        mags.append(row["magnitude"])
        xs.append(row["x"])
        ys.append(row["y"])
        lats.append(row["latitude"])
        lons.append(row["longitude"])

df_proj = pd.DataFrame({
    "distance_along": distances,
    "depth": depths,
    "magnitude": mags,
    "x": xs,
    "y": ys,
    "latitude": lats,
    "longitude": lons
})


bathy_ds = xr.open_dataset("C:/Users/aczachor/Desktop/Grav/Python_Scripts/SWOT/gebco_2024.nc")
bathy = bathy_ds["elevation"]

lon_min, lon_max = sorted([df["longitude"].min() - 2, df["longitude"].max() + 2])
lat_min, lat_max = sorted([df["latitude"].min() - 2, df["latitude"].max() + 2])

bathy = bathy.sel(lon=slice(lon_min, lon_max), lat=slice(lat_min, lat_max))


slab_ds = xr.open_dataset("E:/Ania/Earthquakes/lesser_antilles_slab_BIE-ET-AL.grd", engine="netcdf4")
slab_var = list(slab_ds.data_vars)[0]
slab = slab_ds[slab_var]
slab_subset = slab.sel(x=slice(lon_min, lon_max), y=slice(lat_min, lat_max))


N = 500
lats_profile = np.linspace(start[0], end[0], N)
lons_profile = np.linspace(start[1], end[1], N)

slab_profile_depths = slab_subset.interp(
    x=(("points",), lons_profile),
    y=(("points",), lats_profile)
).values

profile_start_utm = np.array(transformer.transform(start[1], start[0]))
profile_end_utm = np.array(transformer.transform(end[1], end[0]))
profile_total_dist = np.linalg.norm(profile_end_utm - profile_start_utm)
profile_distances = np.linspace(0, profile_total_dist / 1000, N)  # in km


slab_at_eqs = slab_subset.interp(
    x=("points", df_proj["longitude"].values),
    y=("points", df_proj["latitude"].values)
).values

df_proj["slab_depth"] = slab_at_eqs
df_proj["depth_diff_to_slab"] = df_proj["depth"] - slab_at_eqs

# Filter earthquakes within ±5 km of slab
# df_near_slab = df_proj[np.abs(df_proj["depth_diff_to_slab"]) <= 5].copy()
plt.rcParams.update({'font.size': 18})

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Convert bathymetry to km
bathy_km = bathy / 1000.0

bathy_contour = ax.contourf(
    bathy.lon, bathy.lat, bathy_km,
    levels=np.arange(-10, 0, 0.5),  # bathymetry in km
    cmap="Blues_r", extend='both',
    transform=ccrs.PlateCarree()
)

scatter1 = ax.scatter(
    df["longitude"], df["latitude"],
    c=df["depth"], cmap="plasma", s=df["magnitude"]**3, alpha=0.75,
    edgecolors="k", transform=ccrs.PlateCarree()
)

# Profile line
ax.plot([start[1], end[1]], [start[0], end[0]], 'r--', transform=ccrs.PlateCarree())

# Map setup
ax.coastlines(resolution='10m', linewidth=1)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.set_extent([lon_min, lon_max, lat_min, lat_max])
ax.gridlines(draw_labels=True)

# Colorbar in km, remove minus signs
cb = plt.colorbar(bathy_contour, ax=ax, orientation='vertical', label="Bathymetry [km]")
ticks = cb.get_ticks()
cb.set_ticks(ticks)
cb.set_ticklabels([f"{-val:.1f}" for val in ticks])  # show positive km

plt.tight_layout()
plt.show()


plt.rcParams.update({'font.size': 16})

fig, ax = plt.subplots(figsize=(12, 6))

# Slab profile
ax.plot(
    profile_distances, -slab_profile_depths,
    'r--', linewidth=2, label="Slab Surface"
)

# Earthquakes near slab
sc2 = ax.scatter(
    df_proj["distance_along"], -df_proj["depth"],
    c=df_proj["magnitude"], cmap="plasma", s=df_proj["magnitude"]**3,
    edgecolors="k", alpha=0.8, label="Non-filtered earthquakes along the profile"
)

ax.set_xlabel("Distance Along Profile (see map above) [km]")
ax.set_ylabel("Depth Below Seafloor [km]")
ax.grid(True)

ax.legend(fontsize=12)
cbar2 = plt.colorbar(sc2, ax=ax, orientation='vertical', label="Magnitude")

plt.tight_layout()
plt.show()