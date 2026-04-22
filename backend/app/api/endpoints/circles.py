from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.models import User, Circle
from app.schemas.schemas import CircleRead, CircleCreate, AddMemberRequest
from app.schemas.circles import CircleInvite
from app.core.security import get_current_user


router = APIRouter(tags=["Circles"])

# Добавь в app/api/endpoints/circles.py

@router.get("/")
async def get_my_circles(
    db=Depends(get_db), 
    current_user=Depends(get_current_user)
):
    # Ищем все круги, где текущий юзер - владелец
    result = await db.execute(
        select(Circle).where(Circle.owner_id == current_user.id)
    )
    circles = result.scalars().all()
    return circles

@router.post("/")
async def create_circle(
    circle_in: CircleCreate, # Твоя Pydantic схема
    db=Depends(get_db), 
    current_user=Depends(get_current_user)
):
    # ПРОВЕРКА: есть ли уже у этого юзера круг?
    result = await db.execute(select(Circle).where(Circle.owner_id == current_user.id))
    existing_circle = result.scalar_one_or_none()
    
    if existing_circle:
        raise HTTPException(status_code=400, detail="У вас уже есть созданный круг")

    # И только потом создаем...
    new_circle = Circle(name=circle_in.name, owner_id=current_user.id)
    # ...и так далее

@router.post("/")
async def create_circle(
    circle_in: CircleCreate, # Твоя Pydantic схема
    db=Depends(get_db), 
    current_user=Depends(get_current_user)
):
    # ПРОВЕРКА: есть ли у пользователя уже круг?
    result = await db.execute(select(Circle).where(Circle.owner_id == current_user.id))
    existing_circle = result.scalar_one_or_none()
    
    if existing_circle:
        # Если круг есть, просто верни его или выдай ошибку
        return existing_circle 
        # Или: raise HTTPException(status_code=400, detail="Круг уже существует")

    # Если круга нет — создаем
    new_circle = Circle(name=circle_in.name, owner_id=current_user.id)
    db.add(new_circle)
    await db.commit()
    await db.refresh(new_circle)
    return new_circle

# 2. Добавление пользователя в круг
@router.post("/{circle_id}/members")
async def add_member_to_circle(
    circle_id: int, 
    request: AddMemberRequest, 
    db=Depends(get_db), 
    current_user=Depends(get_current_user)
):
    # 1. Находим круг
    result = await db.execute(select(Circle).where(Circle.id == circle_id))
    circle = result.scalar_one_or_none()
    
    if not circle:
        raise HTTPException(status_code=404, detail="Круг не найден")
    
    if circle.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Только владелец может добавлять участников")
    
    # 2. Логика поиска пользователя
    if request.user_id:
        # Ищем по ID
        user_stmt = select(User).where(User.id == request.user_id)
    elif request.email:
        # Ищем по email
        user_stmt = select(User).where(User.email == request.email)
    else:
        # Если не передали ни то, ни другое
        raise HTTPException(status_code=400, detail="Укажите либо user_id, либо email")

    user_result = await db.execute(user_stmt)
    user_to_add = user_result.scalar_one_or_none()
    
    if not user_to_add:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # 3. Добавляем в список участников
    # Проверка, чтобы не добавить дважды
    if user_to_add in circle.members:
        raise HTTPException(status_code=400, detail="Пользователь уже в круге")

    circle.members.append(user_to_add)
    await db.commit()
    
    return {"message": f"Пользователь {user_to_add.email} успешно добавлен"}

@router.post("/invite")
async def send_invite(
    data: CircleInvite, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(User).where(User.email == data.guardian_email))
    guardian = result.scalar_one_or_none()
    
    if not guardian:
        raise HTTPException(status_code=404, detail="Родитель не найден")
    
    new_invite = CircleMember(user_id=current_user.id, guardian_id=guardian.id)
    db.add(new_invite)
    await db.commit()
    return {"message": "Запрос отправлен родителю"}

@router.get("/requests/incoming")
async def get_incoming_requests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(CircleMember).where(
        CircleMember.guardian_id == current_user.id,
        CircleMember.status == "pending"
    )
    result = await db.execute(query)
    requests = result.scalars().all()
    return requests

@router.patch("/requests/{request_id}")
async def update_request_status(
    request_id: int,
    new_status: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(CircleMember).where(
        CircleMember.id == request_id,
        CircleMember.guardian_id == current_user.id
    )
    result = await db.execute(query)
    db_request = result.scalar_one_or_none()

    if not db_request:
        raise HTTPException(status_code=404, detail="Запрос не найден")

    db_request.status = new_status
    await db.commit()
    return {"message": f"Статус обновлен на {new_status}"}

@router.get("/my-teenagers")
async def get_my_teenagers(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = (
        select(User)
        .join(CircleMember, User.id == CircleMember.user_id)
        .where(
            CircleMember.guardian_id == current_user.id,
            CircleMember.status == "accepted"
        )
    )
    result = await db.execute(query)
    teenagers = result.scalars().all()
    return teenagers