from pydantic import BaseModel, EmailStr, SecretStr, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: int
    username: str = Field(min_length=3, max_length=64)
    email: EmailStr
    password: SecretStr
    first_name: str = Field(min_length=3, max_length=64)
    last_name: str = Field(min_length=3, max_length=64)

class Category(BaseModel):
    id: int
    title: str = Field(max_length=256)
    description: str
    slug: str = Field(max_length=64, pattern=r'^[a-zA-Z0-9_-]+$')
    is_published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now())

class Location(BaseModel):
    id: int
    name: str = Field(max_length=256)
    is_published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now())

class Post(BaseModel):
    id: int
    title: str = Field(max_length=256)
    text: str
    pub_date: datetime
    author_id: int
    location_id: Optional[int] = Field(default=None)
    category_id: int
    # image: Optional[str] = Field(default=None)
    is_published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now())

class Comment(BaseModel):
    id: int
    text: str
    post_id: int
    author_id: int
    created_at: datetime = Field(default_factory=datetime.now())
