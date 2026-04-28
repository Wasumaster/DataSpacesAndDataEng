import requests
import time

BROKER_EVENTS_URL = "http://127.0.0.1:7000/events"
TEMP_THRESHOLD = 25.0
VELOCITY_THRESHOLD = 7.5
processed_count = 0

print("Starting Threshold Alert Consumer...")
print(f"Limits -> Temp: >{TEMP_THRESHOLD}, Velocity: >{VELOCITY_THRESHOLD}\n")

while True:
    try:
        response = requests.get(BROKER_EVENTS_URL)
        events = response.json()
        
        # Przetwarzaj tylko nowe zdarzenia
        new_events = events[processed_count:]
        for event in new_events:
            temp = float(event.get("temperature", 0))
            vel = float(event.get("velocity", 0))
            
            if temp > TEMP_THRESHOLD or vel > VELOCITY_THRESHOLD:
                print("WARNING:")
                print(f"Provider: {event.get('provider')}")
                print(f"Object: {event.get('object_id')}")
                print(f"Temperature: {temp} / Velocity: {vel}")
                print("-" * 30)
                
        processed_count = len(events)
    except Exception:
        pass
    
    time.sleep(2)
