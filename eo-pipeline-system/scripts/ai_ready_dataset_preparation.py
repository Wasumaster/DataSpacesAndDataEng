import os
import json
import shutil

DATASET_DIR = "dataset"
IMAGES_DIR = "dataset/images"
METADATA_DIR = "dataset/metadata"

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

FILES_TO_INCLUDE = {
    "ndvi_map": "results/ndvi/ndvi_map.png",
    "water_mask": "results/ndvi/water_mask.png",
    "observation_low_cloud": "results/ndvi_comparison/low_cloud_observation_ndvi_map.png",
    "observation_high_cloud": "results/ndvi_comparison/high_cloud_observation_ndvi_map.png",
    "time_series_trend": "results/ndvi_timeseries/mean_ndvi_trend.png"
}

synthetic_observations = [
    {"id": "OBS_001", "cloud_cover": 5, "mean_ndvi": 0.62, "sensor": "Sentinel-2"},
    {"id": "OBS_002", "cloud_cover": 18, "mean_ndvi": 0.44, "sensor": "Sentinel-2"},
    {"id": "OBS_003", "cloud_cover": 68, "mean_ndvi": 0.21, "sensor": "Sentinel-2"}
]

def determine_quality(cloud_cover, mean_ndvi):
    if cloud_cover <= 10 and mean_ndvi >= 0.5:
        return "excellent", "AI_READY", "LOW"
    elif cloud_cover <= 30 and mean_ndvi >= 0.3:
        return "good", "AI_READY", "MODERATE"
    else:
        return "limited", "NOT_SUITABLE", "HIGH"

print("AI-READY EO DATASET PREPARATION")
print("=" * 60)

quality_distribution = {"excellent": 0, "good": 0, "limited": 0}

for obs in synthetic_observations:
    obs_id = obs["id"]
    quality, suitability, cloud_cond = determine_quality(obs["cloud_cover"], obs["mean_ndvi"])
    quality_distribution[quality] += 1
    
    selected_assets = []
    for key, path in FILES_TO_INCLUDE.items():
        if os.path.exists(path):
            dest_filename = f"{obs_id}_{key}.png"
            dest_path = os.path.join(IMAGES_DIR, dest_filename)
            shutil.copy2(path, dest_path)
            selected_assets.append(dest_path)
            print(f"COPIED: {dest_path}")
        else:
            if obs_id == "OBS_001":
                print(f"MISSING: {path}")

    metadata = {
        "observation_id": obs_id,
        "sensor": obs["sensor"],
        "cloud_cover": obs["cloud_cover"],
        "mean_ndvi": obs["mean_ndvi"],
        "quality": quality,
        "suitability": suitability,
        "selected_assets": selected_assets,
        "labels": {
            "vegetation_monitoring": suitability,
            "ai_training": suitability,
            "cloud_conditions": cloud_cond
        }
    }
    
    meta_path = os.path.join(METADATA_DIR, f"{obs_id}.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"METADATA CREATED: {meta_path}\n")

summary = {
    "dataset_size": len(synthetic_observations),
    "images_directory": IMAGES_DIR,
    "metadata_directory": METADATA_DIR,
    "quality_distribution": quality_distribution
}

summary_path = os.path.join(METADATA_DIR, "dataset_summary.json")
with open(summary_path, "w") as f:
    json.dump(summary, f, indent=4)

print("DATASET SUMMARY")
print("-" * 40)
print(f"Dataset size: {summary['dataset_size']}")
print(f"Excellent: {quality_distribution['excellent']}")
print(f"Good: {quality_distribution['good']}")
print(f"Limited: {quality_distribution['limited']}")

print("\nGENERATED STRUCTURE:")
print("-" * 19)
print("dataset/")
print("  images/")
print("  metadata/")
print("\nAI-READY DATASET COMPLETE")
