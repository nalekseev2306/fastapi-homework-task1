from pydantic import BaseModel, Field
from datetime import datetime


class LocationCreate(BaseModel):
    name: str = Field(max_length=256)
    is_published: bool = True

class LocationResponse(LocationCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
