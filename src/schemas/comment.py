from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CommentCreate(BaseModel):
    text: str
    user_id: int # временно, пока нет авторизации
    post_id: int


class CommentResponse(CommentCreate):
    id: int
    # user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CommentUpdate(BaseModel):
    text: Optional[str] = None
