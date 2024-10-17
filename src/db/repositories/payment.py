"""Payment repository."""

import logging
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from databases import Database

from src.db.repositories.base import BaseRepository
from src.decorators.db import (
    handle_get_database_exceptions,
    handle_post_database_exceptions,
)
from src.enums.event_type import EventType
from src.errors.core import ValueError
from src.errors.database import NotFoundError
from src.models.payment import PaymentCreate, PaymentInDb

CREATE_PAYMENT_QUERY = """
INSERT INTO payments (organization_id, vote_event_id, ticket_event_id, event_type, phone_number, amount, reference, affiliate_user_id)
VALUES (:organization_id, :vote_event_id, :ticket_event_id, :event_type, :phone_number, :amount, :reference, :affiliate_user_id)
RETURNING id, organization_id, vote_event_id, ticket_event_id, event_type, phone_number, amount, reference, affiliate_user_id, created_at, updated_at, is_deleted
"""

GET_PAYMENT_BY_ID_QUERY = """
SELECT id, organization_id, vote_event_id, ticket_event_id, event_type, amount, phone_number, reference, affiliate_user_id, created_at, updated_at, is_deleted
FROM payments
WHERE id = :id AND is_deleted = FALSE
"""

GET_PAYMENTS_QUERY = """
SELECT id, organization_id, vote_event_id, ticket_event_id, event_type, amount, phone_number, reference, affiliate_user_id, created_at, updated_at, is_deleted
FROM payments
WHERE is_deleted = FALSE
ORDER BY created_at DESC
"""

GET_PAYMENTS_BY_ORGANIZATION_ID_QUERY = """
SELECT id, organization_id, vote_event_id, ticket_event_id, event_type, amount, phone_number, reference, affiliate_user_id, created_at, updated_at, is_deleted
FROM payments
WHERE organization_id = :organization_id AND is_deleted = FALSE
ORDER BY created_at DESC
"""

GET_PAYMENTS_BY_VOTE_EVENT_ID_QUERY = """
SELECT id, organization_id, vote_event_id, ticket_event_id, event_type, amount, phone_number, reference, affiliate_user_id, created_at, updated_at, is_deleted
FROM payments
WHERE vote_event_id = :vote_event_id AND is_deleted = FALSE
ORDER BY created_at DESC
"""

GET_PAYMENTS_BY_TICKET_EVENT_ID_QUERY = """
SELECT id, organization_id, vote_event_id, ticket_event_id, event_type, amount, phone_number, reference, affiliate_user_id, created_at, updated_at, is_deleted
FROM payments
WHERE ticket_event_id = :ticket_event_id AND is_deleted = FALSE
ORDER BY created_at DESC
"""

GET_PAYMENT_BY_REFERENCE_QUERY = """
SELECT id, organization_id, vote_event_id, ticket_event_id, event_type, amount, phone_number, reference, affiliate_user_id, created_at, updated_at, is_deleted
FROM payments
WHERE reference = :reference AND is_deleted = FALSE
"""

GET_TOTAL_PAYMENTS_BY_ORGANIZATION_ID_QUERY = """
SELECT SUM(amount) AS total_payments
FROM payments
WHERE organization_id = :organization_id AND is_deleted = FALSE
"""

GET_TOTAL_PAYMENTS_BY_VOTE_EVENT_ID_QUERY = """
SELECT SUM(amount) AS total_payments
FROM payments
WHERE vote_event_id = :vote_event_id AND is_deleted = FALSE
"""

GET_TOTAL_PAYMENTS_BY_TICKET_EVENT_ID_QUERY = """
SELECT SUM(amount) AS total_payments
FROM payments
WHERE ticket_event_id = :ticket_event_id AND is_deleted = FALSE
"""

GET_TOTAL_PAYMENTS_BY_EVENT_TYPE_QUERY = """
SELECT SUM(amount) AS total_payments
FROM payments
WHERE event_type = :event_type AND is_deleted = FALSE
"""

DELETE_PAYMENT_BY_ID_QUERY = """
UPDATE payments
SET is_deleted = TRUE
WHERE id = :id AND is_deleted = FALSE
RETURNING id, organization_id, vote_event_id, ticket_event_id, event_type, amount, reference, affiliate_user_id, created_at, updated_at, is_deleted
"""
audit_logger = logging.getLogger("audit")


