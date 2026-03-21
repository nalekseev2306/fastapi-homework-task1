from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str = Field(max_length=256, min_length=3)
    description: str
    slug: str = Field(max_length=64, min_length=3, pattern=r'^[a-zA-Z0-9_-]+$')
    is_published: bool = True


class CategoryResponse(CategoryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=256, min_length=3)
    description: Optional[str] = None
    slug: Optional[str] = Field(default=None, max_length=64,
                                min_length=3, pattern=r'^[a-zA-Z0-9_-]+$')
    is_published: Optional[bool] = None
