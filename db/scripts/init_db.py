"""Script to initialize the database: create tables."""

from db.database import engine
from db.models import Base

def init_db():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()
