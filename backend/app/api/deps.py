from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.models import UserRole
# Импортируем асинхронную фабрику из твоего файла database.py
from app.db.database import AsyncSessionLocal 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

# Асинхронная зависимость для БД
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        # Сессия автоматически закроется после завершения запроса

# Класс для проверки ролей
class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            role: str = payload.get("role")
            if role not in self.allowed_roles:
                raise HTTPException(status_code=403, detail="Недостаточно прав")
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Невалидный токен")