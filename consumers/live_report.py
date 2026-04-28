import requests
import json
import datetime
import os

BROKER_EVENTS_URL = "http://127.0.0.1:7000/events"
REPORTS_DIR = "reports"

# 1. Load contracts (Task 9 and 10)
with open("contracts/providers_registry.json", "r") as f:
    expected_providers = [p["name"] for p in json.load(f)]

with open("contracts/event_schema.json", "r") as f:
    contract = json.load(f)
    required_fields = contract["required_fields"]

# 2. Fetch data from stream
try:
    response = requests.get(BROKER_EVENTS_URL)
    events = response.json()
except Exception as e:
    print("Broker is offline:", e)
    events = []

# 3. Processing and Validation
total_events = len(events)
valid_count = 0
invalid_count = 0
per_provider = {}
objects = set()
active_providers = set()
selected_object = "OBJ-003"
selected_count = 0

for event in events:
    # Validation (Task 10)
    missing_fields = [field for field in required_fields if field not in event]
    if missing_fields:
        invalid_count += 1
    else:
        valid_count += 1
        
        # Provider statistics
        prov = event["provider"]
        active_providers.add(prov)
        per_provider[prov] = per_provider.get(prov, 0) + 1
        
        # Object statistics
        obj_id = event["object_id"]
        objects.add(obj_id)
        if obj_id == selected_object:
            selected_count += 1

# 4. Detect missing providers (Task 9)
missing_providers = sorted(set(expected_providers) - active_providers)
is_complete = "YES" if not missing_providers else "NO"

# 5. Generate report text (Task 11)
now = datetime.datetime.now()
timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
file_timestamp = now.strftime("%Y%m%d_%H%M%S")

report_lines = [
    "REAL-TIME FEDERATION REPORT",
    "---------------------------",
    f"Generated at: {timestamp_str}",
    "",
    "[STREAM STATUS]",
    f"Total events: {total_events}",
    f"Valid events: {valid_count}",
    f"Invalid events: {invalid_count}",
    "",
    "[PROVIDERS]",
    "Active providers:"
]

for p in sorted(active_providers):
    report_lines.append(f"- {p}")

report_lines.append("\nMissing providers:")
if missing_providers:
    for p in missing_providers:
        report_lines.append(f"- {p}")
else:
    report_lines.append("- none")

report_lines.append("\n[PER-PROVIDER COUNTS]")
for p, c in per_provider.items():
    report_lines.append(f"{p}: {c}")

report_lines.append("\n[OBJECT STATISTICS]")
report_lines.append(f"Distinct objects: {len(objects)}")
report_lines.append(f"{selected_object} observations: {selected_count}")

report_lines.append("\n[FEDERATION STATUS]")
report_lines.append(f"COMPLETE: {is_complete}")

report_text = "\n".join(report_lines)

# 6. Save to file
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)
    
report_filename = f"{REPORTS_DIR}/stream_report_{file_timestamp}.txt"
with open(report_filename, "w") as f:
    f.write(report_text)

print(f"Report successfully generated: {report_filename}\n")
print(report_text)
