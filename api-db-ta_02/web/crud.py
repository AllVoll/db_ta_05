from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models, schemas

def create_api_key(db: Session, api_key: schemas.ApiKeyCreate):
    db_api_key = models.ApiKey(name=api_key.name, binance_key=api_key.binance_key, binance_secret=api_key.binance_secret)
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return db_api_key
