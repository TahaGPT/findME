from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..session import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    storage_path = Column(String, nullable=False)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())
    checksum = Column(String, unique=True, index=True)
