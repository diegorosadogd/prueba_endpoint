from fastapi import FastAPI
import random
from typing import Dict, Any

app = FastAPI(title="Tlalpan Random Points API")

# Bounding box for Tlalpan, Mexico City
# Min Lat: 19.08938, Max Lat: 19.31226
# Min Lon: -99.31625, Max Lon: -99.10093
TLALPAN_BOUNDS = {
    "lat_min": 19.08938,
    "lat_max": 19.31226,
    "lon_min": -99.31625,
    "lon_max": -99.10093
}

@app.get("/random-points", response_model=Dict[str, Any])
async def get_random_points(count: int = 10):
    """
    Generates 'count' random points within the Tlalpan bounding box
    and returns them as a GeoJSON FeatureCollection.
    """
    features = []
    for _ in range(count):
        lat = random.uniform(TLALPAN_BOUNDS["lat_min"], TLALPAN_BOUNDS["lat_max"])
        lon = random.uniform(TLALPAN_BOUNDS["lon_min"], TLALPAN_BOUNDS["lon_max"])
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]  # GeoJSON coordinates are [longitude, latitude]
            },
            "properties": {
                "id": _ + 1
            }
        }
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

