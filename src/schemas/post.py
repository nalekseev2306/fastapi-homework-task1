from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from fastapi import HTTPException, status


class TitleValidatorMixin:
    @field_validator("title", mode="before")
    @staticmethod
    def check_title(title: str):
        if not title:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Title cannot be blank"
            )
        
        return title


class PostCreate(BaseModel, TitleValidatorMixin):
    title: str = Field(max_length=256, min_length=3)
    text: str
    pub_date: datetime
    user_id: int # временно, пока нет авторизации
    location_id: int
    category_id: int
    # image: Optional[str] = None
    is_published: bool = True


class PostResponse(PostCreate):
    id: int
    # user_id: int

    class Config:
        from_attributes = True


class PostUpdate(BaseModel, TitleValidatorMixin):
    title: Optional[str] = Field(default=None, max_length=256)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    # image: Optional[str] = None
    is_published: Optional[bool] = None
