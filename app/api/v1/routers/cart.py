from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from app.db.session import get_db_sync
from app.schemas.cart_schema import (
    CartResponse,
    CartItemCreate,
    PromoCodeRequest,
    CartCheckoutRequest,
    Price
)
from app.schemas.response import SuccessResponse
from app.repositories.cart_repository import CartRepository
from app.utils.logging import logger

router = APIRouter(prefix="/api/v1/cart", tags=["cart"])


@router.get("/{user_id}", response_model=SuccessResponse)
def get_user_cart(
    user_id: str = Path(..., description="User ID"),
    db: Session = Depends(get_db_sync)
):
    """
    Get user's cart with all booked classes and summary.
    
    **Returns:**
    - classes: List of classes in the cart
    - summary: Cart summary with pricing and promo information
    """
    try:
        cart_data = CartRepository.get_user_cart(db, user_id)
        
        if not cart_data:
            # Create empty cart
            CartRepository.get_or_create_cart(db, user_id)
            return SuccessResponse(
                status="success",
                message="Cart retrieved successfully",
                data={
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
            )
        
        return SuccessResponse(
            status="success",
            message="Cart retrieved successfully",
            data=cart_data
        )
    except Exception as e:
        logger.error(f"Error retrieving cart for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve cart"
        )


@router.post("/{user_id}/add", status_code=status.HTTP_200_OK, response_model=SuccessResponse)
def add_to_cart(
    user_id: str = Path(..., description="User ID"),
    item: CartItemCreate = None,
    db: Session = Depends(get_db_sync)
):
    """
    Add a class to user's cart.
    
    **Request body:**
    - tutor_id: UUID of the tutor
    - title: Class title (e.g., "Chinese", "Mathematics")
    - teacher: Teacher name
    - description: Class description
    - price: Price object with amount and currency
    - schedule: Schedule object with date (YYYY-MM-DD) and time (HH:MM)
    - duration_minutes: Duration of the class in minutes
    - student: Student name
    - image: Image URL of the tutor
    - is_favourite: Whether to mark as favourite (optional, default: false)
    """
    try:
        success = CartRepository.add_class_to_cart(
            db=db,
            user_id=user_id,
            tutor_id=item.tutor_id,
            title=item.title,
            teacher=item.teacher,
            description=item.description,
            price_amount=item.price.amount,
            price_currency=item.price.currency,
            schedule_date=item.schedule.date,
            schedule_time=item.schedule.time,
            duration_minutes=item.duration_minutes,
            student=item.student,
            image=item.image,
            is_favourite=item.is_favourite
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Class already exists in cart or failed to add"
            )
        
        # Return updated cart
        cart_data = CartRepository.get_user_cart(db, user_id)
        
        return SuccessResponse(
            status="success",
            message="Class added to cart successfully",
            data=cart_data
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding class to cart: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add class to cart"
        )


@router.delete("/{user_id}/remove/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    user_id: str = Path(..., description="User ID"),
    item_id: str = Path(..., description="Cart Item ID"),
    db: Session = Depends(get_db_sync)
):
    """
    Remove a specific class from user's cart.
    
    **Path parameters:**
    - user_id: UUID of the user
    - item_id: UUID of the cart item to remove
    """
    try:
        success = CartRepository.remove_class_from_cart(db, user_id, item_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing class from cart: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove class from cart"
        )


@router.delete("/{user_id}/clear", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    user_id: str = Path(..., description="User ID"),
    db: Session = Depends(get_db_sync)
):
    """
    Clear all items from user's cart and remove any applied promo codes.
    
    **Path parameters:**
    - user_id: UUID of the user
    """
    try:
        success = CartRepository.clear_cart(db, user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to clear cart"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing cart: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear cart"
        )


@router.post("/{user_id}/apply-promo", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def apply_promo_code(
    user_id: str = Path(..., description="User ID"),
    promo_request: PromoCodeRequest = None,
    discount_amount: float = Query(0.0, description="Discount amount in currency"),
    discount_percentage: Optional[float] = Query(None, description="Discount percentage (optional)"),
    db: Session = Depends(get_db_sync)
):
    """
    Apply a promo code to user's cart and recalculate totals.
    
    **Path parameters:**
    - user_id: UUID of the user
    
    **Request body:**
    - promo_code: The promo code to apply
    
    **Query parameters:**
    - discount_amount: Amount to discount (required)
    - discount_percentage: Percentage discount (optional)
    """
    try:
        success, message = CartRepository.apply_promo_code(
            db=db,
            user_id=user_id,
            promo_code=promo_request.promo_code,
            discount_amount=discount_amount,
            discount_percentage=discount_percentage
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Return updated cart with promo applied
        cart_data = CartRepository.get_user_cart(db, user_id)
        
        return SuccessResponse(
            status="success",
            message="Promo code applied successfully",
            data=cart_data
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error applying promo code: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to apply promo code"
        )


@router.delete("/{user_id}/remove-promo", status_code=status.HTTP_204_NO_CONTENT)
def remove_promo_code(
    user_id: str = Path(..., description="User ID"),
    db: Session = Depends(get_db_sync)
):
    """
    Remove the applied promo code from user's cart.
    
    **Path parameters:**
    - user_id: UUID of the user
    """
    try:
        success = CartRepository.remove_promo_code(db, user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove promo code"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing promo code: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove promo code"
        )


@router.get("/{user_id}/count", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def get_cart_item_count(
    user_id: str = Path(..., description="User ID"),
    db: Session = Depends(get_db_sync)
):
    """
    Get the number of items currently in user's cart.
    
    **Path parameters:**
    - user_id: UUID of the user
    
    **Returns:**
    - count: Number of items in the cart
    """
    try:
        count = CartRepository.get_cart_item_count(db, user_id)
        
        return SuccessResponse(
            status="success",
            message="Cart item count retrieved successfully",
            data={"count": count}
        )
    except Exception as e:
        logger.error(f"Error getting cart item count: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get cart item count"
        )


@router.patch("/{user_id}/favourite/{item_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
def toggle_favourite(
    user_id: str = Path(..., description="User ID"),
    item_id: str = Path(..., description="Cart Item ID"),
    is_favourite: bool = Query(..., description="Set to true or false"),
    db: Session = Depends(get_db_sync)
):
    """
    Toggle favourite status of a cart item.
    
    **Path parameters:**
    - user_id: UUID of the user
    - item_id: UUID of the cart item
    
    **Query parameters:**
    - is_favourite: true to mark as favourite, false to unmark
    """
    try:
        success = CartRepository.toggle_favourite(db, user_id, item_id, is_favourite)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
        
        # Return updated cart
        cart_data = CartRepository.get_user_cart(db, user_id)
        
        return SuccessResponse(
            status="success",
            message="Favourite status updated successfully",
            data=cart_data
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating favourite status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update favourite status"
        )
