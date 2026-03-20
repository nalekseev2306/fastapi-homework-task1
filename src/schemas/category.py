from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# модель для создания категории
class CategoryCreate(BaseModel):
    name: str = Field(max_length=256)
    description: str
    slug: str = Field(max_length=64, pattern=r'^[a-zA-Z0-9_-]+$')
    is_published: bool = True

# модель для возврата категории
class CategoryResponse(CategoryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# модель для обновления категории
class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=256)
    description: Optional[str] = None
    slug: Optional[str] = Field(default=None, max_length=64, pattern=r'^[a-zA-Z0-9_-]+$')
    is_published: Optional[bool] = None
