from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.otp import OTP
from app.core.config import settings


class OTPRepository:
    @staticmethod
    def create_otp(db: Session, email: str, otp_code: str, phone: str = None) -> OTP:
        """Create a new OTP. Phone is optional."""
        expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
        
        db_otp = OTP(
            email=email,
            phone=phone,
            otp_code=otp_code,
            expires_at=expires_at
        )
        db.add(db_otp)
        db.commit()
        db.refresh(db_otp)
        return db_otp

    @staticmethod
    def get_valid_otp(db: Session, email: str) -> OTP:
        """Get a valid (non-expired, non-verified) OTP for email."""
        return db.query(OTP).filter(
            OTP.email == email,
            OTP.is_verified == False,
            OTP.expires_at > datetime.utcnow()
        ).order_by(OTP.created_at.desc()).first()

    @staticmethod
    def verify_otp(db: Session, otp_id: str, email: str = None, phone: str = None) -> OTP:
        """Mark OTP as verified by otp_id and either email or phone."""
        filter_conditions = [OTP.id == otp_id]
        
        if email:
            filter_conditions.append(OTP.email == email)
        if phone:
            filter_conditions.append(OTP.phone == phone)
        
        otp = db.query(OTP).filter(*filter_conditions).first()
        if otp:
            otp.is_verified = True
            otp.verified_at = datetime.utcnow()
            db.commit()
            db.refresh(otp)
        return otp

    @staticmethod
    def increment_attempts(db: Session, otp_id: str) -> OTP:
        """Increment failed attempts for OTP."""
        otp = db.query(OTP).filter(OTP.id == otp_id).first()
        if otp:
            otp.attempts += 1
            db.commit()
            db.refresh(otp)
        return otp