class PaymentRepository(BaseRepository):
    """Payment repository."""

    def __init__(self, db: Database) -> None:
        """Constructor for Payment repository."""
        super().__init__(db)

    @handle_post_database_exceptions(
        "Payment", "Event id, organization id", "Reference"
    )
    async def create_payment(self, *, new_payment: PaymentCreate) -> PaymentInDb:
        """Create a new payment."""
        audit_logger.info("Adding payment...", new_payment.model_dump())
        created_payment = await self.db.fetch_one(
            query=CREATE_PAYMENT_QUERY, values=new_payment.model_dump()
        )
        audit_logger.info("Payment, added completed")

        return PaymentInDb(**created_payment)

    @handle_get_database_exceptions("Payment")
    async def get_payment(
        self, *, id: UUID = None, reference: str = None
    ) -> PaymentInDb:
        """Get payment by id and organization id."""
        search_criteria = {
            "id": (GET_PAYMENT_BY_ID_QUERY, id),
            "reference": (GET_PAYMENT_BY_REFERENCE_QUERY, reference),
        }

        for field, (query, value) in search_criteria.items():
            if value:
                payment = await self.db.fetch_one(query=query, values={field: value})
                if payment:
                    return PaymentInDb(**payment)
                raise NotFoundError(entity_name=field)

        raise ValueError("Please provide a valid payment reference or id")

    @handle_get_database_exceptions("Payment")
    async def get_payments(
        self,
        *,
        organization_id: UUID = None,
        vote_event_id: UUID = None,
        ticket_event_id: UUID = None,
    ) -> List[PaymentInDb]:
        """Get all payments."""
        search_criteria = {
            "organization_id": (GET_PAYMENTS_BY_ORGANIZATION_ID_QUERY, organization_id),
            "vote_event_id": (GET_PAYMENTS_BY_VOTE_EVENT_ID_QUERY, vote_event_id),
            "ticket_event_id": (GET_PAYMENTS_BY_TICKET_EVENT_ID_QUERY, ticket_event_id),
        }

        for key, (query, value) in search_criteria.items():
            if value:
                payments = await self.db.fetch_all(query=query, values={key: value})
                return [PaymentInDb(**payment) for payment in payments]

        payments = await self.db.fetch_all(query=GET_PAYMENTS_QUERY)
        return [PaymentInDb(**payment) for payment in payments]

    @handle_get_database_exceptions("Payment")
    async def get_organization_total_payments(
        self,
        *,
        organization_id: UUID,
        vote_event_id: Optional[UUID] = None,
        ticket_event_id: Optional[UUID] = None,
        event_type: Optional[EventType] = None,
    ) -> List[PaymentInDb]:
        """Get all payments by organization id."""
        base_query = GET_PAYMENTS_BY_ORGANIZATION_ID_QUERY
        query_values = {"organization_id": organization_id}

        if vote_event_id:
            base_query += " AND vote_event_id = :vote_event_id"
            query_values["vote_event_id"] = vote_event_id

        if ticket_event_id:
            base_query += " AND ticket_event_id = :ticket_event_id"
            query_values["ticket_event_id"] = ticket_event_id

        if event_type:
            base_query += " AND event_type = :event_type"
            query_values["event_type"] = event_type.value

        payments = await self.db.fetch_all(query=base_query, values=query_values)
        return [PaymentInDb(**payment) for payment in payments]

    @handle_get_database_exceptions("Payment")
    async def get_total_payments(
        self,
        *,
        organization_id: UUID = None,
        vote_event_id: UUID = None,
        ticket_event_id: UUID = None,
        event_type: Optional[EventType] = None,
    ) -> Decimal:
        """Get total payments."""
        search_criteria = {
            "organization_id": (
                GET_TOTAL_PAYMENTS_BY_ORGANIZATION_ID_QUERY,
                organization_id,
            ),
            "vote_event_id": (GET_TOTAL_PAYMENTS_BY_VOTE_EVENT_ID_QUERY, vote_event_id),
            "ticket_event_id": (
                GET_TOTAL_PAYMENTS_BY_TICKET_EVENT_ID_QUERY,
                ticket_event_id,
            ),
            "event_type": (
                GET_TOTAL_PAYMENTS_BY_EVENT_TYPE_QUERY,
                event_type.value if event_type else None,
            ),
        }

        for key, (query, value) in search_criteria.items():
            if value:
                total_payment = await self.db.fetch_val(
                    query=query, values={key: value}
                )
                return total_payment or 0.0

        raise ValueError("Please provide a valid search criteria")

    @handle_get_database_exceptions("Payment")
    async def delete_payment(self, *, id: UUID) -> PaymentInDb:
        """Delete a payment by its id."""
        deleted_payment = await self.db.fetch_one(
            query=DELETE_PAYMENT_BY_ID_QUERY, values={"id": id}
        )
        return PaymentInDb(**deleted_payment)
