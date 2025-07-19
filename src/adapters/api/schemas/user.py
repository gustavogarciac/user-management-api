from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        unique=True,
    )
    email: EmailStr = Field(..., unique=True)
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None, min_length=3, max_length=50, unique=True
    )
    email: Optional[EmailStr] = Field(None, unique=True)


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    items: List[UserResponse]
    total_items: int = Field(..., ge=0)
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1, le=100)


class UserListQueryParams(BaseModel):
    page: int = Field(1, description='Page number (1-based)')
    page_size: int = Field(
        10,
        description='Number of items per page',
    )
    query: Optional[str] = Field(
        None,
        description='Search query for name or email',
    )
    order_by: Optional[str] = Field(
        None,
        description='Field to order by (name, email, created_at)',
    )
    order_direction: Optional[str] = Field(
        None,
        description='Order direction (asc, desc)',
    )
    username: Optional[str] = Field(None, description='Filter by username')
    email: Optional[str] = Field(None, description='Filter by email')
