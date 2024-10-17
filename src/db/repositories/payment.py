"""Payment repository."""

import logging
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
import sqlite3
from datetime import datetime

from src.models.payments import PaymentCreate, PaymentInDb
from src.errors.database import NotFoundError

DATABASE_URL = "db_model.sqlite"  # Adjust with the correct path to your SQLite file

# Define raw SQL queries
CREATE_PAYMENT_QUERY = """
INSERT INTO payments (student_id, school_id, total_amount, school_amount, admin_amount, 
                      payment_status, payment_method, transaction_reference, paid_at)
VALUES (:student_id, :school_id, :total_amount, :school_amount, :admin_amount, 
        :payment_status, :payment_method, :transaction_reference, :paid_at)
RETURNING id, student_id, school_id, total_amount, school_amount, admin_amount, 
          payment_status, payment_method, transaction_reference, paid_at, created_at, updated_at
"""

GET_PAYMENT_BY_ID_QUERY = """
SELECT * FROM payments WHERE id = :id
"""

GET_PAYMENTS_QUERY = """
SELECT * FROM payments ORDER BY created_at DESC
"""

UPDATE_PAYMENT_QUERY = """
UPDATE payments SET student_id = :student_id, school_id = :school_id, total_amount = :total_amount, 
                    school_amount = :school_amount, admin_amount = :admin_amount, 
                    payment_status = :payment_status, payment_method = :payment_method, 
                    transaction_reference = :transaction_reference, paid_at = :paid_at
WHERE id = :id
RETURNING *;
"""

DELETE_PAYMENT_BY_ID_QUERY = """
DELETE FROM payments WHERE id = :id
"""

audit_logger = logging.getLogger("audit")


class PaymentRepository:
    """Payment repository."""

    def __init__(self, db_url: str = DATABASE_URL) -> None:
        """Constructor for Payment repository."""
        self.db_url = db_url

    def _get_connection(self):
        """Create a new database connection."""
        return sqlite3.connect(self.db_url)

    def create_payment(self, new_payment: PaymentCreate) -> PaymentInDb:
        """Create a new payment."""
        audit_logger.info("Adding payment...", new_payment.dict())
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute(CREATE_PAYMENT_QUERY, new_payment.dict())
            payment_data = cursor.fetchone()
            conn.commit()
            audit_logger.info("Payment added successfully")
            return PaymentInDb(**dict(payment_data))
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_payment(self, id: UUID) -> PaymentInDb:
        """Get payment by id."""
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute(GET_PAYMENT_BY_ID_QUERY, {"id": str(id)})
            payment_data = cursor.fetchone()
            if payment_data is None:
                raise NotFoundError(f"Payment with id {id} not found")
            return PaymentInDb(**dict(payment_data))
        finally:
            cursor.close()
            conn.close()

    def get_payments(self) -> List[PaymentInDb]:
        """Get all payments."""
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute(GET_PAYMENTS_QUERY)
            payments = cursor.fetchall()
            return [PaymentInDb(**dict(payment)) for payment in payments]
        finally:
            cursor.close()
            conn.close()

    def update_payment(self, id: UUID, updated_payment: PaymentCreate) -> PaymentInDb:
        """Update a payment by id."""
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute(
                UPDATE_PAYMENT_QUERY, {**updated_payment.dict(), "id": str(id)}
            )
            payment_data = cursor.fetchone()
            conn.commit()
            if payment_data is None:
                raise NotFoundError(f"Payment with id {id} not found")
            return PaymentInDb(**dict(payment_data))
        finally:
            cursor.close()
            conn.close()

    def delete_payment(self, id: UUID) -> None:
        """Delete a payment by its id."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(DELETE_PAYMENT_BY_ID_QUERY, {"id": str(id)})
            conn.commit()
        finally:
            cursor.close()
            conn.close()
