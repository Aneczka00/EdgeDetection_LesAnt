# === Script: interpolate_bathy_to_gravity_grid.py ===
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Step 1: Load bathymetry in UTM coordinates
print("Loading bathymetry data...")
data = np.load("combined_bathy_data.npz")
combined_x = data["combined_x"]
combined_y = data["combined_y"]
combined_depth = data["combined_depth"]


def check_crs_and_warn(x, y):
    if np.abs(x).max() <= 180 and np.abs(y).max() <= 90:
        print("❌ Input coordinates look like longitude/latitude. STOP — they are not projected.")
        return False
    elif np.abs(x).max() > 1e5 and np.abs(y).max() > 1e5:
        print("✅ Input coordinates look projected (e.g., UTM). Safe to proceed.")
        return True
    else:
        print("⚠️ Ambiguous coordinate values. Check CRS manually.")
        return False

# Example usage:
data = np.load("combined_bathy_data.npz")
x = data["combined_x"]
y = data["combined_y"]

check_crs_and_warn(x, y)


# Step 2: Load gravity grid (already in UTM Zone 20N)
print("Loading gravity grid...")
gravity_df = pd.read_csv(
    "C:/Users/aczachor/Desktop/gravity interpolated grid/interpolated_gravity_noOBS_Demarara_Garanti.xyz",
    delim_whitespace=True,
    names=["ID", "X", "Y", "Gravity"],
    dtype={"ID": int, "X": float, "Y": float, "Gravity": float},
    skiprows=1,
    engine="python"
)

grid_x = gravity_df["X"].values
grid_y = gravity_df["Y"].values

# Step 3: Create meshgrid
print("Creating meshgrid from gravity coordinates...")
unique_x = np.sort(np.unique(grid_x))
unique_y = np.sort(np.unique(grid_y))
xi, yi = np.meshgrid(unique_x, unique_y)

# Step 4: Interpolate
print("Interpolating bathymetry onto gravity grid...")
zi = griddata(
    points=(combined_x, combined_y),
    values=combined_depth,
    xi=(xi, yi),
    method="linear"
)

# Check how much is NaN
print(f"Total grid points: {zi.size}")
print(f"NaN values: {np.isnan(zi).sum()}")

# Step 5: Save as XYZ
print("Saving interpolated bathymetry grid to XYZ...")
xyz_output = np.column_stack((xi.flatten(), yi.flatten(), zi.flatten()))
xyz_output = xyz_output[~np.isnan(xyz_output).any(axis=1)]
np.savetxt("bathymetry_combined_on_gravity_grid.xyz", xyz_output, fmt="%.3f", delimiter=" ")

print("Exported: bathymetry_combined_on_gravity_grid.xyz")

# Step 6: Plot result
print("Plotting...")
plt.figure(figsize=(10, 8))
plt.pcolormesh(xi, yi, zi, shading="auto", cmap="viridis")
plt.colorbar(label="Interpolated Depth (m)")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.title("Bathymetry Interpolated onto Gravity Grid")
plt.tight_layout()
plt.show()
