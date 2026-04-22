import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import User
from app.db.database import get_db
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
# Настройки для JWT
SECRET_KEY = "SUPER_SECRET_KEY" 
ALGORITHM = "HS256"

# 1. Указываем путь, куда клиент будет слать токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# Функция для хеширования пароля
def get_password_hash(password: str) -> str:
    pwd_bytes = password[:72].encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password[:72].encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)

# Функция для создания токена
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Функция-зависимость для проверки пользователя
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    # 1. Выводим токен в консоль, чтобы убедиться, что он пришел верно
    # print(f"DEBUG: Token: {token}") 
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
    )
    
    try:
        # 2. Декодируем и выводим payload (содержимое токена)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"DEBUG: Payload decoded: {payload}")
        
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
        user_id_int = int(user_id)
        
    except Exception as e:
        # Выводим ошибку, если декодирование не удалось
        print(f"DEBUG: Critical Error during decoding: {e}")
        raise credentials_exception
    
    # 3. Выводим ID, который мы ищем
    print(f"DEBUG: Searching for user with ID: {user_id_int}")
    
    result = await db.execute(select(User).where(User.id == user_id_int))
    user = result.scalar_one_or_none()
    
    # 4. Проверяем, нашелся ли пользователь
    if user is None:
        print(f"DEBUG: User not found in DB!")
        raise credentials_exception
    
    return user