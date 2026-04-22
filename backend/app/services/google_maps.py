import httpx
from app.core.config import settings

async def get_route_info(origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    
    headers = {
        "X-Goog-Api-Key": settings.GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.polyline.encodedPolyline"
    }
    
    payload = {
        "origin": {"location": {"latLng": {"latitude": origin_lat, "longitude": origin_lon}}},
        "destination": {"location": {"latLng": {"latitude": dest_lat, "longitude": dest_lon}}},
        "travelMode": "WALK", # Для безопасности пешком обычно важнее
        "routingPreference": "TRAFFIC_AWARE"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if "routes" in data and data["routes"]:
                return data["routes"][0]
            return None
        except Exception as e:
            print(f"Ошибка при запросе к Google Maps: {e}")
            return None