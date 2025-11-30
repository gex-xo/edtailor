from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.associations import lesson_fabrics, fabric_garments


class Fabric(Base):
    """Fabric reference library with properties and characteristics."""

    __tablename__ = "fabrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    fiber_content = Column(String(200), nullable=True)  # e.g., "100% Wool"
    fiber_type = Column(String(100), nullable=True)  # Natural, Synthetic, Semi-synthetic
    weight = Column(String(100), nullable=True)  # Lightweight, Medium, Heavy
    weave_type = Column(String(100), nullable=True)  # Plain, Twill, Satin, Knit
    drape = Column(String(100), nullable=True)  # Soft, Structured, Crisp
    texture = Column(String(200), nullable=True)
    care_instructions = Column(Text, nullable=True)
    common_uses = Column(Text, nullable=True)
    properties = Column(JSON, nullable=True)  # Flexible field for additional properties
    season = Column(String(100), nullable=True)  # Summer, Winter, All-season
    image_url = Column(String(500), nullable=True)
    language = Column(String(2), nullable=False, default='en', index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    lessons = relationship("Lesson", secondary=lesson_fabrics, back_populates="fabrics")
    garments = relationship("Garment", secondary=fabric_garments, back_populates="fabrics")

    def __repr__(self):
        return f"<Fabric {self.name}>"
