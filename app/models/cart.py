from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Float, ForeignKey, Index, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Cart(Base):
    """Cart model for storing user shopping cart."""
    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_carts_user_id', 'user_id'),
    )

    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id})>"


class CartItem(Base):
    """CartItem model for storing individual items in a cart."""
    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.id"), nullable=False, index=True)
    tutor_id = Column(UUID(as_uuid=True), ForeignKey("tutors.id"), nullable=False, index=True)
    
    # Class/Subject information
    title = Column(String(255), nullable=False)
    teacher = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image = Column(String(500), nullable=True)
    
    # Pricing information
    price_amount = Column(Float, nullable=False)
    price_currency = Column(String(10), default="SGD", nullable=False)
    
    # Schedule information
    schedule_date = Column(String(10), nullable=False)  # Format: YYYY-MM-DD
    schedule_time = Column(String(5), nullable=False)   # Format: HH:MM
    duration_minutes = Column(Integer, nullable=False)
    
    # Student information
    student = Column(String(255), nullable=False)
    
    # Status
    is_favourite = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_cart_items_cart_id', 'cart_id'),
        Index('idx_cart_items_tutor_id', 'tutor_id'),
    )

    cart = relationship("Cart", back_populates="cart_items")

    def __repr__(self):
        return f"<CartItem(id={self.id}, title={self.title}, price={self.price_amount})>"


class CartPromoCode(Base):
    """CartPromoCode model for storing promo codes applied to carts."""
    __tablename__ = "cart_promo_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.id"), nullable=False, index=True)
    promo_code = Column(String(100), nullable=False)
    discount_amount = Column(Float, nullable=False)
    discount_percentage = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    applied_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_cart_promo_codes_cart_id', 'cart_id'),
    )

    def __repr__(self):
        return f"<CartPromoCode(id={self.id}, promo_code={self.promo_code})>"
