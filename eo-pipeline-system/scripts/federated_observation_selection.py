import os
import requests

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/search"
AOI = [19.0, 50.0, 20.0, 51.0]
TIME_WINDOW = "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z"
REPORT_FILE = "reports/federated_observation_selection.txt"

os.makedirs("reports", exist_ok=True)

QUERIES = {
    "Sentinel-2 Optical": {
        "collections": ["sentinel-2-l2a"],
        "bbox": AOI,
        "datetime": TIME_WINDOW,
        "limit": 5
    },
    "Sentinel-1 SAR": {
        "collections": ["sentinel-1-grd"],
        "bbox": AOI,
        "datetime": TIME_WINDOW,
        "limit": 5
    }
}

def query_stac(query):
    response = requests.post(STAC_URL, json=query, timeout=30)
    response.raise_for_status()
    return response.json().get("features", [])

def summarize_item(item):
    props = item.get("properties", {})
    assets = item.get("assets", {})
    return {
        "id": item.get("id"),
        "datetime": props.get("datetime"),
        "cloud_cover": props.get("eo:cloud_cover"),
        "assets_count": len(assets),
        "platform": props.get("platform"),
        "constellation": props.get("constellation"),
        "instrument": props.get("instruments")
    }

def compute_sensor_score(sensor_name, items, scenario):
    if not items:
        return 0
    
    score = min(len(items), 5) * 10
    
    if sensor_name == "Sentinel-2 Optical":
        avg_cloud = 0
        valid_clouds = [i["cloud_cover"] for i in items if i["cloud_cover"] is not None]
        if valid_clouds:
            avg_cloud = sum(valid_clouds) / len(valid_clouds)
            
        if scenario == "normal":
            score += max(0, 100 - avg_cloud)
        elif scenario == "cloudy":
            score += max(0, 40 - avg_cloud)
        elif scenario == "night":
            score -= 10
            
    elif sensor_name == "Sentinel-1 SAR":
        if scenario == "normal":
            score += 50
        elif scenario == "cloudy":
            score += 80
        elif scenario == "night":
            score += 80
            
    return score

def select_best_sensor(summaries, scenario):
    best_sensor = None
    best_score = -1
    scores = {}
    
    for sensor, items in summaries.items():
        score = compute_sensor_score(sensor, items, scenario)
        scores[sensor] = score
        if score > best_score:
            best_score = score
            best_sensor = sensor
            
    return best_sensor, scores

summaries = {}
print("FEDERATED OBSERVATION SELECTION")
print("=" * 60)

for sensor_name, query in QUERIES.items():
    print(f"Querying: {sensor_name}")
    features = query_stac(query)
    print(f"{sensor_name} products: {len(features)}")
    summaries[sensor_name] = [summarize_item(f) for f in features]

scenarios = ["normal", "cloudy", "night"]
report_lines = []

for scenario in scenarios:
    best_sensor, scores = select_best_sensor(summaries, scenario)
    report_lines.append(f"Scenario: {scenario}")
    report_lines.append(f"Recommended sensor: {best_sensor}")
    report_lines.append("Scores:")
    for s_name, s_val in scores.items():
        report_lines.append(f" - {s_name}: {s_val:.2f}")
    report_lines.append("")

with open(REPORT_FILE, "w") as f:
    f.write("FEDERATED OBSERVATION SELECTION REPORT\n")
    f.write("======================================\n\n")
    f.write("Sensors compared:\n")
    f.write("- Sentinel-2 Optical\n")
    f.write("- Sentinel-1 SAR\n\n")
    f.write("Scenario-based sensor selection:\n")
    f.write("-" * 32 + "\n")
    for line in report_lines:
        f.write(line + "\n")
    
    f.write("=== ENGINEERING INTERPRETATION ===\n")
    f.write("1. Sentinel-2 (Optical) is heavily preferred for vegetation (NDVI) and visual interpretation under clear, daylight conditions.\n")
    f.write("2. Sentinel-2 becomes unreliable under cloudy conditions and is completely blind during night-time passes (requires solar illumination).\n")
    f.write("3. Sentinel-1 SAR (Synthetic Aperture Radar) is prioritized during cloudy weather and night operations because microwave pulses penetrate clouds and do not rely on the sun.\n")
    f.write("4. Federated observation selection significantly improves mission robustness by guaranteeing continuous data flow regardless of local weather and planetary rotation.\n")

print("\nFEDERATED SELECTION COMPLETE")
print(f"REPORT SAVED TO: {REPORT_FILE}")
