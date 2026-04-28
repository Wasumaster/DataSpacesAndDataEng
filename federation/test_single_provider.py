import requests

data_a_all = requests.get("http://127.0.0.1:8001/observations").json()
data_a_obj = requests.get("http://127.0.0.1:8001/observations/OBJ-003").json()

try:
    data_b_obj = requests.get("http://127.0.0.1:8002/observations/OBJ-003").json()
except Exception:
    data_b_obj = []

print("satellite_A:")
print("NUMBER OF OBSERVATIONS:", len(data_a_all))
print("OBJ-003 RESULTS:", len(data_a_obj))

print("\nsatellite_B:")
print("OBJ-003 RESULTS:", len(data_b_obj))

print("\nCOMPARISON:")
if len(data_a_obj) > 0 and len(data_b_obj) > 0:
    print("OBJ-003 is present in both providers.")
elif len(data_a_obj) > 0:
    print("OBJ-003 is present only in satellite_A.")
elif len(data_b_obj) > 0:
    print("OBJ-003 is present only in satellite_B.")
else:
    print("OBJ-003 is not present in any provider.")
