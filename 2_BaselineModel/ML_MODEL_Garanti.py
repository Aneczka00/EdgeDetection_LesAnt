# Full Random Forest Pipeline using BA grid alignment
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from shapely.geometry import shape
import fiona
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from scipy.interpolate import griddata
from rasterio.transform import rowcol

# -------------------------------
# 1. LOAD XYZ GRAVITY DATA
# -------------------------------
ba = pd.read_csv("C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/C_Bouguer_Garanti_MBES.xyz", 
                 delim_whitespace=True, header=None, names=["X", "Y", "Z"])
bp = pd.read_csv("C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/C_Bouguer_Garanti_MBES_bandpass.xyz", 
                 delim_whitespace=True, header=None, names=["X", "Y", "Z"])
vg = pd.read_csv("C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/VG_Garanti_MBES_bandpass.xyz", 
                 delim_whitespace=True, header=None, names=["X", "Y", "Z"])
# td = pd.read_csv("C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/TD_Garanti_MBES_bandpass.xyz", 
                # delim_whitespace=True, header=None, names=["X", "Y", "Z"])

# Clean up
for df in [ba, bp, vg]:
    df["Z"] = pd.to_numeric(df["Z"], errors="coerce")
    df.dropna(subset=["Z"], inplace=True)

# -------------------------------
# 2. LOAD BATHYMETRY AND INTERPOLATE TO BA POINTS
# -------------------------------
bathy_path = "C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/ML_Bathymetry.tif"
with rasterio.open(bathy_path) as src:
    bathy_array = src.read(1).astype(np.float32)
    bathy_array[bathy_array == src.nodata] = np.nan
    transform = src.transform
    height, width = bathy_array.shape
    x_coords = np.arange(width) * transform.a + transform.c
    y_coords = np.arange(height) * transform.e + transform.f
    xx, yy = np.meshgrid(x_coords, y_coords)

    bathy_points = np.column_stack((xx.flatten(), yy.flatten()))
    bathy_values = bathy_array.flatten()

# Interpolate bathymetry to BA locations
coords = ba[["X", "Y"]].values
bathy_on_ba = griddata(bathy_points, bathy_values, coords, method="linear")

# -------------------------------
# 3. INTERPOLATE OTHER FEATURES TO BA POINTS
# -------------------------------
def interpolate_to_points(source_df, target_coords, method="linear"):
    return griddata((source_df["X"], source_df["Y"]), source_df["Z"], target_coords, method=method)

interpolated_bp = interpolate_to_points(bp, coords)
interpolated_vg = interpolate_to_points(vg, coords)
# interpolated_td = interpolate_to_points(td, coords)
interpolated_ba = ba["Z"].values

# -------------------------------
# 4. STACK FEATURES
# -------------------------------
features = np.column_stack([
    interpolated_ba,
    interpolated_bp,
    # interpolated_td,
    interpolated_vg,
    bathy_on_ba
])
X_rf = features.astype(np.float32)

# -------------------------------
# 5. RASTERIZE SHAPEFILE FOR LABELS
# -------------------------------
with fiona.open("C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/shapefiles/HD_full_MBES_Garanti_contours_00001_lnz_lnz.shp", "r") as shp:
    shapes = [shape(feat["geometry"]) for feat in shp]

label_mask = rasterize(
    [(geom, 1) for geom in shapes],
    out_shape=(height, width),
    transform=transform,
    fill=0,
    dtype=np.uint8
)

# -------------------------------
# 6. FILTER VALID DATA & MAP LABELS TO BA COORDINATES
# -------------------------------
valid_mask = ~np.any(np.isnan(X_rf), axis=1)
X_clean = X_rf[valid_mask]
coords_clean = coords[valid_mask]

rows, cols = zip(*[rowcol(transform, x, y) for x, y in coords_clean])
rows = np.clip(rows, 0, height - 1)
cols = np.clip(cols, 0, width - 1)
y_clean = label_mask[rows, cols]

# -------------------------------
# 7. TRAIN RANDOM FOREST
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_clean, y_clean, test_size=0.2, stratify=y_clean, random_state=42
)

rf = RandomForestClassifier(n_estimators=50, max_depth=8, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

# -------------------------------
# 8. EVALUATION & EXPORT
# -------------------------------
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

feature_names = ["Bouguer", "Bandpass", "Vertical Gradient", "Bathymetry"]
sns.barplot(x=rf.feature_importances_, y=feature_names)
plt.title("Feature Importance")
plt.tight_layout()
plt.show()

save_dir = "C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/result_n2_v1"
os.makedirs(save_dir, exist_ok=True)
joblib.dump(rf, os.path.join(save_dir, "random_forest_edge_detector_full_Garanti11.pkl"))

# -------------------------------
# 9. PREDICT + PLOT BA REGION ONLY (NO FULL GRID)
# -------------------------------
proba_map = rf.predict_proba(X_clean)[:, 1]

# Build DataFrame for plotting
df_plot = pd.DataFrame({
    "X": coords_clean[:, 0],
    "Y": coords_clean[:, 1],
    "Prob": proba_map
})
df_plot.sort_values(by=["Y", "X"], inplace=True)

x_unique = np.sort(df_plot["X"].unique())
y_unique = np.sort(df_plot["Y"].unique())
proba_grid_small = df_plot.pivot(index="Y", columns="X", values="Prob").values

# Plot trimmed grid
plt.figure(figsize=(10, 10))
plt.imshow(proba_grid_small, cmap="inferno", origin="lower",
           extent=[x_unique.min(), x_unique.max(), y_unique.min(), y_unique.max()])
cbar = plt.colorbar()
cbar.set_label("Edge Probability", fontsize=17)
cbar.ax.tick_params(labelsize=15)
plt.xlabel("X (UTM 20N)", fontsize=17)
plt.ylabel("Y (UTM 20N)", fontsize=17)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.tight_layout()
plt.show()

# -------------------------------
# 10. OPTIONAL: EXPORT TO FULL GRID GeoTIFF (if needed)
# -------------------------------
# You can uncomment this if you'd like to still export a full-resolution GeoTIFF (mostly NaNs):
# proba_grid_full = np.full((height * width,), np.nan, dtype=np.float32)
# for p, r, c in zip(proba_map, rows, cols):
#     idx = r * width + c
#     proba_grid_full[idx] = p
# proba_grid_full = proba_grid_full.reshape((height, width))

# geotiff_path = os.path.join(save_dir, "predicted_edge_probability_rf_full_Garanti.tif")
# with rasterio.open(
#     geotiff_path, "w",
#     driver="GTiff",
#     height=proba_grid_full.shape[0],
#     width=proba_grid_full.shape[1],
#     count=1,
#     dtype=proba_grid_full.dtype,
#     crs="EPSG:32620",
#     transform=transform
# ) as dst:
#     dst.write(proba_grid_full, 1)

# print("✅ Exported full-resolution edge probability map to:")
# print(geotiff_path)

# TD and VD as input + diff TD shp - it seems that on a smaller area VD had the biggest impact, when on a bigger area it was tilt derivative 
# TD and VD as input + HD shp - bandpass and vg as the biggest features, td also contibuted
# TD and VD as input + VD shp - 

#VD as input VD as shapefile - 
# VD as input HD as shapefile  - 
#  VD as  input + diff TD shp - bardziej rozlazle, ogolnie takie same jak wcesnien efekty, vg the most imp, for bigger interval again the bandpass role increased
# TD as input + diff TD shp - 
# TD as input + HD shp - 
# TD as input + VD shp - 
