from pydantic import BaseModel, EmailStr, field_validator
from fastapi import HTTPException, status
from typing import Optional


class UserValidatorsMixin:
    @field_validator("username", "first_name", "last_name", mode="before")
    @staticmethod
    def validate_name(value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        
        if not value or not value.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Field cannot be empty or whitespace"
            )
        
        stripped = value.strip()
        
        if len(stripped) < 3:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Field must be at least 3 characters long"
            )
        
        if len(stripped) > 64:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Field cannot exceed 64 characters"
            )
        
        return stripped
    
    @field_validator("email", mode="before")
    @staticmethod
    def validate_email(value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        
        if not value or not value.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Email cannot be empty or whitespace"
            )
        
        return value.strip().lower()
    
    @field_validator("password", mode="before")
    @staticmethod
    def validate_password(value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        
        if not value or not value.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Password cannot be empty or whitespace"
            )
        
        if len(value) < 6:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Password must be at least 6 characters long"
            )
        
        return value


class UserCreate(UserValidatorsMixin, BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    
    class Config:
        from_attributes = True


class UserUpdate(UserValidatorsMixin, BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
