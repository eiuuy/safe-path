from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

load_dotenv()

# Твой URL теперь БЕЗ "?sslmode=require"
DATABASE_URL = os.getenv("DATABASE_URL") 

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    # ВАЖНО: Эти параметры чинят твою ошибку
    pool_pre_ping=True,      # Проверять соединение перед использованием
    pool_recycle=3600,       # Пересоздавать соединения каждый час
    pool_size=5,             # Максимум соединений в пуле
    max_overflow=10          # Разрешить временный рост пула
)

# Добавляем connect_args


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
