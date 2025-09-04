import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  
from matplotlib import cm
import xarray as xr
import geopandas as gpd
from shapely.geometry import Point
from scipy.interpolate import griddata
from scipy.spatial import cKDTree
from mpl_toolkits.axes_grid1 import make_axes_locatable

# =========================
# Loading bathymetry 
# =========================
bathy_ds = xr.open_dataset("E:/Ania/M2_QGIS_Project/DATA/Bathy/gebco_74-52-10-24.nc")
bathy_var = list(bathy_ds.data_vars)[0] 
bathy = bathy_ds[bathy_var]

# Crop bathymetry 
slab_domain = {
    "lon_min": -65, "lon_max": -55,
    "lat_min": 9, "lat_max": 20
}

y_vals = bathy['y'].values
if y_vals[0] > y_vals[-1]:
    # y decreases (north -> south) -> flip slice
    y_slice = slice(slab_domain["lat_max"], slab_domain["lat_min"])
else:
    # y increases (south -> north)
    y_slice = slice(slab_domain["lat_min"], slab_domain["lat_max"])

bathy_cropped = bathy.sel(
    x=slice(slab_domain["lon_min"], slab_domain["lon_max"]),
    y=y_slice
)


# Extract arrays
BATHY_LON, BATHY_LAT = np.meshgrid(
    bathy_cropped['x'].values,
    bathy_cropped['y'].values
)
BATHY_Z = bathy_cropped.values / 1000.0  # meters -> km


# =========================
# Loading slab and earthquake data
# =========================

# Slab
slab_ds = xr.open_dataset("E:/Ania/Earthquakes/lesser_antilles_slab_BIE-ET-AL.grd", engine="netcdf4")
slab_var = list(slab_ds.data_vars)[0] 
slab = slab_ds[slab_var]

slab_lons = slab_ds['x'].values
slab_lats = slab_ds['y'].values
LON, LAT = np.meshgrid(slab_lons, slab_lats)
DEPTH = slab.values  

# Earthquake data
df = pd.read_csv("E:/Ania/Earthquakes/Seismicity_IPGP/FINAL_final_filtered_catalogue_H_less_11_D_6_all.csv", sep=";", engine="python")
df.columns = df.columns.str.strip().str.lower()
df["magnitude"] = df["magnitude"].astype(str).str.replace(",", ".").astype(float)
df.dropna(subset=["latitude", "longitude", "depth", "magnitude"], inplace=True)

# Interpolate slab depth at earthquake locations
eq_lons = df["longitude"].values
eq_lats = df["latitude"].values
slab_interp = slab.interp(x=(("points",), eq_lons), y=(("points",), eq_lats)).values
df["slab_depth"] = slab_interp
df["depth_diff_to_slab"] = df["depth"] - df["slab_depth"]
df_near_slab = df[np.abs(df["depth_diff_to_slab"]) <= 5]

# Export near-slab earthquakes
geometry = [Point(xy) for xy in zip(df_near_slab['longitude'], df_near_slab['latitude'])]
gdf_eq = gpd.GeoDataFrame(df_near_slab, geometry=geometry)
gdf_eq.set_crs(epsg=4326, inplace=True)
gdf_eq_utm = gdf_eq.to_crs(epsg=32620)
gdf_eq_utm.to_file("E:/Ania/Earthquakes/earthquakes_near_slab_utm20N_only_Massin.shp")

# =========================
# Shapefiles
# =========================
shapefiles = [
    "E:/Ania/M2_QGIS_Project/OUTPUT/shapefiles/CJL_line.shp",
    "E:/Ania/M2_QGIS_Project/OUTPUT/shapefiles/FZs_slab_final.shp",
    "E:/Ania/M2_QGIS_Project/OUTPUT/shapefiles/Anomaly_4_ln.shp"
]

all_coords_list = []

for shp_path in shapefiles:
    shp = gpd.read_file(shp_path)
    shp = shp.to_crs(epsg=4326)
    coords_list = []

    # Extraction of coords
    def extract_coords(geom):
        if geom.is_empty:
            return
        if geom.geom_type == "Polygon":
            coords_list.append(geom.exterior.xy)
            for interior in geom.interiors:
                coords_list.append(interior.xy)
        elif geom.geom_type == "LineString":
            coords_list.append(geom.xy)
        elif geom.geom_type.startswith("Multi") or geom.geom_type == "GeometryCollection":
            for part in geom.geoms:
                extract_coords(part)

    for geom in shp.geometry:
        extract_coords(geom)

    all_coords_list.append(coords_list)

# =========================
# Interpolation
# =========================
points = np.column_stack((LON.ravel(), LAT.ravel()))
values = DEPTH.ravel()
tree = cKDTree(points)

