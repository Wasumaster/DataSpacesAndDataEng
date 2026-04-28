import pandas as pd
import requests
import time

BROKER_URL = "http://127.0.0.1:7000/publish"
PROVIDER_NAME = "satellite_B"

try:
    df = pd.read_csv("providers/satellite_B/observations.csv")
    for _, row in df.iterrows():
        event = {
            "provider": PROVIDER_NAME,
            "timestamp": str(row["timestamp"]),
            "object_id": str(row["object_id"]),
            "temperature": float(row["temperature"]),
            "velocity": float(row["velocity"])
        }
        response = requests.post(BROKER_URL, json=event)
        print(f"SENT: {event['provider']} | STATUS: {response.status_code}")
        # Task P3: High-frequency (0.2s delay)
        time.sleep(0.2)
except Exception as e:
    print(f"Error in satellite_B producer: {e}")
