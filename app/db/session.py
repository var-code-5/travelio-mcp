# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URI,
    pool_pre_ping=True,  # Test connections for liveness
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database dependency to be used in FastAPI endpoints
def get_db():
    """
    Dependency for FastAPI endpoints to get database session.
    Ensures session is closed after request completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()