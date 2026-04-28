import requests
import time

BROKER_EVENTS_URL = "http://127.0.0.1:7000/events"

while True:
    try:
        response = requests.get(BROKER_EVENTS_URL)
        events = response.json()
        
        print("\n" + "="*40)
        print("CURRENT NUMBER OF EVENTS:", len(events))
        
        if len(events) > 0:
            providers = sorted(set(event["provider"] for event in events))
            objects = sorted(set(event["object_id"] for event in events))
            
            print("ACTIVE PROVIDERS:", providers)
            
            # Zadanie 8 - Agregacje
            per_provider = {}
            for event in events:
                prov = event["provider"]
                per_provider[prov] = per_provider.get(prov, 0) + 1
                
            print("PER PROVIDER:")
            for prov, count in per_provider.items():
                print(f"  {prov}: {count}")
                
            print("DISTINCT OBJECTS:", len(objects))
            
            selected_object = "OBJ-003"
            selected_count = sum(1 for event in events if event.get("object_id") == selected_object)
            print(f"{selected_object} OBSERVATIONS: {selected_count}")
            
            timestamps = [event["timestamp"] for event in events]
            print("MOST RECENT EVENT:", max(timestamps))

        print("="*40)
    except Exception as e:
        print("Broker is unavailable...")
        
    time.sleep(3)
