
from alembic import op
import sqlalchemy as sa
from typing import Tuple



def create_uuid_default():
    return sa.text("(UUID())")


def create_updated_at_trigger(table_name: str, trigger_name: str) -> None:
    """Create a trigger to update the updated_at timestamp on a table."""


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    """timestamps for columns."""
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )


def is_deleted() -> sa.Column:
    """Create is_deleted column."""
    return sa.Column(
        "is_deleted", sa.Boolean, nullable=False, server_default=sa.false(), index=True
    )


def create_schools_table() -> None:
    """Create Schools table."""
    users = op.create_table(
        'schools',
        sa.Column('id', sa.String(36), primary_key=True, server_default=create_uuid_default()),
        sa.Column('school_name', sa.String(255), nullable=False, unique=True),
        sa.Column('location', sa.String(255), nullable=False),
        sa.Column('district', sa.String(255), nullable=False),
        sa.Column('region', sa.String(255), nullable=False),
        is_deleted(),
        *timestamps(),
    )


def create_students_table() -> None:
    """Create Students table."""
    op.create_table(
        'students',
        sa.Column('id', sa.String(36), primary_key=True, server_default=create_uuid_default()),
        sa.Column('jhs_index_number', sa.String(20), nullable=False, unique=True),
        sa.Column('student_name', sa.String(255), nullable=False),
        sa.Column('gender', sa.String(10), nullable=False),
        sa.Column('date_of_birth', sa.Date, nullable=False),
        sa.Column('school_id', sa.String(36), sa.ForeignKey('schools.id'), nullable=False),
        is_deleted(),
        *timestamps(),
    )


def create_admissions_table() -> None:
    """Create Admissions table."""
    op.create_table(
        'admissions',
        sa.Column('id', sa.String(36), primary_key=True, server_default=create_uuid_default()),
        sa.Column('student_id', sa.String(36), sa.ForeignKey('students.id'), nullable=False),
        sa.Column('school_id', sa.String(36), sa.ForeignKey('schools.id'), nullable=False),
        sa.Column('admission_status', sa.String(20), nullable=False),
        sa.Column('admission_date', sa.Date, nullable=False),
        is_deleted(),
        *timestamps(),
    )


def create_payments_table() -> None:
    """Create Payments table."""
    op.create_table(
        'payments',
        sa.Column('id', sa.String(36), primary_key=True, server_default=create_uuid_default()),
        sa.Column('admission_id', sa.String(36), sa.ForeignKey('admissions.id'), nullable=False),
        sa.Column('payment_type', sa.String(50), nullable=False),
        sa.Column('payment_method', sa.String(50), nullable=False),
        sa.Column('payment_reference', sa.String(255), unique=True, nullable=True),
        sa.Column('payment_date', sa.Date, nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        is_deleted(),
        *timestamps(),
    )


def create_user_accounts_table() -> None:
    """Create UserAccounts table."""
    op.create_table(
        'user_accounts',
        sa.Column('id', sa.String(36), primary_key=True, server_default=create_uuid_default()),
        sa.Column('username', sa.String(255), nullable=False, unique=True),
        sa.Column('user_password', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('user_role', sa.String(50), nullable=False),
        sa.Column('user_status', sa.String(50), nullable=False),
        is_deleted(),
        *timestamps(),
    )


def create_payment_plans_table() -> None:
    """Create payment plans table."""
    # Create payment_plans table
    payment_plan = op.create_table(
        "payment_plans",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("price_percentage", sa.Float, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        *timestamps(),
        is_deleted(),
    )

    # Create trigger for updating 'updated_at' column before update
    op.execute(
        """
        CREATE TRIGGER update_payment_plan_modtime
        BEFORE UPDATE
        ON payment_plans
        FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )

    # Insert initial data into payment_plans table
    op.bulk_insert(
        payment_plan,
        [
            {
                "name": "Basic",
                "description": "Basic payment plan description",
                "price_percentage": 10,
            },
            {
                "name": "Premium",
                "description": "Premium payment plan description",
                "price_percentage": 15,
            },
        ],
    )


def create_tables():
    """Upgrade the database."""
    create_schools_table()
    create_students_table()
    create_admissions_table()
    create_payments_table()
    create_user_accounts_table()
    create_payment_plans_table()


def drop_tables():
    """Downgrade the database."""
    op.drop_table('payment_plans')
    op.drop_table('user_accounts')
    op.drop_table('payments')
    op.drop_table('admissions')
    op.drop_table('students')
    op.drop_table('schools')
