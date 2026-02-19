from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Price(BaseModel):
    """Schema for price information."""
    amount: float
    currency: str = "SGD"


class Schedule(BaseModel):
    """Schema for class schedule."""
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM


class CartItemCreate(BaseModel):
    """Schema for creating a cart item."""
    tutor_id: str
    title: str
    teacher: str
    description: str
    price: Price
    schedule: Schedule
    duration_minutes: int
    student: str
    image: str
    is_favourite: bool = False


class CartItem(BaseModel):
    """Schema for a cart item."""
    id: str
    title: str
    is_favourite: bool
    teacher: str
    description: str
    price: Price
    schedule: Schedule
    duration_minutes: int
    student: str
    image: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CartSummary(BaseModel):
    """Schema for cart summary."""
    total_lesson_minutes: int = Field(alias="totalLessonMinutes")
    processing_fee: Price = Field(alias="processingFee")
    subtotal: Price
    total: Price
    promo_code_applied: bool = Field(alias="promoCodeApplied")
    credits_button: bool = Field(alias="creditsButton")
    credit_points: int = Field(alias="credit points")

    class Config:
        populate_by_name = True


class CartResponse(BaseModel):
    """Schema for cart response."""
    classes: List[CartItem]
    summary: CartSummary

    class Config:
        populate_by_name = True


class PromoCodeRequest(BaseModel):
    """Schema for applying a promo code."""
    promo_code: str


class CartCheckoutRequest(BaseModel):
    """Schema for cart checkout request."""
    user_id: str
    payment_method: Optional[str] = None
