import os
import requests

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/search"

QUERY = {
    "collections": ["sentinel-2-l2a"],
    "bbox": [19.0, 50.0, 20.0, 51.0],
    "datetime": "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z",
    "query": {
        "eo:cloud_cover": {
            "lt": 20
        }
    },
    "limit": 1
}

OUTPUT_PATHS = {
    "thumbnail": "assets/thumbnails/thumbnail.jpg",
    "TCI_10m": "assets/visual/visual.jp2",
    "B04_10m": "assets/bands/B04.jp2",
    "B08_10m": "assets/bands/B08.jp2"
}

def is_http_url(url):
    return (
        url.startswith("http://")
        or url.startswith("https://")
    )

def download_file(url, output_path):
    if not is_http_url(url):
        print(f"SKIPPED NON-HTTP ASSET: {url}")
        return False
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"ERROR DOWNLOADING ASSET: {e}")
        return False

response = requests.post(STAC_URL, json=QUERY)
data = response.json()

if not data.get("features"):
    print("NO PRODUCTS FOUND TO DOWNLOAD.")
    exit()

item = data["features"][0]
assets = item["assets"]

print("AVAILABLE ASSETS IN METADATA:")
for asset_name in assets:
    print(f" - {asset_name}")

print("\nSTARTING ASSET PROCESSING PIPELINE...")

downloaded_count = 0
skipped_count = 0
report_entries = []

for asset_name, out_path in OUTPUT_PATHS.items():
    if asset_name in assets:
        asset_url = assets[asset_name]["href"]
        print(f"\nChecking asset: '{asset_name}'")
        
        if download_file(asset_url, out_path):
            print(f"-> SUCCESS: Saved to {out_path}")
            downloaded_count += 1
            report_entries.append(f"{asset_name}: DOWNLOADED -> {out_path}")
        else:
            skipped_count += 1
            report_entries.append(f"{asset_name}: SKIPPED (Non-HTTP protocol or auth required)")
    else:
        print(f"\nAsset '{asset_name}' not found in STAC metadata for this product.")
        report_entries.append(f"{asset_name}: NOT FOUND IN METADATA")

report_path = "reports/download_report.txt"
with open(report_path, "w") as report_file:
    report_file.write("=== EO ASSET DOWNLOAD REPORT ===\n")
    report_file.write(f"Product ID: {item['id']}\n")
    report_file.write(f"Total Attempted: {len(OUTPUT_PATHS)}\n")
    report_file.write(f"Successfully Downloaded: {downloaded_count}\n")
    report_file.write(f"Skipped/Failed: {skipped_count}\n")
    report_file.write("--------------------------------\n")
    for entry in report_entries:
        report_file.write(f"{entry}\n")

print(f"\nPipeline finished. Summary report saved to: {report_path}")
