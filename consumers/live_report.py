import requests
import json
import os
from datetime import datetime

BROKER_URL = "http://127.0.0.1:7000/events"
REGISTRY_PATH = "contracts/providers_registry.json"
SCHEMA_PATH = "contracts/event_schema.json"

def generate_report():
    try:
        # Load Contracts
        with open(REGISTRY_PATH, 'r') as f:
            expected = [p['name'] for p in json.load(f)]
        with open(SCHEMA_PATH, 'r') as f:
            required_fields = json.load(f)['required_fields']
            
        # Fetch Events
        events = requests.get(BROKER_URL).json()
        
        # Validation & Aggregation
        valid_count = 0
        invalid_count = 0
        per_provider = {}
        objects = set()
        active_providers = set()
        selected_obj_count = 0
        selected_obj_id = "OBJ-003"

        for e in events:
            # Task 10: Validation
            is_valid = all(field in e for field in required_fields)
            if is_valid:
                valid_count += 1
                active_providers.add(e['provider'])
                per_provider[e['provider']] = per_provider.get(e['provider'], 0) + 1
                objects.add(e['object_id'])
                if e['object_id'] == selected_obj_id:
                    selected_obj_count += 1
            else:
                invalid_count += 1

        # Task 9: Missing Providers
        missing = [p for p in expected if p not in active_providers]
        is_complete = "YES" if not missing else "NO"

        # Task 11: Generate Report
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_ts = datetime.now().strftime("%Y%m%d_%HH%MM%SS")
        
        report_content = f"""REAL-TIME FEDERATION REPORT
---------------------------
Generated at: {timestamp}

[STREAM STATUS]
Total events: {len(events)}
Valid events: {valid_count}
Invalid events: {invalid_count}

[PROVIDERS]
Active providers:
{chr(10).join(['- ' + p for p in sorted(active_providers)])}

Missing providers:
{chr(10).join(['- ' + p for p in missing]) if missing else '- none'}

[PER-PROVIDER COUNTS]
{chr(10).join([p + ': ' + str(c) for p, c in per_provider.items()])}

[OBJECT STATISTICS]
Distinct objects: {len(objects)}
{selected_obj_id} observations: {selected_obj_count}

[FEDERATION STATUS]
COMPLETE: {is_complete}
"""
        # Save report
        report_path = f"reports/stream_report_{file_ts}.txt"
        with open(report_path, "w") as f:
            f.write(report_content)
            
        print(f"Report generated: {report_path}")
        print(report_content)

    except Exception as e:
        print(f"Error generating report: {e}")

if __name__ == "__main__":
    generate_report()
