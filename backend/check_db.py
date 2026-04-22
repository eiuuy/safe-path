import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import OperationalError

# ПОМЕНЯЙ ЭТИ ДАННЫЕ:
# Если пароль не помнишь, это тот, что вводил при установке Postgres
async def check():
    engine = create_async_engine(DATABASE_URL)
    try:
        async with engine.connect() as conn:
            print("✅ ПОДКЛЮЧЕНИЕ УСПЕШНО!")
    except Exception as e:
        print("\n❌ ОШИБКА:")
        print(f"Тип ошибки: {type(e).__name__}")
        print(f"Текст ошибки: {e}")
        print("\n--- СОВЕТЫ ---")
        if "password authentication failed" in str(e):
            print("-> Неверный пароль. Попробуй вспомнить тот, что вводил при установке Postgres.")
        elif "database 'safepath' does not exist" in str(e):
            print(f"-> База данных '{DB_NAME}' не найдена. Создай её в pgAdmin (правой кнопкой на Databases -> Create).")
        elif "connection refused" in str(e):
            print("-> База данных не отвечает. Проверь, запущен ли сервис PostgreSQL в 'Службы' (services.msc).")

if __name__ == "__main__":
    asyncio.run(check())
