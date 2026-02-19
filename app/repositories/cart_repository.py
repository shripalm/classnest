from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import uuid4
from typing import List, Tuple, Optional, Dict, Any
from app.models.cart import Cart, CartItem, CartPromoCode
from app.models.user import User
from app.models.tutor import Tutor
from datetime import datetime


class CartRepository:
    """Repository for cart operations."""

    @staticmethod
    def get_or_create_cart(db: Session, user_id: str) -> Cart:
        """Get existing cart or create a new one for user."""
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            cart = Cart(id=uuid4(), user_id=user_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        return cart

    @staticmethod
    def get_user_cart(db: Session, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's cart with all items and calculate summary."""
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        
        if not cart:
            return None

        cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
        
        if not cart_items:
            return {
                "classes": [],
                "summary": {
                    "totalLessonMinutes": 0,
                    "processingFee": {"amount": 0.0, "currency": "SGD"},
                    "subtotal": {"amount": 0.0, "currency": "SGD"},
                    "total": {"amount": 0.0, "currency": "SGD"},
                    "promoCodeApplied": False,
                    "creditsButton": True,
                    "credit points": 0
                }
            }

        # Format cart items
        classes = []
        total_minutes = 0
        subtotal_amount = 0.0

        for item in cart_items:
            classes.append({
                "id": str(item.tutor_id),
                "title": item.title,
                "isFavourite": item.is_favourite,
                "teacher": item.teacher,
                "description": item.description,
                "price": {
                    "amount": item.price_amount,
                    "currency": item.price_currency
                },
                "_isFavourite": item.is_favourite,
                "schedule": {
                    "date": item.schedule_date,
                    "time": item.schedule_time
                },
                "durationMinutes": item.duration_minutes,
                "student": item.student,
                "image": item.image
            })
            total_minutes += item.duration_minutes
            subtotal_amount += item.price_amount

        # Calculate processing fee (0.39% of subtotal for SGD)
        processing_fee = round(subtotal_amount * 0.0039, 2)
        total_amount = subtotal_amount + processing_fee

        # Check for applied promo codes
        promo_code = db.query(CartPromoCode).filter(
            CartPromoCode.cart_id == cart.id,
            CartPromoCode.is_active == True
        ).first()

        if promo_code:
            total_amount = max(0, total_amount - promo_code.discount_amount)

        return {
            "classes": classes,
            "summary": {
                "totalLessonMinutes": total_minutes,
                "processingFee": {
                    "amount": processing_fee,
                    "currency": "SGD"
                },
                "subtotal": {
                    "amount": subtotal_amount,
                    "currency": "SGD"
                },
                "total": {
                    "amount": total_amount,
                    "currency": "SGD"
                },
                "promoCodeApplied": promo_code is not None,
                "creditsButton": True,
                "credit points": int(total_amount * 100)  # 100 points per SGD
            }
        }

    @staticmethod
    def add_class_to_cart(
        db: Session, 
        user_id: str, 
        tutor_id: str,
        title: str,
        teacher: str,
        description: str,
        price_amount: float,
        price_currency: str,
        schedule_date: str,
        schedule_time: str,
        duration_minutes: int,
        student: str,
        image: str,
        is_favourite: bool = False
    ) -> bool:
        """Add a class to user's cart."""
        try:
            cart = CartRepository.get_or_create_cart(db, user_id)

            # Check if item already exists
            existing_item = db.query(CartItem).filter(
                CartItem.cart_id == cart.id,
                CartItem.tutor_id == tutor_id,
                CartItem.schedule_date == schedule_date,
                CartItem.schedule_time == schedule_time
            ).first()

            if existing_item:
                return False  # Item already in cart

            cart_item = CartItem(
                id=uuid4(),
                cart_id=cart.id,
                tutor_id=tutor_id,
                title=title,
                teacher=teacher,
                description=description,
                image=image,
                price_amount=price_amount,
                price_currency=price_currency,
                schedule_date=schedule_date,
                schedule_time=schedule_time,
                duration_minutes=duration_minutes,
                student=student,
                is_favourite=is_favourite
            )

            db.add(cart_item)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def remove_class_from_cart(db: Session, user_id: str, cart_item_id: str) -> bool:
        """Remove a class from user's cart."""
        try:
            cart = db.query(Cart).filter(Cart.user_id == user_id).first()
            
            if not cart:
                return False

            cart_item = db.query(CartItem).filter(
                CartItem.id == cart_item_id,
                CartItem.cart_id == cart.id
            ).first()

            if not cart_item:
                return False

            db.delete(cart_item)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def clear_cart(db: Session, user_id: str) -> bool:
        """Clear all items from user's cart."""
        try:
            cart = db.query(Cart).filter(Cart.user_id == user_id).first()
            
            if not cart:
                return False

            db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
            db.query(CartPromoCode).filter(CartPromoCode.cart_id == cart.id).delete()
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def apply_promo_code(
        db: Session, 
        user_id: str, 
        promo_code: str,
        discount_amount: float,
        discount_percentage: Optional[float] = None
    ) -> Tuple[bool, str]:
        """Apply a promo code to user's cart."""
        try:
            cart = db.query(Cart).filter(Cart.user_id == user_id).first()
            
            if not cart:
                return False, "Cart not found"

            # Deactivate any existing promo codes
            db.query(CartPromoCode).filter(
                CartPromoCode.cart_id == cart.id,
                CartPromoCode.is_active == True
            ).update({"is_active": False})

            # Apply new promo code
            promo = CartPromoCode(
                id=uuid4(),
                cart_id=cart.id,
                promo_code=promo_code,
                discount_amount=discount_amount,
                discount_percentage=discount_percentage,
                is_active=True
            )

            db.add(promo)
            db.commit()
            return True, "Promo code applied successfully"
        except Exception as e:
            db.rollback()
            return False, str(e)

    @staticmethod
    def remove_promo_code(db: Session, user_id: str) -> bool:
        """Remove promo code from user's cart."""
        try:
            cart = db.query(Cart).filter(Cart.user_id == user_id).first()
            
            if not cart:
                return False

            db.query(CartPromoCode).filter(
                CartPromoCode.cart_id == cart.id,
                CartPromoCode.is_active == True
            ).update({"is_active": False})
            
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def get_cart_item_count(db: Session, user_id: str) -> int:
        """Get number of items in user's cart."""
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        
        if not cart:
            return 0

        return db.query(CartItem).filter(CartItem.cart_id == cart.id).count()

    @staticmethod
    def toggle_favourite(db: Session, user_id: str, cart_item_id: str, is_favourite: bool) -> bool:
        """Toggle favourite status of a cart item."""
        try:
            cart = db.query(Cart).filter(Cart.user_id == user_id).first()
            
            if not cart:
                return False

            cart_item = db.query(CartItem).filter(
                CartItem.id == cart_item_id,
                CartItem.cart_id == cart.id
            ).first()

            if not cart_item:
                return False

            cart_item.is_favourite = is_favourite
            cart_item.updated_at = datetime.utcnow()
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
