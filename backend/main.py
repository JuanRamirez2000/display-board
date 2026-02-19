from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json

from database import init_db, get_connection
from models import SubmissionRequest

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  
    yield       


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this down later when you have a real domain
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/submit")
def submit(payload: SubmissionRequest):
    """Accept a 32x32 pixel drawing and add it to the queue."""
    if len(payload.pixels) != 1024:
        raise HTTPException(status_code=400, detail="Must be exactly 1024 pixels (32x32)")

    conn = get_connection()
    conn.execute(
        "INSERT INTO submissions (pixels) VALUES (?)",
        (json.dumps(payload.pixels),)  # serialize list → JSON string
    )
    conn.commit()
    conn.close()

    return {"message": "Submitted successfully"}


@app.get("/api/next")
def get_next():
    """Return the oldest undisplayed submission and mark it as displayed."""
    conn = get_connection()

    row = conn.execute(
        "SELECT * FROM submissions WHERE displayed = 0 ORDER BY submitted_at ASC LIMIT 1"
    ).fetchone()

    if row is None:
        conn.close()
        return {"pixels": None, "message": "Queue is empty"}

    # Mark it as displayed
    conn.execute("UPDATE submissions SET displayed = 1 WHERE id = ?", (row["id"],))
    conn.commit()
    conn.close()

    return {
        "id": row["id"],
        "pixels": json.loads(row["pixels"]),  # deserialize JSON string → list
        "submitted_at": row["submitted_at"]
    }