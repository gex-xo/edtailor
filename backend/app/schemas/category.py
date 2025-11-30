from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    """Base schema for Category."""

    name: str
    description: Optional[str] = None
    slug: str
    parent_id: Optional[int] = None
    icon_url: Optional[str] = None


class CategoryCreate(CategoryBase):
    """Schema for creating a Category."""

    pass


class CategoryResponse(CategoryBase):
    """Schema for Category responses."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
