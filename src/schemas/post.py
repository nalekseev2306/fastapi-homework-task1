from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# модель для создания поста
class PostCreate(BaseModel):
    title: str = Field(max_length=256)
    text: str
    pub_date: datetime
    location_id: Optional[int] = None
    category_id: int
    # image: Optional[str] = None
    is_published: bool = True

# модель для возврата поста
class PostResponse(PostCreate):
    id: int
    author_id: int

# модель для обновления поста
class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=256)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    # image: Optional[str] = None
    is_published: Optional[bool] = None
