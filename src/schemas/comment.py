from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
from fastapi import HTTPException, status


class TextValidatorMixin:
    @field_validator("text", mode="before")
    @staticmethod
    def validate_text(value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        
        if not value or not value.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Name cannot be empty or whitespace"
            )
        
        return value.strip()


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
