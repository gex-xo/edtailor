from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Topic(Base):
    """Topics within categories (e.g., Natural Fibers, Suit Construction)."""

    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    language = Column(String(2), nullable=False, default='en', index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    category = relationship("Category", back_populates="topics")
    lessons = relationship("Lesson", back_populates="topic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Topic {self.name}>"
