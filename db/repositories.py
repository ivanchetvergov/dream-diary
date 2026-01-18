"""Repository classes for DB operations."""

from sqlalchemy.orm import Session
from typing import List, Optional
from .models import User, Dream, Classification, ChatHistory
from .database import SessionLocal


class UserRepository:
    """Repository for User model."""

    @staticmethod
    def get_or_create(telegram_id: int, username: str = None) -> User:
        with SessionLocal() as session:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            if not user:
                user = User(telegram_id=telegram_id, username=username)
                session.add(user)
                session.commit()
                session.refresh(user)
            return user

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        with SessionLocal() as session:
            return session.query(User).filter_by(id=user_id).first()


class DreamRepository:
    """Repository for Dream model."""

    @staticmethod
    def create(user_id: int, text: str, analysis: str = None, language: str = "en") -> Dream:
        try:
            print(f"[DreamRepository] Creating dream for user_id={user_id}")
            with SessionLocal() as session:
                dream = Dream(
                    user_id=user_id,
                    text=text,
                    raw_analysis={"content": analysis} if analysis else {},
                    language=language
                )
                session.add(dream)
                print(f"[DreamRepository] Dream added to session, committing...")
                session.commit()
                print(f"[DreamRepository] Commit successful, refreshing...")
                session.refresh(dream)
                print(f"[DreamRepository] Dream created successfully with id={dream.id}")
                return dream
        except Exception as e:
            print(f"❌ [DreamRepository] Error creating dream: {e}")
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def get_by_user(user_id: int) -> List[Dream]:
        with SessionLocal() as session:
            return session.query(Dream).filter_by(user_id=user_id).all()

    @staticmethod
    def get_by_id(dream_id: int) -> Optional[Dream]:
        with SessionLocal() as session:
            return session.query(Dream).filter_by(id=dream_id).first()


class ClassificationRepository:
    """Repository for Classification model."""

    @staticmethod
    def create(dream_id: int, emotion: str, intensity: int, symbol: str = None) -> Classification:
        try:
            print(f"[ClassificationRepository] Creating classification for dream_id={dream_id}, emotion={emotion}")
            with SessionLocal() as session:
                classification = Classification(
                    dream_id=dream_id,
                    model="claude-emotions",
                    labels=[emotion] if emotion else [],
                    scores={emotion: intensity} if emotion else {}
                )
                session.add(classification)
                session.commit()
                session.refresh(classification)
                print(f"[ClassificationRepository] Classification created with id={classification.id}")
                return classification
        except Exception as e:
            print(f"[ClassificationRepository] Error: {e}")
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def get_by_dream(dream_id: int) -> List[Classification]:
        with SessionLocal() as session:
            return session.query(Classification).filter_by(dream_id=dream_id).all()


class ChatHistoryRepository:
    """Repository for ChatHistory model."""

    @staticmethod
    def add_message(user_id: int, message: str, response: str) -> ChatHistory:
        try:
            print(f"[ChatHistoryRepository] Adding message for user_id={user_id}")
            with SessionLocal() as session:
                chat = ChatHistory(user_id=user_id, message=message, response=response)
                session.add(chat)
                session.commit()
                session.refresh(chat)
                print(f"[ChatHistoryRepository] Chat history created with id={chat.id}")
                return chat
        except Exception as e:
            print(f"[ChatHistoryRepository] Error: {e}")
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def get_by_user(user_id: int, limit: int = 20) -> List[ChatHistory]:
        with SessionLocal() as session:
            return session.query(ChatHistory).filter_by(user_id=user_id).order_by(ChatHistory.timestamp.desc()).limit(limit).all()
