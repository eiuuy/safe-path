from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.future import select
from app.api.deps import get_db
from app.models.models import UserPosition
from app.schemas.schemas import PositionUpdate
from app.core.security import get_current_user # (твоя схема выше)

router = APIRouter()

@router.post("/")
async def update_my_position(
    data: PositionUpdate,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Ищем, есть ли уже запись позиции для этого пользователя
    result = await db.execute(select(UserPosition).where(UserPosition.user_id == current_user.id))
    position = result.scalar_one_or_none()

    # Создаем точку в формате PostGIS
    point = func.ST_SetSRID(func.ST_MakePoint(data.longitude, data.latitude), 4326)

    if position:
        # Обновляем существующую
        position.geom = point
    else:
        # Создаем новую
        position = UserPosition(
            user_id=current_user.id,
            geom=point
        )
        db.add(position)
    
    await db.commit()
    return {"message": "Позиция обновлена"}


@router.get("/my")
async def get_my_position(
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Делаем запрос к БД
    result = await db.execute(
        select(UserPosition).where(UserPosition.user_id == current_user.id)
    )
    position = result.scalar_one_or_none()
    
    if not position:
        raise HTTPException(status_code=404, detail="Позиция не найдена")

    # Преобразуем геометрию в координаты для ответа
    # ST_X (долгота), ST_Y (широта)
    coords = await db.execute(
        select(func.ST_X(position.geom), func.ST_Y(position.geom))
    )
    lon, lat = coords.one()
    
    return {
        "latitude": lat,
        "longitude": lon,
        "updated_at": position.updated_at
    }