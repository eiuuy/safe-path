from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from geoalchemy2.functions import ST_DWithin
# Исправленный импорт: теперь берем из elements
from geoalchemy2.elements import WKTElement 
from app.db.database import get_db
from app.models.models import SafetyPoint

router = APIRouter(prefix="/safe-spaces", tags=["Safe Spaces"])

@router.get("/nearest")
async def get_nearest_safe_space(
    lat: float, 
    lon: float, 
    db: AsyncSession = Depends(get_db)
):
    user_location = WKTElement(f'POINT({lon} {lat})', srid=4326)
    
    # Ищем, сортируем по удаленности и берем только первую (самую близкую)
    query = select(SafetyPoint).where(
        ST_DWithin(SafetyPoint.location, user_location, 2000) # Увеличим радиус до 2км для поиска
    ).order_by(
        func.ST_Distance(SafetyPoint.location, user_location)
    ).limit(1)
    
    result = await db.execute(query)
    nearest = result.scalar_one_or_none()
    
    if not nearest:
        return {"message": "Безопасных мест рядом не найдено"}
    
    return nearest