from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import engine, Base
from app.api.endpoints import auth, circles, safe_spaces, sos, positions
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 2. ЗАТЕМ СОЗДАНИЕ ПРИЛОЖЕНИЯ
app = FastAPI()

# 3. ПОСЛЕ СОЗДАНИЯ ПРИЛОЖЕНИЯ ДОБАВЛЯЕМ MIDDLEWARE (CORS)
# Это «ворота» твоего приложения. Ставим их здесь, чтобы запрос проверялся до того, как дойдет до маршрутов.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.lovableproject\.com|https://.*\.lovable\.app|http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Эта функция запускается ОДИН РАЗ при старте сервера
@asynccontextmanager
async def lifespan(app: FastAPI):
    # СОЗДАНИЕ ТАБЛИЦ
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # (Здесь можно добавить код для закрытия соединения при выключении)

app = FastAPI(title="Safe Path API", lifespan=lifespan)

# Подключаем маршруты
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(circles.router, prefix="/api/v1/circles", tags=["Circles"])
app.include_router(safe_spaces.router, prefix="/api/v1/safe-spaces", tags=["Safe Spaces"])
app.include_router(sos.router, prefix="/api/v1", tags=["SOS Emergency"])
app.include_router(positions.router, prefix="/api/v1/positions", tags=["Positions"])

@app.get("/")
def read_root():
    return {"message": "Safe Path API is running!"}