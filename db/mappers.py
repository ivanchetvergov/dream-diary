"""Data mappers for transforming DB models."""

from typing import Dict, Any, List
from .models import User, Dream, Classification, ChatHistory


class UserMapper:

    @staticmethod
    def to_dict(user: User) -> Dict[str, Any]:
        return {
            "id": user.id,
            "telegram_id": user.telegram_id,
            "username": user.username,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> User:
        return User(
            telegram_id=data["telegram_id"],
            username=data.get("username")
        )


class DreamMapper:

    @staticmethod
    def to_dict(dream: Dream) -> Dict[str, Any]:
        return {
            "id": dream.id,
            "user_id": dream.user_id,
            "text": dream.text,
            "analysis": dream.analysis,
            "emotions": dream.emotions,
            "created_at": dream.created_at.isoformat() if dream.created_at else None
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Dream:
        return Dream(
            user_id=data["user_id"],
            text=data["text"],
            analysis=data.get("analysis"),
            emotions=data.get("emotions")
        )


class ClassificationMapper:
    """Mapper for Classification model."""

    @staticmethod
    def to_dict(classification: Classification) -> Dict[str, Any]:
        return {
            "id": classification.id,
            "dream_id": classification.dream_id,
            "emotion": classification.emotion,
            "intensity": classification.intensity,
            "symbol": classification.symbol
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Classification:
        return Classification(
            dream_id=data["dream_id"],
            emotion=data["emotion"],
            intensity=data["intensity"],
            symbol=data.get("symbol")
        )


class ChatHistoryMapper:

    @staticmethod
    def to_dict(chat: ChatHistory) -> Dict[str, Any]:
        return {
            "id": chat.id,
            "user_id": chat.user_id,
            "message": chat.message,
            "response": chat.response,
            "timestamp": chat.timestamp.isoformat() if chat.timestamp else None
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> ChatHistory:
        return ChatHistory(
            user_id=data["user_id"],
            message=data["message"],
            response=data["response"]
        )


class EmotionMapper:

    @staticmethod
    def parse_emotions(emotions_str: str) -> List[Dict[str, Any]]:
        """Parse '[joy:1 (high), fear:0 (none), ...]' to list."""
        if not emotions_str or not emotions_str.startswith("["):
            return []
        items = emotions_str.strip("[]").split(", ")
        result = []
        for item in items:
            parts = item.split(":")
            if len(parts) == 2:
                emotion, rest = parts
                intensity_part = rest.split(" ")
                intensity = int(intensity_part[0]) if intensity_part[0].isdigit() else 0
                note = intensity_part[1].strip("()") if len(intensity_part) > 1 else ""
                result.append({"emotion": emotion, "intensity": intensity, "note": note})
        return result