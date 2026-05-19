import os
import numpy as np
import matplotlib.pyplot as plt

NDVI_PATH = "results/ndvi/ndvi.npy"
OUTPUT_IMAGE = "results/ndvi/ndvi_map.png"
REPORT_FILE = "reports/ndvi_analysis.txt"

os.makedirs("results/ndvi", exist_ok=True)
os.makedirs("reports", exist_ok=True)

if not os.path.exists(NDVI_PATH):
    print("ERROR: File ndvi.npy not found.")
    exit()

ndvi = np.load(NDVI_PATH)

ndvi_min = float(np.min(ndvi))
ndvi_max = float(np.max(ndvi))
ndvi_mean = float(np.mean(ndvi))

high_vegetation_pixels = int(np.sum(ndvi > 0.5))
low_ndvi_pixels = int(np.sum(ndvi < 0))

plt.figure(figsize=(8, 6))
plt.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
plt.colorbar(label='NDVI')
plt.title("NDVI Map")
plt.savefig(OUTPUT_IMAGE)
plt.close()

print("NDVI VISUALIZATION")
print("=" * 50)
print(f"NDVI MIN: {ndvi_min:.2f}")
print(f"NDVI MAX: {ndvi_max:.2f}")
print(f"NDVI MEAN: {ndvi_mean:.2f}")
print(f"HIGH VEGETATION PIXELS: {high_vegetation_pixels}")
print(f"LOW NDVI PIXELS: {low_ndvi_pixels}")
print(f"NDVI MAP SAVED TO: {OUTPUT_IMAGE}")
print(f"ANALYSIS REPORT SAVED TO: {REPORT_FILE}")

with open(REPORT_FILE, "w") as f:
    f.write("=== NDVI ANALYSIS REPORT ===\n")
    f.write(f"Input file: {NDVI_PATH}\n")
    f.write(f"Visualization: {OUTPUT_IMAGE}\n\n")
    f.write(f"NDVI MIN: {ndvi_min:.2f}\n")
    f.write(f"NDVI MAX: {ndvi_max:.2f}\n")
    f.write(f"NDVI MEAN: {ndvi_mean:.2f}\n")
    f.write(f"High vegetation pixels (NDVI > 0.5): {high_vegetation_pixels}\n")
    f.write(f"Low NDVI pixels (NDVI < 0): {low_ndvi_pixels}\n\n")
    f.write("=== ENGINEERING INTERPRETATION ===\n")
    f.write("1. Vegetated areas: Regions with high NDVI values (>0.5), mapped in green colors on the visualization.\n")
    f.write("2. Non-vegetated areas: Regions with low or negative NDVI values, mapped in red/yellow colors.\n")
    f.write("3. Low-NDVI areas: In real scenarios, these would represent water bodies, shadows, or urban surfaces. Here, they represent the lower end of our synthetic data.\n")
    f.write("4. Cloud contamination: No direct cloud contamination can be confirmed because the input bands were synthetically generated for pipeline testing.\n")
