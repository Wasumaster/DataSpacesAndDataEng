import os
import numpy as np
import matplotlib.pyplot as plt

NDVI_PATH = "results/ndvi/ndvi.npy"
MASK_NPY_OUTPUT = "results/ndvi/water_mask.npy"
MASK_PNG_OUTPUT = "results/ndvi/water_mask.png"
REPORT_FILE = "reports/water_detection.txt"

if not os.path.exists(NDVI_PATH):
    print("ERROR: NDVI file not found.")
    exit()

ndvi = np.load(NDVI_PATH)

water_mask = ndvi < 0

water_pixels = int(np.sum(water_mask))
total_pixels = ndvi.size
non_water_pixels = total_pixels - water_pixels
water_percentage = (water_pixels / total_pixels) * 100

np.save(MASK_NPY_OUTPUT, water_mask)

plt.figure(figsize=(10, 8))
plt.imshow(water_mask, cmap='Blues')
plt.colorbar(label='Water Candidate')
plt.title("Water Detection Mask (NDVI < 0)")
plt.savefig(MASK_PNG_OUTPUT)
plt.close()

print("WATER DETECTION")
print("=" * 50)
print("Loading NDVI...")
print("Generating binary mask...")
print(f"Water candidate pixels: {water_pixels}")
print(f"Non-water pixels: {non_water_pixels}")
print("\nFILES GENERATED:")
print("-" * 16)
print(MASK_NPY_OUTPUT)
print(MASK_PNG_OUTPUT)
print(REPORT_FILE)

with open(REPORT_FILE, "w") as f:
    f.write("WATER DETECTION REPORT\n")
    f.write("======================\n\n")
    f.write("Detection rule:\n")
    f.write("NDVI < 0\n\n")
    f.write("Pixel statistics:\n")
    f.write(f"Water candidate pixels: {water_pixels}\n")
    f.write(f"Non-water pixels: {non_water_pixels}\n")
    f.write(f"Water candidate percentage: {water_percentage:.2f}%\n\n")
    f.write("Interpretation:\n")
    if water_percentage < 15:
        f.write("Small number of low-NDVI areas detected.\n")
    else:
        f.write("Significant number of low-NDVI areas detected.\n")
    f.write("\nPotential explanations:\n")
    f.write("- water surfaces\n")
    f.write("- shadows\n")
    f.write("- urban regions\n\n")
    
    f.write("=== ENGINEERING INTERPRETATION ===\n")
    f.write("1. NDVI < 0 may indicate water because water strongly absorbs near-infrared radiation.\n")
    f.write("2. NDVI alone is insufficient for reliable water detection. Shadows, dense urban centers, and thick clouds can also yield negative NDVI.\n")
    f.write("3. Additional bands (like Short-Wave Infrared - SWIR) and specialized indices (like NDWI - Normalized Difference Water Index) are required to separate water from shadows.\n")
    f.write("4. Simple threshold-based products (like this one) are frequently used as rapid preprocessing steps to mask out irrelevant data before feeding images into heavy AI segmentation models.\n")
