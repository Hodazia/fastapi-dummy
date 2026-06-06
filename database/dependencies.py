from database.start_db import SessionLocal

'''
understand the dependencies

'''

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()