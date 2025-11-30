from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.associations import lesson_tags


class Tag(Base):
    """Tags for cross-referencing and categorizing content."""

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    lessons = relationship("Lesson", secondary=lesson_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag {self.name}>"
