from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from fastapi import HTTPException, status


class LocationCreate(BaseModel):
    name: str = Field(max_length=256, min_length=3)
    is_published: bool = True

    @field_validator("name", mode="before")
    @staticmethod
    def check_name(name: str):
        if not name:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Name cannot be blank"
            )

        return name


class LocationResponse(BaseModel):
    id: int
    name: str
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True
