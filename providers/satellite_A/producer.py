import pandas as pd
import requests
import time

BROKER_URL = "http://127.0.0.1:7000/publish"
PROVIDER_NAME = "satellite_A"
df = pd.read_csv("providers/satellite_A/observations.csv")

for _, row in df.iterrows():
    event = {
        "provider": PROVIDER_NAME,
        "timestamp": str(row["timestamp"]),
        "object_id": str(row["object_id"]),
        "temperature": float(row["temperature"]),
        "velocity": float(row["velocity"])
    }
    try:
        response = requests.post(BROKER_URL, json=event)
        print("SENT:", event["provider"], "| STATUS:", response.status_code)
    except Exception as e:
        pass
    time.sleep(1)
