import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import xarray as xr
import geopandas as gpd
from shapely.geometry import Point

# =========================
# Domain
# =========================
slab_domain = {
    "lon_min": -65, "lon_max": -55,
    "lat_min": 9, "lat_max": 20
}

# =========================
# Load slab
# =========================
slab_ds = xr.open_dataset("E:/Ania/Earthquakes/lesser_antilles_slab_BIE-ET-AL.grd", engine="netcdf4")
slab_var = list(slab_ds.data_vars)[0]
slab = slab_ds[slab_var]

slab_lons = slab_ds['x'].values
slab_lats = slab_ds['y'].values
LON, LAT = np.meshgrid(slab_lons, slab_lats)
DEPTH = slab.values  # already in km

# =========================
# Load earthquakes
# =========================
df = pd.read_csv(
    "E:/Ania/Earthquakes/Seismicity_IPGP/Massin_only_Johanna.csv",
    sep=";", engine="python"
)
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
# Load bathymetry
# =========================
bathy_ds = xr.open_dataset("E:/Ania/M2_QGIS_Project/DATA/Bathy/GEBCO_22_Apr_2025_131f4cc381e2/GEBCO_22_Apr_2025_131f4cc381e2/gebco_2024_n25.9365_s-3.7705_w-93.252_e-33.3105.nc")
bathy_var = list(bathy_ds.data_vars)[0]
bathy = bathy_ds[bathy_var]

y_vals = bathy['lat'].values
# Ensure latitude slice works correctly
lat_min, lat_max = slab_domain["lat_min"], slab_domain["lat_max"]

if y_vals[0] > y_vals[-1]:  # descending
    y_slice = slice(lat_max, lat_min)
else:  # ascending
    y_slice = slice(lat_min, lat_max)

bathy_cropped = bathy.sel(
    lon=slice(slab_domain["lon_min"], slab_domain["lon_max"]),
    lat=slice(lat_min, lat_max)   # small buffer
)

# Extract arrays
BATHY_LON, BATHY_LAT = np.meshgrid(
    bathy_cropped['lon'].values,
    bathy_cropped['lat'].values
)
BATHY_Z = bathy_cropped.values / 1000.0  # meters -> km (no exaggeration)

# =========================
# 2D Map Plot with legend
# =========================
fig, ax = plt.subplots(figsize=(10, 8))

from matplotlib.colors import LogNorm, PowerNorm

# Slab depth raster
slab_img = ax.pcolormesh(
    LON, LAT, DEPTH,
    cmap="cividis",
    shading="auto",
    norm=PowerNorm(gamma=0.5)  # adjust range as needed
)



from mpl_toolkits.axes_grid1 import make_axes_locatable

cb1 = fig.colorbar(slab_img, ax=ax, orientation="vertical", fraction=0.035, pad=0.08)
cb1.set_label("Slab Depth [km]", fontsize=15)

bathy_img = ax.pcolormesh(
    BATHY_LON, BATHY_LAT, -BATHY_Z,
    cmap="terrain_r",     # instead of "terrain_r"
    shading="auto",
    alpha=0.4,
    vmin=-2, vmax=8,     # enforce range 0–8 km
    zorder=2
)

contours = ax.contour(
    BATHY_LON, BATHY_LAT, -BATHY_Z,
    levels=np.arange(0, np.nanmax(-BATHY_Z), 1),  # every 1 km
    colors="k", linewidths=0.5, alpha=0.6, zorder=3
)
ax.clabel(contours, inline=True, fontsize=8, fmt="%.0f km")

cb0 = fig.colorbar(bathy_img, ax=ax, orientation="vertical", fraction=0.035, pad=0.05)
cb0.set_label("Water depth [km]", fontsize=15)
cb0.ax.invert_yaxis()

# Earthquakes
sc = ax.scatter(
    df_near_slab["longitude"], 
    df_near_slab["latitude"], 
    c=df_near_slab["magnitude"], 
    cmap="plasma", 
    s=np.clip(df_near_slab["magnitude"].values ** 3, 5, 100), 
    edgecolor="k", 
    alpha=0.8,
    zorder=3
)

# ----------------------------
# Bubble (size) legend
# ----------------------------
import matplotlib.lines as mlines
from matplotlib import cm


cmap = cm.plasma
norm = plt.Normalize(vmin=df_near_slab["magnitude"].min(), vmax=df_near_slab["magnitude"].max())

ranges = [(df_near_slab["magnitude"].min(), 4),   # small
          (4, 6),                                  # medium
          (6, df_near_slab["magnitude"].max())]   # large

# Representative values for size scaling (midpoints)
rep_values = [(low + high)/2 for low, high in ranges]

# Scale sizes for legend, without clipping
# Use the same scaling factor as your scatter plot
# Adjust the factor if needed so dots are visually distinct
size_vals = [v**3 for v in rep_values]  



cb2 = fig.colorbar(sc, ax=ax, orientation="vertical", fraction=0.035, pad=0.08)
cb2.set_label("Magnitude", fontsize=15)

# Shapefiles with labels for legend
shp_labels = ["CJL (Lesourd-Laux et al., 2025)", "Fracture Zones", "Anomaly A"]
shp_colors = ["red", "yellow", "violet"]

for i_shp, coords_list in enumerate(all_coords_list):
    color = shp_colors[i_shp % len(shp_colors)]
    label = shp_labels[i_shp]
    for j, (x, y) in enumerate(coords_list):
        # Only add label once per shapefile group (avoid duplicates)
        if j == 0:
            ax.plot(x, y, color=color, linewidth=2, zorder=2, label=label)
        else:
            ax.plot(x, y, color=color, linewidth=2, zorder=2)

# Labels and limits
ax.set_xlabel("Longitude", fontsize=20)
ax.set_ylabel("Latitude", fontsize=20)
ax.tick_params(axis="both", labelsize=16)

ax.set_xlim(slab_domain["lon_min"], slab_domain["lon_max"])
ax.set_ylim(slab_domain["lat_min"], slab_domain["lat_max"])


# Add shapefile legend
ax.legend(fontsize=15, title_fontsize=18, loc="upper right")
# Create a tiny figure just for the size legend
fig, ax = plt.subplots(figsize=(2, 5))  # wide and short

# Create empty scatter points (white fill, black edge)
handles = [
    ax.scatter([], [], s=size, edgecolor="k", facecolor="white")
    for size in size_vals
]
labels = [f"M {low:.1f}-{high:.1f}" for low, high in ranges[:-1]] + ["M 6≤"]

# Add legend
ax.legend(
    handles, labels,
    scatterpoints=1,
    title="Magnitude (size)",
    fontsize=12,
    title_fontsize=14,
    ncol=1,                # single column → vertical
    frameon=True,
    loc="center"
)

# Remove axes
ax.axis("off")

plt.tight_layout()
plt.show()


print("GEBCO lat range:", bathy['y'].min().values, "to", bathy['y'].max().values)
print("GEBCO lon range:", bathy['x'].min().values, "to", bathy['x'].max().values)
