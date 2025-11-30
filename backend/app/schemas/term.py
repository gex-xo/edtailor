from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class TermBase(BaseModel):
    """Base schema for Term."""

    term: str
    definition: str
    category: Optional[str] = None
    pronunciation: Optional[str] = None
    image_url: Optional[str] = None


class TermCreate(TermBase):
    """Schema for creating a Term."""

    pass


class TermResponse(TermBase):
    """Schema for Term responses."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
