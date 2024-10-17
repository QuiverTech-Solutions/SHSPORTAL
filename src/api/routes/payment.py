"""Route to manage payments."""

import logging
from decimal import Decimal
from typing import Any, Dict, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.db.repositories.payment import PaymentRepository
from src.models.payments import PaymentCreate, PaymentPublic
from src.models.users import UserPublic
from src.errors.database import DatabaseError

payment_router = APIRouter()
audit_logger = logging.getLogger("audit")


@payment_router.post(
    "/",
    response_model=PaymentPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    payment_create: PaymentCreate,
    payment_repo: PaymentRepository = Depends(),
) -> PaymentPublic:
    """Create a new payment."""
    try:
        audit_logger.info("Attempting to create a new payment.")
        payment = payment_repo.create_payment(new_payment=payment_create)
        audit_logger.info("Payment created successfully.")
        return payment
    except DatabaseError as e:
        handle_exception(e, "Database error during payment creation.")
    except Exception as e:
        handle_exception(e, "System error", is_system_error=True)


@payment_router.get(
    "/{payment_id}",
    response_model=PaymentPublic,
    status_code=status.HTTP_200_OK,
)
async def get_payment(
    payment_id: UUID,
    payment_repo: PaymentRepository = Depends(),
) -> PaymentPublic:
    """Retrieve payment details by ID."""
    try:
        return payment_repo.get_payment(id=payment_id)
    except DatabaseError as e:
        handle_exception(e, "Database error during payment retrieval.")
    except Exception as e:
        handle_exception(e, "System error", is_system_error=True)


@payment_router.get(
    "/",
    response_model=Decimal,
    status_code=status.HTTP_200_OK,
)
async def get_total_payments(
    student_id: Optional[UUID] = Query(None, description="Student's ID"),
    school_id: Optional[UUID] = Query(None, description="School's ID"),
    payment_repo: PaymentRepository = Depends(),
    current_user: UserPublic = Depends(),
) -> Decimal:
    """Get total payments for the current user."""
    try:
        total_payments = payment_repo.get_total_payments(
            student_id=student_id, school_id=school_id
        )
        return total_payments
    except DatabaseError as e:
        handle_exception(e, "Database error during total payments retrieval.")
    except Exception as e:
        handle_exception(e, "System error", is_system_error=True)


@payment_router.delete(
    "/{payment_id}",
    response_model=PaymentPublic,
    status_code=status.HTTP_200_OK,
)
async def delete_payment(
    payment_id: UUID,
    payment_repo: PaymentRepository = Depends(),
) -> PaymentPublic:
    """Delete a payment by ID."""
    try:
        deleted_payment = payment_repo.delete_payment(id=payment_id)
        return deleted_payment
    except DatabaseError as e:
        handle_exception(e, "Database error during payment deletion.")
    except Exception as e:
        handle_exception(e, "System error", is_system_error=True)


def handle_exception(e: Exception, message: str, is_system_error: bool = False) -> None:
    """Handle exceptions by logging and re-raising as HTTPExceptions."""
    audit_logger.exception(message, exc_info=e)
    if is_system_error:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
    raise HTTPException(status_code=400, detail=message)
