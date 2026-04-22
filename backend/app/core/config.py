from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Твои существующие переменные (убедись, что они тут есть)
    DATABASE_URL: str
    SECRET_KEY: str
    
    # Новая переменная для карт
    GOOGLE_MAPS_API_KEY: str
    
    # Указываем, что переменные нужно брать из .env
    model_config = SettingsConfigDict(env_file=".env")

# Создаем экземпляр, который будем импортировать
settings = Settings()