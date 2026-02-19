from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json

from database import engine, get_db, Base
from models import Submission, SubmissionRequest

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # creates table if it doesn't exist
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/submit")
def submit(payload: SubmissionRequest, db: Session = Depends(get_db)):
    if len(payload.pixels) != 1024:
        raise HTTPException(status_code=400, detail="Must be exactly 1024 pixels (32x32)")

    submission = Submission(pixels=json.dumps(payload.pixels))
    db.add(submission)
    db.commit()

    return {"message": "Submitted successfully"}


@app.get("/api/next")
def get_next(db: Session = Depends(get_db)):
    submission = (
        db.query(Submission)
        .filter(Submission.displayed == False)
        .order_by(Submission.submitted_at.asc())
        .first()
    )

    if submission is None:
        return {"pixels": None, "message": "Queue is empty"}

    submission.displayed = True
    db.commit()

    return {
        "id": submission.id,
        "pixels": json.loads(submission.pixels),
        "submitted_at": submission.submitted_at
    }