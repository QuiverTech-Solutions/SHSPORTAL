"""Initial model

Revision ID: f06c85b28783
Revises:
Create Date: 2024-02-14 14:25:42.623439
"""

from typing import Optional, Sequence, Tuple, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f06c85b28783"
down_revision: Optional[str] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    """Create timestamp columns."""
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            index=indexed,
        ),
    )


def is_deleted() -> sa.Column:
    """Create is_deleted column."""
    return sa.Column(
        "is_deleted", sa.Boolean, nullable=False, server_default=sa.false(), index=True
    )


def create_users_table() -> None:
    """Create users table."""
    op.create_table(
        "users",
        sa.Column("user_id", sa.String(36), primary_key=True),
        sa.Column("first_name", sa.String(50), nullable=False),
        sa.Column("last_name", sa.String(50), nullable=False),
        sa.Column("email", sa.String(100), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role_id", sa.String(36), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("school_id", sa.String(36), sa.ForeignKey("schools.school_id")),
        sa.Column(
            "created_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")
        ),
    )


def create_students_table() -> None:
    """Create students table."""
    op.create_table(
        "students",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("index_number", sa.String(20), unique=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("dob", sa.Date, nullable=False),
        sa.Column("school_id", sa.String(36), sa.ForeignKey("schools.id")),
        sa.Column("location", sa.String(100), nullable=False),
        sa.Column("registration_paid", sa.Boolean, default=False),
        sa.Column(
            "created_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")
        ),
    )


def create_schools_table() -> None:
    """Create schools table."""
    op.create_table(
        "schools",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("location", sa.String(100), nullable=False),
        sa.Column("registration_fee", sa.Numeric(10, 2), default=0.00),
        sa.Column(
            "created_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")
        ),
    )


def create_roles_table() -> None:
    """Create roles table."""
    op.create_table(
        "roles",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        *timestamps(),
        is_deleted(),
    )
    op.create_index(
        "uq_roles_name_is_deleted",
        "roles",
        ["name", "is_deleted"],
        unique=True,
    )


def create_user_roles_table() -> None:
    """Create user_roles table."""
    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.user_id"), index=True),
        sa.Column("role_id", sa.String(36), sa.ForeignKey("roles.id"), index=True),
        *timestamps(),
        is_deleted(),
    )
    op.create_index(
        "uq_user_roles_user_id_role_id_is_deleted",
        "user_roles",
        ["user_id", "role_id", "is_deleted"],
        unique=True,
    )


def create_transactions_table() -> None:
    """Create transactions table."""
    op.create_table(
        "transactions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("student_name", sa.String(100), nullable=False),
        sa.Column("school_id", sa.String(36), sa.ForeignKey("schools.id")),
        sa.Column("school_name", sa.String(100), nullable=False),
        sa.Column("reference", sa.String(50), nullable=False),
        sa.CheckConstraint("amount >= 0", name="check_transaction_amount_positive"),
        *timestamps(),
        is_deleted(),
    )
    op.create_index(
        "uq_transactions_reference_is_deleted",
        "transactions",
        ["reference", "is_deleted"],
        unique=True,
    )


def create_payments_table() -> None:
    """Create payments table."""
    op.create_table(
        "payments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("student_id", sa.String(36), sa.ForeignKey("students.id")),
        sa.Column("school_id", sa.String(36), sa.ForeignKey("schools.id")),
        sa.Column("total_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("school_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("admin_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("payment_status", sa.String(50), default="pending"),
        sa.Column("payment_method", sa.String(50), nullable=False),
        sa.Column("transaction_reference", sa.String(100), unique=True, nullable=False),
        sa.Column("paid_at", sa.TIMESTAMP),
        *timestamps(),
        is_deleted(),
    )


def create_settings_table() -> None:
    """Create settings table."""
    op.create_table(
        "settings",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("key", sa.String(50), nullable=False, unique=True, index=True),
        sa.Column("value", sa.String(255), nullable=False),
        *timestamps(),
        is_deleted(),
    )


def upgrade() -> None:
    """Upgrade database."""
    create_roles_table()
    create_user_roles_table()
    create_users_table()
    create_schools_table()
    create_students_table()
    create_transactions_table()
    create_payments_table()
    create_settings_table()


def downgrade() -> None:
    """Downgrade database."""
    tables = [
        "user_roles",
        "roles",
        "transactions",
        "payments",
        "settings",
        "students",
        "schools",
        "users",
    ]

    for table in tables:
        op.execute(f"DROP TABLE IF EXISTS {table}")
