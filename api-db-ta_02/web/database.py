#database.py

import asyncpg
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from . import models

DB_URL = "postgresql://av:password@timescale/av"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

async def get_db():
    async with asyncpg.create_pool(DB_URL) as pool:
        async with pool.acquire() as conn:
            async with conn.transaction():
                db = Session(engine)
                try:
                    yield db
                finally:
                    db.close()
