from sqlalchemy import Column, Integer, Text, Boolean, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import List
from base import Base

class Submission(Base):
    __tablename__ = "submissions"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    pixels       = Column(Text, nullable=False)
    submitted_at = Column(DateTime, server_default=func.now())
    displayed    = Column(Boolean, default=False)

class SubmissionRequest(BaseModel):
    pixels: List[List[int]]