from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TagBase(BaseModel):
    """Base schema for Tag."""

    name: str


class TagCreate(TagBase):
    """Schema for creating a Tag."""

    pass


class TagResponse(TagBase):
    """Schema for Tag responses."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
