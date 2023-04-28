#models.py

from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .base import Base



Base = declarative_base()



class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    binance_key = Column(String, unique=True, index=True)
    binance_secret = Column(String, unique=True, index=True)
    __table_args__ = (UniqueConstraint("binance_key"), UniqueConstraint("binance_secret"),)


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    code_path = Column(String, index=True)
    bot_id = Column(Integer, ForeignKey("bots.id"))
    bot2_id = Column(Integer, ForeignKey("bot2.id"))

    bot = relationship("Bot", back_populates="strategies")
    bot2 = relationship("Bot2", back_populates="strategies")



class Bot(Base):
    __tablename__ = "bots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))
    wallet_id = Column(Integer, ForeignKey("wallets.id"))

    strategies = relationship("Strategy", back_populates="bot")
    wallet = relationship("Wallet", back_populates="bots")


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    balance = Column(Float)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))

    bots = relationship("Bot", back_populates="wallet")
    bot2 = relationship("Bot2", back_populates="wallet")

class Bot2(Base):
    __tablename__ = "bot2"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))
    wallet_id = Column(Integer, ForeignKey("wallets.id"))

    strategies = relationship("Strategy", back_populates="bot2")
    wallet = relationship("Wallet", back_populates="bot2")  