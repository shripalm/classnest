from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class FavoriteTutor(Base):
    """FavoriteTutor model for storing user's favorite tutors."""
    __tablename__ = "favorite_tutors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    tutor_id = Column(UUID(as_uuid=True), ForeignKey("tutors.id"), nullable=False, index=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_favorite_tutors_user_id', 'user_id'),
        Index('idx_favorite_tutors_tutor_id', 'tutor_id'),
        Index('idx_favorite_tutors_user_tutor', 'user_id', 'tutor_id'),  # Composite index
    )

    def __repr__(self):
        return f"<FavoriteTutor(user_id={self.user_id}, tutor_id={self.tutor_id})>"
