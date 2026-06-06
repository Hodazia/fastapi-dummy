'''
Basically here i will be making the DB as well as models which are gonna be used 

'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base
from database.models import User,Task

from core.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


Base.metadata.create_all(bind=engine)