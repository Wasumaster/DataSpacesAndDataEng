import json, requests, strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

with open("../contracts/providers_registry.json", "r") as f:
    PROVIDERS = json.load(f)

@strawberry.type
class Observation:
    provider: str
    timestamp: str
    object_id: str
    temperature: float
    velocity: float

def fetch_data(url, object_id=None):
    full_url = f"{url}/observations"
    if object_id:
        full_url += f"/{object_id}"
    try:
        r = requests.get(full_url, timeout=2)
        return r.json()
    except:
        return []

@strawberry.type
class Query:
    @strawberry.field
    def observations(self) -> list[Observation]:
        results = []
        for p in PROVIDERS:
            data = fetch_data(p['url'])
            for row in data:
                results.append(Observation(
                    provider=p['name'],
                    timestamp=str(row.get('timestamp', '')),
                    object_id=str(row.get('object_id', '')),
                    temperature=float(row.get('temperature', 0)),
                    velocity=float(row.get('velocity', 0))
                ))
        return results

    @strawberry.field
    def observations_by_object(self, object_id: str) -> list[Observation]:
        results = []
        for p in PROVIDERS:
            data = fetch_data(p['url'], object_id)
            for row in data:
                results.append(Observation(
                    provider=p['name'],
                    timestamp=str(row.get('timestamp', '')),
                    object_id=str(row.get('object_id', '')),
                    temperature=float(row.get('temperature', 0)),
                    velocity=float(row.get('velocity', 0))
                ))
        return results

schema = strawberry.Schema(query=Query)
app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
