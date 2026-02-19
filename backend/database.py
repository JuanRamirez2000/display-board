from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base

DATABASE_URL = "sqlite:///./submissions.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()