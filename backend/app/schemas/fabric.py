from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime


class FabricBase(BaseModel):
    """Base schema for Fabric."""

    name: str
    description: Optional[str] = None
    fiber_content: Optional[str] = None
    fiber_type: Optional[str] = None
    weight: Optional[str] = None
    weave_type: Optional[str] = None
    drape: Optional[str] = None
    texture: Optional[str] = None
    care_instructions: Optional[str] = None
    common_uses: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    season: Optional[str] = None
    image_url: Optional[str] = None


class FabricCreate(FabricBase):
    """Schema for creating a Fabric."""

    pass


class FabricResponse(FabricBase):
    """Schema for Fabric responses."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
