from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class GarmentBase(BaseModel):
    """Base schema for Garment."""

    name: str
    description: Optional[str] = None
    garment_type: Optional[str] = None
    formality_level: Optional[str] = None
    construction_details: Optional[str] = None
    key_features: Optional[str] = None
    historical_context: Optional[str] = None
    styling_tips: Optional[str] = None
    image_url: Optional[str] = None


class GarmentCreate(GarmentBase):
    """Schema for creating a Garment."""

    pass


class GarmentResponse(GarmentBase):
    """Schema for Garment responses."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
