import json
import requests

with open("contracts/providers_registry.json", "r") as f:
    providers = json.load(f)
with open("contracts/observation_schema.json", "r") as f:
    contract = json.load(f)

required = contract["required_fields"]
stats = {"OK": 0, "VIOLATION": 0, "UNAVAILABLE": 0, "EMPTY DATASET": 0}

for p in providers:
    name, url = p["name"], p["url"]
    try:
        response = requests.get(f"{url}/observations", timeout=2)
        data = response.json()
        if not data:
            print(f"{name}: EMPTY DATASET")
            stats["EMPTY DATASET"] += 1
            continue
        
        missing = [f for f in required if f not in data[0]]
        if missing:
            print(f"{name}: VIOLATION (Missing: {missing})")
            stats["VIOLATION"] += 1
        else:
            print(f"{name}: OK")
            stats["OK"] += 1
    except Exception:
        print(f"{name}: UNAVAILABLE")
        stats["UNAVAILABLE"] += 1

print("\nSUMMARY:")
for k, v in stats.items():
    print(f"{k}: {v}")
print("\nFEDERATION STATE:", "RELIABLE" if stats["UNAVAILABLE"] == 0 and stats["VIOLATION"] == 0 else "DEGRADED")
