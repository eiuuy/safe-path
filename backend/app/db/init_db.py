import asyncio
import os
from dotenv import load_dotenv # 1. Импортируем загрузчик

# 2. Загружаем .env ПЕРЕД импортом моделей и движка
load_dotenv()

from app.db.database import engine, Base
from app.models.models import User, Circle, UserPosition, SOSHistory, SafetyPoint

async def init_tables():
    # 3. Выведем, какой URL он видит, для отладки
    url = os.getenv("DATABASE_URL")
    print(f"DEBUG: Пытаюсь подключиться к базе по адресу: {url}")
    
    print("Создаю таблицы в базе данных...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("База данных готова!")
    except Exception as e:
        print(f"ОШИБКА при создании таблиц: {e}")

if __name__ == "__main__":
    asyncio.run(init_tables())