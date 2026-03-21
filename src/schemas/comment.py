from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
from fastapi import HTTPException, status


class TextValidatorMixin:
    @field_validator("text", mode="before")
    @staticmethod
    def check_text(text: Optional[str]) -> Optional[str]:
        if text is None:
            return text

        if not text:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Text cannot be blank"
            )
        
        return text


class CommentCreate(BaseModel, TextValidatorMixin):
    text: str
    user_id: int # временно, пока нет авторизации
    post_id: int


class CommentResponse(CommentCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CommentUpdate(BaseModel, TextValidatorMixin):
    text: Optional[str] = None
