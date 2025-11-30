"""Association tables for many-to-many relationships."""
from sqlalchemy import Table, Column, Integer, ForeignKey, Text
from app.core.database import Base

# Lesson <-> Fabric
lesson_fabrics = Table(
    "lesson_fabrics",
    Base.metadata,
    Column("lesson_id", Integer, ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True),
    Column("fabric_id", Integer, ForeignKey("fabrics.id", ondelete="CASCADE"), primary_key=True),
    Column("note", Text, nullable=True),
)

# Lesson <-> Garment
lesson_garments = Table(
    "lesson_garments",
    Base.metadata,
    Column("lesson_id", Integer, ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True),
    Column("garment_id", Integer, ForeignKey("garments.id", ondelete="CASCADE"), primary_key=True),
    Column("note", Text, nullable=True),
)

# Lesson <-> Term
lesson_terms = Table(
    "lesson_terms",
    Base.metadata,
    Column("lesson_id", Integer, ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True),
    Column("term_id", Integer, ForeignKey("terms.id", ondelete="CASCADE"), primary_key=True),
)

# Lesson <-> Tag
lesson_tags = Table(
    "lesson_tags",
    Base.metadata,
    Column("lesson_id", Integer, ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

# Fabric <-> Garment
fabric_garments = Table(
    "fabric_garments",
    Base.metadata,
    Column("fabric_id", Integer, ForeignKey("fabrics.id", ondelete="CASCADE"), primary_key=True),
    Column("garment_id", Integer, ForeignKey("garments.id", ondelete="CASCADE"), primary_key=True),
    Column("usage_note", Text, nullable=True),
)
