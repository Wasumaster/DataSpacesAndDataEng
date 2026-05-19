import os
import requests
from datetime import datetime

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/search"
QUERY = {
    "collections": ["sentinel-2-l2a"],
    "bbox": [19.0, 50.0, 20.0, 51.0],
    "datetime": "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z",
    "limit": 10
}
REPORT_FILE = "reports/observation_ranking.txt"

os.makedirs("reports", exist_ok=True)

def parse_datetime(value):
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value)

def compute_cloud_score(cloud_cover):
    if cloud_cover is None:
        return 0
    return max(0, 100 - cloud_cover)

def compute_completeness_score(assets_count):
    if assets_count >= 30:
        return 30
    elif assets_count >= 20:
        return 20
    elif assets_count >= 10:
        return 10
    return 0

def compute_recency_score(acq_time, newest_time):
    if acq_time is None:
        return 0
    total_days = 30.0
    age_days = (newest_time - acq_time).total_seconds() / 86400.0
    return max(0, 20 - (age_days / total_days) * 20)

response = requests.post(STAC_URL, json=QUERY, timeout=30)
response.raise_for_status()
features = response.json().get("features", [])

if not features:
    print("No observations found.")
    exit()

parsed_features = []
valid_times = []

for item in features:
    dt_str = item.get("properties", {}).get("datetime")
    if dt_str:
        valid_times.append(parse_datetime(dt_str))

newest_time = max(valid_times) if valid_times else datetime.now(timezone.utc)

for item in features:
    props = item.get("properties", {})
    product_id = item.get("id")
    acq_time_str = props.get("datetime")
    cloud_cover = props.get("eo:cloud_cover")
    assets_count = len(item.get("assets", {}))
    
    acq_time = parse_datetime(acq_time_str) if acq_time_str else None
    
    c_score = compute_cloud_score(cloud_cover)
    a_score = compute_completeness_score(assets_count)
    r_score = compute_recency_score(acq_time, newest_time)
    
    final_score = c_score + a_score + r_score
    
    parsed_features.append({
        "id": product_id,
        "time": acq_time_str,
        "cloud": cloud_cover,
        "assets": assets_count,
        "c_score": c_score,
        "a_score": a_score,
        "r_score": r_score,
        "final": final_score
    })

ranked = sorted(parsed_features, key=lambda x: x["final"], reverse=True)

with open(REPORT_FILE, "w") as f:
    f.write("OBSERVATION RANKING ENGINE\n")
    f.write("=" * 60 + "\n")
    
    for idx, obs in enumerate(ranked, 1):
        f.write(f"{idx}. {obs['id']}\n")
        f.write(f"   Time: {obs['time']}\n")
        f.write(f"   Cloud cover: {obs['cloud']}%\n")
        f.write(f"   Assets count: {obs['assets']}\n")
        f.write(f"   Cloud score: {obs['c_score']:.2f}\n")
        f.write(f"   Completeness score: {obs['a_score']:.2f}\n")
        f.write(f"   Recency score: {obs['r_score']:.2f}\n")
        f.write(f"   Final score: {obs['final']:.2f}\n")
        f.write("-" * 60 + "\n")

    f.write("\n=== ENGINEERING INTERPRETATION ===\n")
    best = ranked[0]
    f.write(f"1. Which product should be processed first? Product ID: {best['id']}.\n")
    f.write("2. Why did it receive the highest score? Because its combined score of cloud clearance, recency, and available data assets was the highest among the batch.\n")
    f.write("3. Was the decision mostly influenced by cloud coverage, recency or asset completeness? Cloud coverage. The mathematical weighting (up to 100 points) dominates the ranking compared to recency (20 pts) and assets (30 pts).\n")
    f.write("4. Would this ranking strategy be sufficient for a real mission system? No. Real pipelines must also consider spatial overlap with the Area of Interest, data cost, processing level, download endpoints (HTTP vs S3), and provider reliability.\n")

print("OBSERVATION RANKING ENGINE")
print("=" * 60)
for idx, obs in enumerate(ranked, 1):
    print(f"{idx}. {obs['id']}")
    print(f"   Time: {obs['time']}")
    print(f"   Cloud cover: {obs['cloud']}%")
    print(f"   Assets count: {obs['assets']}")
    print(f"   Cloud score: {obs['c_score']:.2f}")
    print(f"   Completeness score: {obs['a_score']:.2f}")
    print(f"   Recency score: {obs['r_score']:.2f}")
    print(f"   Final score: {obs['final']:.2f}")
    print("-" * 60)

print(f"\nAnalysis report and interpretations saved to: {REPORT_FILE}")
