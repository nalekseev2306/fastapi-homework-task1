from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CommentCreate(BaseModel):
    text: str
    post_id: int

class CommentResponse(CommentCreate):
    id: int
    author_id: int
    created_at: datetime

class CommentUpdate(BaseModel):
    text: Optional[str] = None
