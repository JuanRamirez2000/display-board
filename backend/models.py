from pydantic import BaseModel
from typing import List

class SubmissionRequest(BaseModel):
    pixels: List[List[int]]  # list of 1024 [R, G, B] values