import os
import numpy as np
import rasterio
from rasterio.transform import from_origin
import matplotlib.pyplot as plt

OUTPUT_DIR = "results/ndvi_timeseries"
REPORT_FILE = "reports/time_series_ndvi_monitoring.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("reports", exist_ok=True)
os.makedirs("assets/bands", exist_ok=True)

def create_sample_observation(name, nir_mean):
    width, height = 300, 300
    transform = from_origin(19.0, 51.0, 10, 10)
    
    red = np.random.normal(1200, 250, (height, width))
    nir = np.random.normal(nir_mean, 500, (height, width))
    
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
        
    return red_path, nir_path

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

observations = [
    {"date": "2024-04-01", "nir_mean": 2600},
    {"date": "2024-05-01", "nir_mean": 3400},
    {"date": "2024-06-01", "nir_mean": 4300}
]

dates = []
means = []
report_lines = []

print("Processing:")

for obs in observations:
    date = obs["date"]
    name = f"observation_{date.replace('-', '_')}"
    red_p, nir_p = create_sample_observation(name, obs["nir_mean"])
    
    ndvi = compute_ndvi(red_p, nir_p)
    mean_val = np.mean(ndvi)
    
    dates.append(date)
    means.append(mean_val)
    
    map_path = f"{OUTPUT_DIR}/{name}_ndvi_map.png"
    save_ndvi_map(ndvi, map_path, f"NDVI Map - {date}")
    
    print(name)
    print(f"Mean NDVI: {mean_val:.2f}")
    
    report_lines.append(f"{date}\nMean NDVI: {mean_val:.2f}\n")

plt.figure(figsize=(8, 5))
plt.plot(dates, means, marker="o", linestyle="-", color="green")
plt.title("Mean NDVI Trend")
plt.xlabel("Date")
plt.ylabel("Mean NDVI")
plt.grid(True)
trend_plot_path = f"{OUTPUT_DIR}/mean_ndvi_trend.png"
plt.savefig(trend_plot_path)
plt.close()

first_mean = means[0]
last_mean = means[-1]
change = last_mean - first_mean

if change > 0.05:
    trend = "Increasing vegetation activity"
elif change < -0.05:
    trend = "Decreasing vegetation activity"
else:
    trend = "Stable vegetation conditions"

with open(REPORT_FILE, "w") as f:
    f.write("TIME-SERIES NDVI MONITORING REPORT\n")
    f.write("==================================\n\n")
    for line in report_lines:
        f.write(line + "\n")
    
    f.write("Vegetation trend:\n")
    f.write("-----------------\n")
    f.write(f"First mean NDVI: {first_mean:.2f}\n")
    f.write(f"Last mean NDVI: {last_mean:.2f}\n")
    f.write(f"Change: {change:+.2f}\n")
    f.write("Detected trend:\n")
    f.write(f"{trend}\n\n")
    
    f.write("=== ENGINEERING INTERPRETATION ===\n")
    f.write("1. Increasing NDVI usually indicates a stronger vegetation response (e.g., spring/summer growth phase of crops or forests).\n")
    f.write("2. Decreasing NDVI may indicate drought, disease, deforestation, harvest time, or seasonal leaf fall in autumn.\n")
    f.write("3. Stable NDVI suggests limited temporal change (characteristic of dense evergreen forests, bare soil, or urban infrastructure).\n")
    f.write("4. Time-series EO analysis provides significantly more information than a single observation because it captures dynamic ecosystem behaviors and enables proactive environmental monitoring.\n")

print("\nTIME-SERIES NDVI MONITORING COMPLETE")
print("Generated files:")
print(f" - {OUTPUT_DIR}/observation_2024_04_01_ndvi_map.png")
print(f" - {OUTPUT_DIR}/observation_2024_05_01_ndvi_map.png")
print(f" - {OUTPUT_DIR}/observation_2024_06_01_ndvi_map.png")
print(f" - {trend_plot_path}")
print(f" - {REPORT_FILE}")
