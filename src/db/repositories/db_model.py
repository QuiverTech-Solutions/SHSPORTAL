from sqlalchemy import Column, String, Boolean, Date, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from utils.databse import Base
from sqlalchemy.types import TIMESTAMP


def timestamps(indexed: bool = False):
    """Return created_at and updated_at columns."""
    return (
        Column("created_at", TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=indexed),
        Column("updated_at", TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, index=indexed),
    )


def is_deleted():
    """Return is_deleted column."""
    return Column("is_deleted", Boolean, nullable=False, server_default="0", index=True)


class School(Base):
    __tablename__ = "schools"

    id = Column(String(36), primary_key=True, server_default=func.uuid_generate_v4())
    school_name = Column(String(255), nullable=False, unique=True)
    location = Column(String(255), nullable=False)
    district = Column(String(255), nullable=False)
    region = Column(String(255), nullable=False)
    is_deleted = is_deleted()
    created_at, updated_at = timestamps()

    # Relationships
    students = relationship("Student", back_populates="school")
    admissions = relationship("Admission", back_populates="school")


class Student(Base):
    __tablename__ = "students"

    id = Column(String(36), primary_key=True, server_default=func.uuid_generate_v4())
    jhs_index_number = Column(String(20), nullable=False, unique=True)
    student_name = Column(String(255), nullable=False)
    gender = Column(String(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    school_id = Column(String(36), ForeignKey('schools.id'), nullable=False)
    is_deleted = is_deleted()
    created_at, updated_at = timestamps()

    # Relationships
    school = relationship("School", back_populates="students")
    admissions = relationship("Admission", back_populates="student")


class Admission(Base):
    __tablename__ = "admissions"

    id = Column(String(36), primary_key=True, server_default=func.uuid_generate_v4())
    student_id = Column(String(36), ForeignKey('students.id'), nullable=False)
    school_id = Column(String(36), ForeignKey('schools.id'), nullable=False)
    admission_status = Column(String(20), nullable=False)
    admission_date = Column(Date, nullable=False)
    is_deleted = is_deleted()
    created_at, updated_at = timestamps()

    # Relationships
    student = relationship("Student", back_populates="admissions")
    school = relationship("School", back_populates="admissions")
    payments = relationship("Payment", back_populates="admission")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String(36), primary_key=True, server_default=func.uuid_generate_v4())
    admission_id = Column(String(36), ForeignKey('admissions.id'), nullable=False)
    payment_type = Column(String(50), nullable=False)
    payment_method = Column(String(50), nullable=False)
    payment_reference = Column(String(255), unique=True, nullable=True)
    payment_date = Column(Date, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    is_deleted = is_deleted()
    created_at, updated_at = timestamps()

    # Relationships
    admission = relationship("Admission", back_populates="payments")


class UserAccount(Base):
    __tablename__ = "user_accounts"

    id = Column(String(36), primary_key=True, server_default=func.uuid_generate_v4())
    username = Column(String(255), nullable=False, unique=True)
    user_password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    user_role = Column(String(50), nullable=False)
    user_status = Column(String(50), nullable=False)
    is_deleted = is_deleted()
    created_at, updated_at = timestamps()
