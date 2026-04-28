import requests
import time

BROKER_URL = "http://127.0.0.1:7000/events"
TEMP_LIMIT = 25.0
VEL_LIMIT = 7.5
processed_indices = 0

print(f"Monitoring stream for alerts (Temp > {TEMP_LIMIT}, Vel > {VEL_LIMIT})...")

while True:
    try:
        events = requests.get(BROKER_URL).json()
        new_events = events[processed_indices:]
        
        for event in new_events:
            temp = event.get("temperature", 0)
            vel = event.get("velocity", 0)
            
            if temp > TEMP_LIMIT or vel > VEL_LIMIT:
                print("\n[!] THRESHOLD ALERT")
                print(f"Provider: {event['provider']} | Object: {event['object_id']}")
                print(f"Temp: {temp} | Vel: {vel}")
        
        processed_indices = len(events)
    except:
        pass
    time.sleep(2)
