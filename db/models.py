"""Database models for DreamWeaver AI using SQLAlchemy."""

from sqlalchemy import Column, String, Text, Boolean, TIMESTAMP, BigInteger, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(255))
    language = Column(String(2), default="en")  # 'en' or 'ru'
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    settings = Column(JSON, default=dict)       # JSONB for extensible settings

    dreams = relationship("Dream", back_populates="user")
    chat_history = relationship("ChatHistory", back_populates="user")

class Dream(Base):
    __tablename__ = "dreams"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=False)
    language = Column(String(2), default="en")
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    raw_analysis = Column(JSON, default=dict)   # Claude analysis
    processed = Column(Boolean, default=False)

    user = relationship("User", back_populates="dreams")
    classifications = relationship("Classification", back_populates="dream")

class Classification(Base):
    __tablename__ = "classifications"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    dream_id = Column(BigInteger, ForeignKey("dreams.id"), nullable=False)
    model = Column(String(50), nullable=False)  # e.g., 'roberta-emotions'
    labels = Column(JSON, nullable=False)       # Array of labels
    scores = Column(JSON, nullable=False)       # Dict of scores
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    dream = relationship("Dream", back_populates="classifications")

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="chat_history")
