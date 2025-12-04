import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()


def _get_database_url() -> str:
    """
    Return a SQLAlchemy-compatible DATABASE_URL.

    - In Heroku, we expect DATABASE_URL env var (often 'postgres://...').
      We convert it to 'postgresql+psycopg2://...'.
    - Locally, fall back to a sensible default if DATABASE_URL is not set.
    """
    url = os.getenv("DATABASE_URL")
    if url:
        # Heroku often uses 'postgres://' scheme, which SQLAlchemy 2.x dislikes.
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
        return url

    # Local development default
    return "postgresql+psycopg2://chao-peilu:@localhost:5431/chao-peilu"


DATABASE_URL = _get_database_url()

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


