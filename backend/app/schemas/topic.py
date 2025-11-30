from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class TopicBase(BaseModel):
    """Base schema for Topic."""

    category_id: int
    name: str
    description: Optional[str] = None
    slug: str


class TopicCreate(TopicBase):
    """Schema for creating a Topic."""

    pass


class TopicResponse(TopicBase):
    """Schema for Topic responses."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
