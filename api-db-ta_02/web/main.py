#main.py

from fastapi import FastAPI, Request, Form, Depends, HTTPException, APIRouter, responses
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncpg
from sqlalchemy.orm import Session
from web import schemas, database
from .models import ApiKey
from .database import get_db, engine, SessionLocal
from alembic import command
from alembic.config import Config
from .base import Base
from typing import List
from . import database, models, config, migration_utils, api_manager
from .migration_utils import create_migration, check_database, upgrade_database
import logging

app = FastAPI()

api_router = APIRouter()

app.mount("/static", StaticFiles(directory="/app/web/static"), name="static")

templates = Jinja2Templates(directory="/app/web/templates")

app.include_router(api_router, prefix="/api")

#Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine, checkfirst=True)

alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option("script_location", "migrations")

# вызываем функцию check_database() и передаем аргумент engine
try:
    check_database(engine)
except Exception as e:
    logging.error(f"An error occurred while checking the database: {e}")

#new_new
@app.on_event("startup")
async def startup():
    try:
        check_database(engine)
    except Exception as e:
        logging.error(f"An error occurred while checking the database: {e}")

@app.on_event("shutdown")
async def shutdown():
    try:
        models.SessionLocal.close_all()
    except Exception as e:
        logging.error(f"An error occurred while closing database sessions: {e}")    


#new
#def create_tables():
#    Base.metadata.create_all(bind=engine)
#
#def check_tables_exist():
#    for table in Base.metadata.tables:
#        if not engine.dialect.has_table(engine, table):
#            return False
#    return True

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(database.get_db)):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logging.error(f"An error occurred while rendering the index template: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/tradingview_widget")
async def tradingview_widget(request: Request, db: Session = Depends(database.get_db)):
    try:
        return templates.TemplateResponse("tradingview_widget.html", {"request": request})
    except Exception as e:
        logging.error(f"An error occurred while rendering the tradingview_widget template: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Этот endpoint получает список ключей из базы данных и передает его в шаблон settings.html
@app.get("/settings", response_class=HTMLResponse)
async def settings(request: Request, db: Session = Depends(database.get_db)):
    try:
        keys = db.query(models.ApiKey).all()
        return templates.TemplateResponse("settings.html", {"request": request, "keys": keys})
    except Exception as e:
        logging.error(f"An error occurred while rendering the settings template: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/api_manager")
async def api_manager(request: Request, db: Session = Depends(database.get_db)):
    return templates.TemplateResponse("api_manager.html", {"request": request})

@app.get("/api_keys")
async def api_manager(request: Request, db: Session = Depends(database.get_db)):
    return templates.TemplateResponse("api_keys.html", {"request": request})

# @app.post("/api_manager")
# async def add_api_key(request: Request, name: str = Form(...), binance_key: str = Form(...), binance_secret: str = Form(...), db: Session = Depends(database.get_db)):
#     api_key = schemas.ApiKey(name=name, binance_key=binance_key, binance_secret=binance_secret)
#     db.add(ApiKey(**api_key.dict()))
#     db.commit()
#     # Add the migration
#     command.stamp(alembic_cfg, "head")
#     return templates.TemplateResponse("api_manager.html", {"request": request})


@app.post("/api_manager")
async def add_api_key(request: Request, name: str = Form(...), binance_key: str = Form(...), binance_secret: str = Form(...), db: Session = Depends(database.get_db)):
    try:
        api_key = schemas.ApiKey(name=name, binance_key=binance_key, binance_secret=binance_secret)
        db.add(ApiKey(**api_key.dict()))
        db.commit()
        # Add the migration
        command.stamp(alembic_cfg, "head")
        return templates.TemplateResponse("api_manager.html", {"request": request})        
    except Exception as e:
        return {"error": str(e)}


#удаляем API-keys
@app.get("/delete_api_key/{key_id}")
async def delete_api_key(key_id: int, db: Session = Depends(database.get_db)):
    try:
        api_key = db.query(ApiKey).filter(ApiKey.id == key_id).first()
        db.delete(api_key)
        db.commit()
        # Add the migration
        command.stamp(alembic_cfg, "head")
        return RedirectResponse(url="/settings")        
    except Exception as e:
        return {"error": str(e)}    
  
