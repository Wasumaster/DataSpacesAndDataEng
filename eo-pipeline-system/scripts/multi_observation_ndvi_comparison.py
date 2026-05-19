import os
import numpy as np
import rasterio
from rasterio.transform import from_origin
import matplotlib.pyplot as plt

OUTPUT_DIR = "results/ndvi_comparison"
REPORT_FILE = "reports/multi_observation_ndvi_comparison.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("reports", exist_ok=True)
os.makedirs("assets/bands", exist_ok=True)

def create_sample_observation(name, cloud_level):
    width, height = 300, 300
    transform = from_origin(19.0, 51.0, 10, 10)
    
    red = np.random.normal(1200, 250, (height, width))
    nir = np.random.normal(2500, 500, (height, width))
    
    if cloud_level == "high":
        cloud_pct = "75%"
        cloud_mask = np.random.rand(height, width) < 0.75
    else:
        cloud_pct = "5%"
        cloud_mask = np.random.rand(height, width) < 0.05
        
    red[cloud_mask] = np.random.normal(8000, 500, np.sum(cloud_mask))
    nir[cloud_mask] = np.random.normal(8200, 500, np.sum(cloud_mask))

    profile = {
        "driver": "GTiff", "height": height, "width": width,
        "count": 1, "dtype": "float32", "crs": "EPSG:4326",
        "transform": transform
    }
    
    red_path = f"assets/bands/{name}_red.tif"
    nir_path = f"assets/bands/{name}_nir.tif"
    
    with rasterio.open(red_path, "w", **profile) as dst:
        dst.write(red.astype("float32"), 1)
    with rasterio.open(nir_path, "w", **profile) as dst:
        dst.write(nir.astype("float32"), 1)
        
    return red_path, nir_path, cloud_pct

def compute_ndvi(red_path, nir_path):
    with rasterio.open(red_path) as r:
        red = r.read(1).astype(float)
    with rasterio.open(nir_path) as n:
        nir = n.read(1).astype(float)
    return (nir - red) / (nir + red + 1e-6)

def save_ndvi_map(ndvi, output_path, title):
    plt.figure(figsize=(8, 6))
    plt.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
    plt.colorbar(label='NDVI')
    plt.title(title)
    plt.savefig(output_path)
    plt.close()

def get_stats(ndvi):
    return {
        "min": np.min(ndvi),
        "max": np.max(ndvi),
        "mean": np.mean(ndvi),
        "high_veg": np.sum(ndvi > 0.5),
        "low_ndvi": np.sum(ndvi < 0)
    }

low_red, low_nir, low_pct = create_sample_observation("low_cloud", "low")
high_red, high_nir, high_pct = create_sample_observation("high_cloud", "high")

ndvi_low = compute_ndvi(low_red, low_nir)
ndvi_high = compute_ndvi(high_red, high_nir)

save_ndvi_map(ndvi_low, f"{OUTPUT_DIR}/low_cloud_observation_ndvi_map.png", "Low Cloud NDVI")
save_ndvi_map(ndvi_high, f"{OUTPUT_DIR}/high_cloud_observation_ndvi_map.png", "High Cloud NDVI")

stats_low = get_stats(ndvi_low)
stats_high = get_stats(ndvi_high)

with open(REPORT_FILE, "w") as f:
    f.write("MULTI-OBSERVATION NDVI COMPARISON\n")
    f.write("=================================\n\n")
    
    f.write("low_cloud_observation\n")
    f.write("---------------------\n")
    f.write(f"Cloud cover: {low_pct}\n")
    f.write(f"NDVI min: {stats_low['min']:.2f}\n")
    f.write(f"NDVI max: {stats_low['max']:.2f}\n")
    f.write(f"NDVI mean: {stats_low['mean']:.2f}\n")
    f.write(f"High vegetation pixels: {stats_low['high_veg']}\n")
    f.write(f"Low NDVI pixels: {stats_low['low_ndvi']}\n\n")

    f.write("high_cloud_observation\n")
    f.write("----------------------\n")
    f.write(f"Cloud cover: {high_pct}\n")
    f.write(f"NDVI min: {stats_high['min']:.2f}\n")
    f.write(f"NDVI max: {stats_high['max']:.2f}\n")
    f.write(f"NDVI mean: {stats_high['mean']:.2f}\n")
    f.write(f"High vegetation pixels: {stats_high['high_veg']}\n")
    f.write(f"Low NDVI pixels: {stats_high['low_ndvi']}\n\n")

    f.write("ENGINEERING COMPARISON\n")
    f.write("----------------------\n")
    f.write("The low-cloud observation provides a clearer and more useful NDVI result.\n")
    f.write("The high-cloud observation is operationally less reliable because clouds\n")
    f.write("reduce interpretability and may hide the real surface signal.\n\n")
    f.write("Recommended observation:\n")
    f.write("low_cloud_observation\n\n")
    f.write("--- ANSWERS TO ENGINEERING QUESTIONS ---\n")
    f.write("1. Which observation has better NDVI quality? Low-cloud observation.\n")
    f.write("2. Which observation appears more affected by clouds? High-cloud observation.\n")
    f.write("3. Which observation should be selected for operational monitoring? low_cloud_observation.\n")
    f.write("4. Why is the high-cloud observation less reliable? Clouds are highly reflective in both Red and NIR bands, dragging the NDVI math towards zero and hiding the surface.\n")
    f.write("5. Would this difference matter for AI-based vegetation classification? Yes. AI models trained on cloudy scenes will classify clouds instead of terrain, producing garbage outputs. Metadata filtering is strictly necessary.\n")

print("COMPARISON COMPLETE")
print("Generated files:")
print(f" - {OUTPUT_DIR}/low_cloud_observation_ndvi_map.png")
print(f" - {OUTPUT_DIR}/high_cloud_observation_ndvi_map.png")
print(f" - {REPORT_FILE}")
