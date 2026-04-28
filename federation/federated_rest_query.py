import json
import requests

with open("contracts/providers_registry.json", "r") as f:
    providers = json.load(f)

all_results = []
per_provider_count = {}

for provider in providers:
    name = provider["name"]
    url = provider["url"]
    try:
        response = requests.get(f"{url}/observations", timeout=2)
        data = response.json()
        per_provider_count[name] = len(data)
        for row in data:
            row["provider"] = name
            all_results.append(row)
    except Exception:
        per_provider_count[name] = 0

print("TOTAL RECORDS:", len(all_results))
print("PER-PROVIDER COUNTS:")
for name, count in per_provider_count.items():
    print(f"{name}: {count}")

if per_provider_count:
    largest = max(per_provider_count, key=per_provider_count.get)
    print("LARGEST PROVIDER:", largest)
