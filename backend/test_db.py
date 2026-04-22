import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

# Скопируй сюда точно ту же строку, что у тебя в database.py
DATABASE_URL = "postgresql+asyncpg://user:Esen2010@localhost:5432/safepath"

async def check_connection():
    try:
        engine = create_async_engine(DATABASE_URL, echo=True)
        async with engine.connect() as conn:
            print("✅ Успешно! Подключение к базе данных установлено.")
    except Exception as e:
        print(f"❌ ОШИБКА подключения: {e}")

if __name__ == "__main__":
    asyncio.run(check_connection())