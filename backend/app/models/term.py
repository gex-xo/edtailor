from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.associations import lesson_terms


class Term(Base):
    """Glossary of fashion and tailoring terminology."""

    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String(200), unique=True, nullable=False, index=True)
    definition = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)  # Construction, Design, Tailoring
    pronunciation = Column(String(200), nullable=True)
    image_url = Column(String(500), nullable=True)
    language = Column(String(2), nullable=False, default='en', index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    lessons = relationship("Lesson", secondary=lesson_terms, back_populates="terms")

    def __repr__(self):
        return f"<Term {self.term}>"
