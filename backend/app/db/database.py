from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

load_dotenv()

# Твой URL теперь БЕЗ "?sslmode=require"
DATABASE_URL = os.getenv("DATABASE_URL") 

# Добавляем connect_args
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"ssl": "require"}
)

if not DATABASE_URL:
    raise ValueError("Ошибка: DATABASE_URL не задан в переменных окружения!")
# Создаем движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика сессий
AsyncSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Базовый класс для всех моделей
Base = declarative_base()

# Dependency для FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session