# =========================
# Plotting 3D slab, bathymetry, earthquakes, shapefiles
# =========================
fig3d = plt.figure(figsize=(14, 10))
ax3d = fig3d.add_subplot(111, projection='3d')

# Bathymetry range for cropped region
bathy_min = float(np.nanmin(BATHY_Z))
bathy_max = float(np.nanmax(BATHY_Z))

# Vertical exaggeration for bathymetry
vertical_exaggeration = 10  # exaggerate 10x
BATHY_Z_DOWN = -BATHY_Z  # now 0 at surface, positive downward
BATHY_Z_EXAG = BATHY_Z_DOWN * vertical_exaggeration

surf_bathy = ax3d.plot_trisurf(
    BATHY_LON.ravel(),
    BATHY_LAT.ravel(),
    BATHY_Z_EXAG.ravel(),
    cmap='terrain_r',
    linewidth=0,
    alpha=0.7
)


# Slab surface
surf = ax3d.plot_surface(
    LON, LAT, DEPTH,
    cmap="cividis", edgecolor='none', alpha=0.7
)

# Earthquakes
sc = ax3d.scatter(
    df_near_slab["longitude"].values,
    df_near_slab["latitude"].values,
    df_near_slab["depth"].values,
    c=df_near_slab["magnitude"].values,
    cmap='plasma',
    s=np.clip(df_near_slab["magnitude"].values ** 3, 5, 100),
    edgecolor='k',
    alpha=0.9
)

# # Shapefile lines
# colors = ["red", "black", "green"]
# for i_shp, coords_list in enumerate(all_coords_list):
#     color = colors[i_shp % len(colors)]
#     for x, y in coords_list:
#         x = np.array(x)
#         y = np.array(y)
#         xy_points = np.column_stack((x.ravel(), y.ravel()))

#         # Nearest neighbor interpolation
#         z = griddata(points, values, xy_points, method="nearest")

#         # Fill NaNs with nearest neighbor
#         if np.isnan(z).any():
#             nan_idx = np.where(np.isnan(z))[0]
#             for idx in nan_idx:
#                 _, nearest_idx = tree.query(xy_points[idx])
#                 z[idx] = values[nearest_idx]

#         ax3d.plot(x, y, z, color=color, linewidth=2)

# Labels 
ax3d.set_xlabel("Longitude", fontsize=16, labelpad=10)
ax3d.set_ylabel("Latitude", fontsize=16, labelpad=10)
ax3d.set_zlabel("Depth [km]", fontsize=16, labelpad=10)
ax3d.tick_params(axis='both', labelsize=14)
ax3d.set_zlim(np.nanmax(DEPTH), np.nanmin(DEPTH))  # flip Z axis

# Colorbars
cax1 = fig3d.add_axes([0.20, 0.10, 0.20, 0.02])  # slab
cax2 = fig3d.add_axes([0.45, 0.10, 0.20, 0.02])  # earthquakes
cax3 = fig3d.add_axes([0.70, 0.10, 0.20, 0.02])  # bathymetry

cb1 = fig3d.colorbar(surf, cax=cax1, orientation='horizontal')
cb2 = fig3d.colorbar(sc, cax=cax2, orientation='horizontal')
cb3 = fig3d.colorbar(surf_bathy, cax=cax3, orientation='horizontal')

cb1.set_label('Slab Depth [km]', fontsize=14)
cb2.set_label('Magnitude', fontsize=14)
cb3.set_label('Bathymetry (exaggerated x 10) [km]', fontsize=14)

cb1.ax.tick_params(labelsize=12)
cb2.ax.tick_params(labelsize=12)
cb3.ax.tick_params(labelsize=12)

plt.tight_layout()
plt.show()



# Interactive 3D plot in the web

# surface = go.Surface(
#     x=LON, y=LAT, z=DEPTH,
#     colorscale='Viridis', opacity=0.7,
#     colorbar=dict(title='Slab Depth (km)')
# )

# scatter = go.Scatter3d(
#     x=eq_lons, y=eq_lats, z=eq_depths,
#     mode='markers',
#     marker=dict(
#         size=np.clip(eq_mags ** 3, 5, 30),
#         color=eq_mags,
#         colorscale='Plasma',
#         colorbar=dict(title='Magnitude'),
#         line=dict(width=1, color='black'),
#         opacity=0.9,
#     ),
#     name='Earthquakes'
# )

# layout = go.Layout(
#     title="3D View: Slab and Earthquakes (within ±5 km of slab)",
#     scene=dict(
#         xaxis=dict(title='Longitude'),
#         yaxis=dict(title='Latitude'),
#         zaxis=dict(title='Depth (km)', autorange='reversed'),
#     ),
#     height=800,
#     width=1000
# )
# fig = go.Figure(data=[surface, scatter], layout=layout)
# fig.show()

print(shp.crs)