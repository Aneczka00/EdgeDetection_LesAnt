# === Script: create_combined_bathy_data.py ===
import pandas as pd
import numpy as np
import xarray as xr
import rioxarray as rxr
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
import geopandas as gpd

print("Loading GEBCO and MBES datasets...")
gebco = xr.open_dataset("C:/Users/aczachor/Desktop/gebco_2024.nc")
mbes = rxr.open_rasterio("C:/Users/aczachor/Desktop/Synthese_ArcAntillais_1_16min_BATHY.tif")

# Clip bounds
x_min, x_max = -66.5, -40.5
y_min, y_max = 6.0, 20.0

print("Clipping datasets...")
gebco_clip = gebco.sel(lon=slice(x_min, x_max), lat=slice(y_min, y_max))
mbes_clip = mbes.rio.clip_box(minx=x_min, miny=y_min, maxx=x_max, maxy=y_max)

print("Cleaning MBES...")
mbes_clean = mbes_clip.squeeze()
mbes_clean = np.where(mbes_clean <= -10000, np.nan, mbes_clean)

X, Y = np.meshgrid(mbes_clip.x, mbes_clip.y)
mbes_mask = ~np.isnan(mbes_clean)
mbes_lon = X[mbes_mask]
mbes_lat = Y[mbes_mask]
mbes_depth = mbes_clean[mbes_mask]

print("Creating GeoDataFrames...")
mbes_gdf = gpd.GeoDataFrame({'depth': mbes_depth}, geometry=gpd.points_from_xy(mbes_lon, mbes_lat), crs="EPSG:4326")

gebco_lon, gebco_lat = np.meshgrid(gebco_clip['lon'], gebco_clip['lat'])
gebco_depth = gebco_clip['elevation'].values
gebco_flat = pd.DataFrame({
    'lon': gebco_lon.flatten(),
    'lat': gebco_lat.flatten(),
    'depth': gebco_depth.flatten()
}).dropna()

gebco_gdf = gpd.GeoDataFrame(gebco_flat, geometry=gpd.points_from_xy(gebco_flat['lon'], gebco_flat['lat']), crs="EPSG:4326")

# Reproject to UTM Zone 20N
print("Reprojecting to UTM Zone 20N (EPSG:32620)...")
utm_crs = "EPSG:32620"
mbes_utm = mbes_gdf.to_crs(utm_crs)
gebco_utm = gebco_gdf.to_crs(utm_crs)

# Filter GEBCO points too close to MBES
print("Filtering GEBCO points within 5 km of MBES...")
mbes_coords = np.column_stack((mbes_utm.geometry.x.values, mbes_utm.geometry.y.values))
gebco_coords = np.column_stack((gebco_utm.geometry.x.values, gebco_utm.geometry.y.values))
mbes_tree = cKDTree(mbes_coords)
dists, _ = mbes_tree.query(gebco_coords, k=1)

distance_threshold = 5000  # 5 km
gebco_filtered = gebco_utm[dists > distance_threshold]

# Combine
print("Combining MBES and filtered GEBCO data...")
combined_x = np.concatenate([mbes_utm.geometry.x.values, gebco_filtered.geometry.x.values])
combined_y = np.concatenate([mbes_utm.geometry.y.values, gebco_filtered.geometry.y.values])
combined_depth = np.concatenate([mbes_utm['depth'].values, gebco_filtered['depth'].values])

# Save
print("Saving to NPZ...")
np.savez("combined_bathy_data.npz",
         combined_x=combined_x,
         combined_y=combined_y,
         combined_depth=combined_depth)

print("Saved: combined_bathy_data.npz")
