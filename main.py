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

@app.get("/")
async def root():
    return {"message": "Hola Mundo"}

@app.get("/random-points", response_model=Dict[str, Any])
async def get_random_points(count: int = 50):
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
                "coordinates": [lon, lat] , # GeoJSON coordinates are [longitude, latitude]
                "negocio":random.choice(["tienda","restaurante"])
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
    import os 
    host ="0.0.0.0"
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)

