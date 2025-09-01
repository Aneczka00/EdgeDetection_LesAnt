# Full Random Forest Pipeline using GeoTIFF grid
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

# -------------------------------
# 1. LOAD XYZ GRAVITY DATA
# -------------------------------
ba = pd.read_csv("C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/C_Bouguer_full_MBES.xyz", delim_whitespace=True, header=None, names=["X", "Y", "Z"])
bp = pd.read_csv("C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/C_Bouguer_full_MBES_bandpass.xyz", delim_whitespace=True, header=None, names=["X", "Y", "Z"])
# vg = pd.read_csv("C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/VG_full_MBES_bandpass.xyz", delim_whitespace=True, header=None, names=["X", "Y", "Z"])
td = pd.read_csv("C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/TD_full_MBES_bandpass.xyz", delim_whitespace=True, header=None, names=["X", "Y", "Z"])


# Clean up
for df in [ba, bp, td]:
    df["Z"] = pd.to_numeric(df["Z"], errors="coerce")
    df.dropna(subset=["Z"], inplace=True)
    print(df.dtypes)

# -------------------------------
# 2. LOAD BATHYMETRY FROM GeoTIFF
# -------------------------------
bathy_path = "C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/ML_Bathymetry.tif"
with rasterio.open(bathy_path) as src:
    bathy_array = src.read(1).astype(np.float32)
    bathy_array[bathy_array == src.nodata] = np.nan
    transform = src.transform
    height, width = bathy_array.shape
    minx = transform.c
    maxx = transform.c + width * transform.a
    maxy = transform.f
    miny = transform.f + height * transform.e 
    x_coords = np.arange(width) * transform.a + transform.c
    y_coords = np.arange(height) * transform.e + transform.f
    xx, yy = np.meshgrid(x_coords, y_coords)

print(f"Bathy Grid Shape: {bathy_array.shape}")

# -------------------------------
# 3. INTERPOLATE GRAVITY TO BATHY GRID
# -------------------------------
bp_path = "C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/interpolated_bp_on_bathy.npy"
# vg_path = "C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/interpolated_vg_on_bathy.npy"
td_path = "C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/interpolated_td_on_bathy.npy"
ba_path = "C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/interpolated_ba_on_bathy.npy"

def interpolate_to_grid(df, grid_x, grid_y, method="linear"):
    return griddata((df["X"], df["Y"]), df["Z"], (grid_x, grid_y), method=method)

if os.path.exists(bp_path) and os.path.exists(ba_path) and os.path.exists(td_path):
    print("Loading interpolated BA, BP, TD, and VG from .npy files...")
    ba_grid = np.load(ba_path)
    bp_grid = np.load(bp_path)
    # vg_grid = np.load(vg_path)
    td_grid = np.load(td_path)

else:
    print("Interpolating gravity data to bathy grid...")
    ba_grid = interpolate_to_grid(ba, xx, yy)
    bp_grid = interpolate_to_grid(bp, xx, yy)
    # vg_grid = interpolate_to_grid(vg, xx, yy)
    td_grid = interpolate_to_grid(td, xx, yy)

    np.save(ba_path, ba_grid)
    np.save(bp_path, bp_grid)
    # np.save(vg_path, vg_grid)
    np.save(td_path, td_grid)
    print("Saved interpolated grids.")

# -------------------------------
# 4. STACK FEATURES
# -------------------------------
print("ba_grid", ba_grid.shape)
print("bp_grid", bp_grid.shape)
# print("vg_grid", vg_grid.shape)
print("td_grid", td_grid.shape)
# print("bathy_array:", bathy_array.shape)

features = np.stack([ba_grid, bp_grid, td_grid, bathy_array], axis=-1)
X_rf = features.reshape(-1, 4)

# -------------------------------
# 5. RASTERIZE SHAPEFILE FOR LABELS
# -------------------------------
with fiona.open("C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/shapefiles/VD_full_MBES_contours_00001_lnz.shp", "r") as shp:
    shapes = [shape(feat["geometry"]) for feat in shp]

label_mask = rasterize(
    [(geom, 1) for geom in shapes],
    out_shape=(height, width),
    transform=transform,
    fill=0,
    dtype=np.uint8
)
y_rf = label_mask.flatten()

# -------------------------------
# 6. FILTER INVALID DATA
# -------------------------------
X_rf = X_rf.astype(np.float32)
valid_mask = ~np.any(np.isnan(X_rf), axis=1)
X_clean = X_rf[valid_mask]
y_clean = y_rf[valid_mask]

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

# Plot feature importances
feature_names = ["Bouguer", "Bandpass", "Tilt Derivative", "Bathymetry"]
sns.barplot(x=rf.feature_importances_, y=feature_names)
plt.title("Feature Importance")
plt.tight_layout()
plt.show()

# Save model
save_dir = "C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/result_n2_v1"
os.makedirs(save_dir, exist_ok=True)
joblib.dump(rf, os.path.join(save_dir, "random_forest_edge_detector_fulllllllll.pkl"))

import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.transform import from_origin
import joblib

# Load model
rf = joblib.load("C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/result_n2_v1/random_forest_edge_detector_fulllllllll.pkl")

# Predict full-resolution edge probabilities
proba_map = rf.predict_proba(X_clean)[:, 1]  # Edge probability
proba_grid = np.full((height * width,), np.nan, dtype=np.float32)
proba_grid[valid_mask] = proba_map
proba_grid = proba_grid.reshape((height, width))

# Plot edge probability map
plt.figure(figsize=(10, 10)) 
plt.imshow(proba_grid, cmap="inferno", origin="upper", extent=[minx, maxx, miny, maxy])

cbar = plt.colorbar()
cbar.set_label("Edge Probability", fontsize=17)
cbar.ax.tick_params(labelsize=15)

# plt.title("Predicted Edge Probability Map (Random Forest, Full Resolution)", fontsize=18)
plt.xlabel("X (UTM 20N)", fontsize=17)
plt.ylabel("Y (UTM 20N)", fontsize=17)

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.tight_layout()
plt.show()

# Export to GeoTIFF
geotiff_path = "C:/Users/aczachor/Desktop/MACHINE LEARNING/source data/result_n2_v1/predicted_edge_probability_rf_full_td_vg_vg.tif"
with rasterio.open(
    geotiff_path, "w",
    driver="GTiff",
    height=proba_grid.shape[0],
    width=proba_grid.shape[1],
    count=1,
    dtype=proba_grid.dtype,
    crs="EPSG:32620",
    transform=transform
) as dst:
    dst.write(proba_grid, 1)

print("✅ Exported full-resolution edge probability map to:")
print(geotiff_path)

