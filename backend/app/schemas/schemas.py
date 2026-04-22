from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from app.models.models import UserRole # Импорт Enum — это ок

class PositionUpdate(BaseModel):
    latitude: float
    longitude: float

class AddMemberRequest(BaseModel):
    user_id: Optional[int] = None
    email: Optional[EmailStr] = None
# 1. Схема для Кругов
class CircleBase(BaseModel):
    name: str

class CircleCreate(CircleBase):
    pass

class CircleRead(CircleBase):
    id: int
    owner_id: int
    # Здесь мы просто указываем типы данных, а не связи БД
    members: List[int] = [] 

    class Config:
        from_attributes = True

# 2. Схемы для Пользователей
class UserBase(BaseModel):
    email: EmailStr
    role: UserRole
    # УДАЛИ СТРОКУ С relationship ОТСЮДА!

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72) 
    
class UserRead(UserBase):
    id: int
    class Config:
        from_attributes = True

# 3. Схемы для SOS
class SOSRequest(BaseModel):
    latitude: float
    longitude: float
    message: Optional[str] = None

# 4. Схемы для SafetyPoint
class SafetyPointBase(BaseModel):
    name: str
    description: Optional[str] = None
    latitude: float
    longitude: float

class SafetyPointCreate(SafetyPointBase):
    pass

class SafetyPointRead(SafetyPointBase):
    id: int
    class Config:
        from_attributes = True

# 5. JWT
class Token(BaseModel):
    access_token: str
    token_type: str