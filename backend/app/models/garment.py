from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.associations import lesson_garments, fabric_garments


class Garment(Base):
    """Clothing items encyclopedia with construction and styling details."""

    __tablename__ = "garments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    garment_type = Column(String(100), nullable=True)  # Outerwear, Shirt, Trousers, Accessory
    formality_level = Column(String(100), nullable=True)  # Casual, Business, Formal
    construction_details = Column(Text, nullable=True)
    key_features = Column(Text, nullable=True)
    historical_context = Column(Text, nullable=True)
    styling_tips = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    language = Column(String(2), nullable=False, default='en', index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    lessons = relationship("Lesson", secondary=lesson_garments, back_populates="garments")
    fabrics = relationship("Fabric", secondary=fabric_garments, back_populates="garments")

    def __repr__(self):
        return f"<Garment {self.name}>"
