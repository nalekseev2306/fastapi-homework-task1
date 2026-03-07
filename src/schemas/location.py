from pydantic import BaseModel, Field
from datetime import datetime


class LocationCreate(BaseModel):
    name: str = Field(max_length=256)

class LocationResponse(BaseModel):
    id: int
    name: str
    is_published: bool
    created_at: datetime
