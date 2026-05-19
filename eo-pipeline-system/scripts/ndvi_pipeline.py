import rasterio
import numpy as np
import matplotlib.pyplot as plt

with rasterio.open("assets/bands/B04_10m.tif") as red_src:
    red = red_src.read(1).astype(float)

with rasterio.open("assets/bands/B08_10m.tif") as nir_src:
    nir = nir_src.read(1).astype(float)

ndvi = (nir - red) / (nir + red + 1e-6)

ndvi_min = np.min(ndvi)
ndvi_max = np.max(ndvi)
ndvi_mean = np.mean(ndvi)
veg_pixels = np.sum(ndvi > 0.5)
water_pixels = np.sum(ndvi < 0)

np.save("results/ndvi/ndvi.npy", ndvi)

plt.figure(figsize=(8, 6))
plt.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
plt.colorbar(label='NDVI')
plt.title("NDVI Map (Simulated Data)")
plt.savefig("results/ndvi/ndvi_map.png")
plt.close()

report_path = "reports/ndvi_report.txt"
with open(report_path, "w") as f:
    f.write(f"NDVI MIN: {ndvi_min:.2f}\n")
    f.write(f"NDVI MAX: {ndvi_max:.2f}\n")
    f.write(f"NDVI MEAN: {ndvi_mean:.2f}\n")
    f.write(f"Pixels with NDVI > 0.5: {veg_pixels}\n")
    f.write(f"Pixels with NDVI < 0: {water_pixels}\n")

print(f"NDVI MIN: {ndvi_min:.2f}")
print(f"NDVI MAX: {ndvi_max:.2f}")
print("NDVI array saved to: results/ndvi/ndvi.npy")
print("NDVI map saved to: results/ndvi/ndvi_map.png")
print("Report saved to: reports/ndvi_report.txt")

