from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from pgvector.sqlalchemy import Vector
from ..session import Base

class Face(Base):
    __tablename__ = "faces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id = Column(UUID(as_uuid=True), ForeignKey("images.id"), nullable=False)
    grab_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    embedding = Column(Vector(512))  # Assuming 512-dim embedding
    bounding_box = Column(JSON)  # Stores x, y, w, h

    image = relationship("Image", back_populates="faces")

# Update Image to have back_populates
from .image import Image
Image.faces = relationship("Face", back_populates="image", cascade="all, delete-orphan")
