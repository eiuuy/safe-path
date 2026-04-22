import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
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

async def check_connection():
    try:
        engine = create_async_engine(DATABASE_URL, echo=True)
        async with engine.connect() as conn:
            print("✅ Успешно! Подключение к базе данных установлено.")
    except Exception as e:
        print(f"❌ ОШИБКА подключения: {e}")

if __name__ == "__main__":
    asyncio.run(check_connection())