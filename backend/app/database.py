import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()


def _get_database_url() -> str:
    """
    Return a SQLAlchemy-compatible DATABASE_URL.

    Priority order:
    1. POSTGRES_CONNECTION_STRING (Zeabur format)
    2. DATABASE_URL (Heroku/other platforms)
    3. Individual POSTGRES_* variables (Zeabur alternative format)
    4. Local development default
    """
    # Check for Zeabur's POSTGRES_CONNECTION_STRING first
    zeabur_url = os.getenv("POSTGRES_CONNECTION_STRING")
    if zeabur_url:
        # Zeabur may use 'postgres://' scheme, convert to 'postgresql+psycopg2://'
        if zeabur_url.startswith("postgres://"):
            zeabur_url = zeabur_url.replace("postgres://", "postgresql+psycopg2://", 1)
        return zeabur_url

    # Check for standard DATABASE_URL (Heroku, etc.)
    url = os.getenv("DATABASE_URL")
    if url:
        # Heroku often uses 'postgres://' scheme, which SQLAlchemy 2.x dislikes.
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
        return url

    # Check for individual POSTGRES_* variables (Zeabur alternative format)
    postgres_host = os.getenv("POSTGRES_HOST")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")
    postgres_user = os.getenv("POSTGRES_USERNAME") or os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("POSTGRES_DATABASE") or os.getenv("POSTGRES_DB")

    if postgres_host and postgres_user and postgres_password and postgres_db:
        return f"postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

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


