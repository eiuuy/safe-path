from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_DWithin # Импортируем фильтр
from app.db.database import get_db
from app.models.models import SafetyPoint
from app.services.google_maps import get_route_info

router = APIRouter(prefix="/safe-spaces", tags=["Safe Spaces"])

@router.get("/nearest")
async def get_nearest_safe_space(lat: float, lon: float, db: AsyncSession = Depends(get_db)):
    user_location = WKTElement(f'POINT({lon} {lat})', srid=4326)
    
    # 1. Фильтруем (радиус 5000 метров = 5 км) и сортируем
    query = select(
        SafetyPoint, 
        func.ST_X(SafetyPoint.location).label("lon"), 
        func.ST_Y(SafetyPoint.location).label("lat")
    ).where(
        ST_DWithin(SafetyPoint.location, user_location, 5000) 
    ).order_by(
        func.ST_Distance(SafetyPoint.location, user_location)
    ).limit(1)
    
    result = await db.execute(query)
    row = result.one_or_none()
    
    if not row:
        # Если в радиусе 5 км ничего нет, можно вернуть ошибку или пустой ответ
        raise HTTPException(status_code=404, detail="Безопасных мест в радиусе 5 км не найдено")

    nearest_point = row[0]
    dest_lat, dest_lon = row[2], row[1]

    # 2. Запрашиваем маршрут у Google
    route_data = await get_route_info(lat, lon, dest_lat, dest_lon)
    
    return {
        "point": {
            "id": nearest_point.id,
            "name": nearest_point.name,
            "address": nearest_point.address,
            "lat": dest_lat,
            "lon": dest_lon
        },
        "route": route_data
    }