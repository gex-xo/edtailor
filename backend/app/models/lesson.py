from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.associations import lesson_fabrics, lesson_garments, lesson_terms, lesson_tags


class Lesson(Base):
    """Individual learning units with content."""

    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(300), nullable=False)
    slug = Column(String(300), unique=True, nullable=False, index=True)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    reading_time_minutes = Column(Integer, nullable=True)
    difficulty_level = Column(String(50), nullable=True)  # Beginner, Intermediate, Advanced
    image_url = Column(String(500), nullable=True)
    language = Column(String(2), nullable=False, default='en', index=True)  # ISO 639-1 code: en, ru, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    topic = relationship("Topic", back_populates="lessons")

    # Many-to-many relationships
    fabrics = relationship("Fabric", secondary=lesson_fabrics, back_populates="lessons")
    garments = relationship("Garment", secondary=lesson_garments, back_populates="lessons")
    terms = relationship("Term", secondary=lesson_terms, back_populates="lessons")
    tags = relationship("Tag", secondary=lesson_tags, back_populates="lessons")

    def __repr__(self):
        return f"<Lesson {self.title}>"
