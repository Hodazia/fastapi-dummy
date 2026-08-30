from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base
from database.config import DB_URL
import database.models  # noqa: F401 — register models before create_all

engine = create_engine(
    DB_URL,
    echo=True,
    pool_size=10,
    max_overflow=10
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base.metadata.create_all(bind=engine)