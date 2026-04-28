import requests
import time

BROKER_EVENTS_URL = "http://127.0.0.1:7000/events"
WINDOW_SIZE = 10

print(f"Starting Sliding Window Consumer (Window Size: {WINDOW_SIZE} events)...\n")

while True:
    try:
        response = requests.get(BROKER_EVENTS_URL)
        events = response.json()
        
        if len(events) > 0:
            # Sliding window magic: take only the last N elements from the list
            window_events = events[-WINDOW_SIZE:]
            
            print("\n" + "="*40)
            print(f"SLIDING WINDOW STATS (Last {len(window_events)} events)")
            print("-" * 40)
            
            # Aggregation only within the window
            per_provider = {}
            for event in window_events:
                prov = event.get("provider", "unknown")
                per_provider[prov] = per_provider.get(prov, 0) + 1
                
            print("MESSAGES PER PROVIDER:")
            for prov, count in per_provider.items():
                print(f"  {prov}: {count}")
                
            objects = set(event.get("object_id") for event in window_events)
            print(f"DISTINCT OBJECTS IN WINDOW: {len(objects)}")
            print("="*40)
            
    except Exception as e:
        print("Broker unavailable...")
        
    time.sleep(3)
