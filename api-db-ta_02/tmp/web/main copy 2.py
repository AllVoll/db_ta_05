from fastapi import FastAPI, Request, Form, Depends, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from alembic import command
from alembic.config import Config
from web import schemas, database
from .models import ApiKey
from .database import engine, get_db
from .base import Base
from typing import List


app = FastAPI()

api_router = APIRouter()

app.mount("/static", StaticFiles(directory="/app/web/static"), name="static")

templates = Jinja2Templates(directory="/app/web/templates")

app.include_router(api_router, prefix="/api")

# Создаем таблицы при инициализации приложения
def create_tables():
    Base.metadata.create_all(bind=engine)

# Проверяем, существуют ли все таблицы в БД
def check_tables_exist():
    for table in Base.metadata.tables.values():
        if not engine.dialect.has_table(engine, table.name):
            return False
    return True

@app.on_event("startup")
async def startup():
    # Проверяем, существуют ли все таблицы в БД при запуске приложения
    if not check_tables_exist():
        create_tables()
        # После создания таблиц запускаем миграцию Alembic
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("script_location", "alembic")
        command.stamp(alembic_cfg, "head")

# Корневой маршрут
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(database.get_db)):
    return templates.TemplateResponse("index.html", {"request": request})

# TradingView виджет
@app.get("/tradingview_widget")
async def tradingview_widget(request: Request, db: Session = Depends(database.get_db)):
    return templates.TemplateResponse("tradingview_widget.html", {"request": request})

# Endpoint для страницы настроек
@app.get("/settings", response_class=HTMLResponse)
async def settings(request: Request, db: Session = Depends(database.get_db)):
    keys = db.query(ApiKey).all()
    return templates.TemplateResponse("settings.html", {"request": request, "keys": keys})

# Endpoint для страницы управления API
@app.get("/api_manager")
async def api_manager(request: Request, db: Session = Depends(database.get_db)):
    return templates.TemplateResponse("api_manager.html", {"request": request})

# Endpoint для страницы ключей API
@app.get("/api_keys")
async def api_manager(request: Request, db: Session = Depends(database.get_db)):
    return templates.TemplateResponse("api_keys.html", {"request": request})

# Endpoint для добавления нового ключа API
@app.post("/api/api_manager")
async def add_api_key(request: Request, name: str = Form(...), binance_key: str = Form(...), binance_secret: str = Form(...), db: Session = Depends(database.get_db)):
    api_key = schemas.ApiKey(name=name, binance_key=binance_key, binance_secret=binance_secret)
    db.add(ApiKey(**api_key.dict()))
    db.commit()
    return templates.TemplateResponse("api_manager.html", {"request": request})
