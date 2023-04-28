#schemas.py

from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel


class ApiKeyBase(BaseModel):
    name: str
    binance_key: str
    binance_secret: str


class ApiKeyCreate(ApiKeyBase):
    pass


class ApiKey(ApiKeyBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

