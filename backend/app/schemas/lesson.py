from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class LessonBase(BaseModel):
    """Base schema for Lesson."""

    topic_id: int
    title: str
    slug: str
    summary: Optional[str] = None
    content: str
    reading_time_minutes: Optional[int] = None
    difficulty_level: Optional[str] = None
    image_url: Optional[str] = None


class LessonCreate(LessonBase):
    """Schema for creating a Lesson."""

    pass


class LessonResponse(LessonBase):
    """Schema for Lesson responses."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
