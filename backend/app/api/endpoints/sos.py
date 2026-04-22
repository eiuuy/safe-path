from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.models import SOSSession, SOSResponse, User
from app.core.security import get_current_user  # Убедись, что путь к security верный

router = APIRouter(prefix="/sos", tags=["SOS Emergency"])

@router.post("/trigger")
async def trigger_sos(
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # 1. Получаем текущую позицию пользователя
    result = await db.execute(select(UserPosition).where(UserPosition.user_id == current_user.id))
    user_pos = result.scalar_one_or_none()
    
    # 2. Создаем сессию
    new_sos = SOSSession(user_id=current_user.id, status="active")
    db.add(new_sos)
    await db.flush() # Получаем ID новой сессии (sos_id)
    
    # 3. Сохраняем "точку входа" в SOSHistory (важно зафиксировать, где всё началось)
    if user_pos:
        sos_log = SOSHistory(
            user_id=current_user.id, 
            geom=user_pos.geom
        )
        db.add(sos_log)
    
    # Собираем токены всех участников круга
    # (Предположим, у тебя есть метод получения участников)
    target_tokens = [] 
    for circle in current_user.circles:
        for member in circle.members:
            if member.fcm_token:
                target_tokens.append(member.fcm_token)
    
    # Добавляем задачу в фон
    if target_tokens:
        background_tasks.add_task(
            send_push_notification,
            tokens=target_tokens,
            title="SOS! Нужна помощь!",
            body=f"{current_user.name} отправил сигнал тревоги!"
        )
    
    return {"message": "SOS активирован!", "sos_id": new_sos.id}


@router.post("/{sos_id}/accept")
async def accept_sos(
    sos_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # 1. Находим сессию
    sos_session = await db.get(SOSSession, sos_id)
    if not sos_session:
        raise HTTPException(status_code=404, detail="SOS не найден")

    # 2. ПРОВЕРКА: Состоит ли текущий пользователь в круге с пострадавшим?
    # (Предположим, у тебя есть метод проверки связи)
    # is_in_same_circle = ...
    
    # Пока просто создаем отклик
    new_response = SOSResponse(sos_id=sos_id, responder_id=current_user.id)
    db.add(new_response)
    await db.commit()
    
    return {"message": "Вы подтвердили помощь, следуйте к локации пользователя."}

@router.post("/{sos_id}/complete")
async def finish_sos(
    sos_id: int, 
    db: AsyncSession = Depends(get_db)
):
    # Ребенок дошел или нажал "Я дома"
    sos = await db.get(SOSSession, sos_id)
    if not sos:
        raise HTTPException(status_code=404, detail="SOS не найден")
    
    sos.status = "completed"
    await db.commit()
    return {"message": "Статус изменен на 'Безопасно'. Уведомления отправлены."}