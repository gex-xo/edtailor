from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Category(Base):
    """Top-level organization for content (e.g., Fabrics, Tailoring, Styling)."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    icon_url = Column(String(500), nullable=True)
    language = Column(String(2), nullable=False, default='en', index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    topics = relationship("Topic", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category {self.name}>"
