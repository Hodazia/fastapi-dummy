from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import get_settings
from database.base import Base
from database.config import DB_URL
import database.models  # noqa: F401 — register models before create_all

settings = get_settings()

engine = create_engine(
    DB_URL,
    echo=settings.sql_echo,
    pool_size=10,
    max_overflow=10,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
