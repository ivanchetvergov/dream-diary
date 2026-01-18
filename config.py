"""Configuration module for DreamWeaver AI."""

import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Central configuration class."""

    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    MODEL_DIR = os.path.join(BASE_DIR, "model")
    LOG_DIR = os.path.join(BASE_DIR, "logs")

    # ML settings
    MAX_SEQ_LEN = 512
    BATCH_SIZE = 16
    LEARNING_RATE = 2e-5
    EPOCHS = 3


    # API keys (set via env vars)
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
    ANTHROPIC_TOKEN = os.getenv("ANTHROPIC_API_KEY", "")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/dreamweaver")

    @classmethod
    def get(cls, key: str) -> Any:
        """Get config value by key."""
        return getattr(cls, key.upper(), None)
