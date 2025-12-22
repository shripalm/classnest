from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Child(Base):
    """Child model for storing child information."""
    __tablename__ = "children"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20), nullable=True)
    photo = Column(String(500), nullable=True)
    interest = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_children_parent_id', 'parent_id'),
    )

    parent = relationship("User", back_populates="children")

    def __repr__(self):
        return f"<Child(id={self.id}, name={self.name}, parent_id={self.parent_id})>"
