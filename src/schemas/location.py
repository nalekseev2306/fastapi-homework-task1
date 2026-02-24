from pydantic import BaseModel, Field
# from typing import Optional
from datetime import datetime


class Location(BaseModel):
    id: int
    name: str = Field(max_length=256)
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now())
