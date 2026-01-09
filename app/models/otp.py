from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean, Index, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base


class OTP(Base):
    """OTP model for storing OTP information."""
    __tablename__ = "otps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=True)  # Optional phone number for OTP
    otp_code = Column(String(10), nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    verified_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index('idx_otps_email', 'email'),
    )

    def __repr__(self):
        return f"<OTP(id={self.id}, email={self.email})>"
