from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./submissions.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite only
)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    """
    Hands out a database session and ensures it always gets closed.
    Think of it like borrowing a tool from a shed — you always return it
    when you're done, even if something goes wrong mid-task.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()