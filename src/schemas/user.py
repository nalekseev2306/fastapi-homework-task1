from pydantic import BaseModel, EmailStr, SecretStr, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: EmailStr
    password: SecretStr
    first_name: str = Field(min_length=3, max_length=64)
    last_name: str = Field(min_length=3, max_length=64)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=64)
    email: Optional[EmailStr] = None
    password: Optional[SecretStr] = None
    first_name: Optional[str] = Field(default=None, min_length=3, max_length=64)
    last_name: Optional[str] = Field(default=None, min_length=3, max_length=64)
