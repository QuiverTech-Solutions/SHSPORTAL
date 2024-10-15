import hashlib
import time
import uuid
import re
from typing import Optional
import validators

class SHSApplicationUtils:

    @staticmethod
    def generate_application_unique_code(student: dict) -> str:
        """Generate a hashed unique code for a student application."""
        base_string = f"{student['student_id']}{student['name'].lower()}{student['birth_date']}{student['application_year']}"
        normalized_string = base_string.replace(" ", "").lower()

        hash_object = hashlib.sha256()
        hash_object.update(normalized_string.encode("utf-8"))
        hashed_code = hash_object.hexdigest()

        return hashed_code

    @staticmethod
    def generate_transaction_id(email: str, student_id: str) -> str:
        """Create a unique input string by combining the email and student ID."""
        current_time = str(time.time())
        unique_input = f"{email}-{student_id}-{current_time}"
        namespace = uuid.NAMESPACE_OID
        unique_hash = uuid.uuid5(namespace, unique_input).hex
        allowed_id = re.sub(r"[^a-zA-Z0-9-.=]", "-", unique_hash)

        return allowed_id

    @staticmethod
    def generate_n_digit_uuid(value: int) -> str:
        """Generate n digit uuid."""
        return str(uuid.uuid4().hex[:value])

    @staticmethod
    def validate_email(email: str) -> Optional[str]:
        """Check if an email is valid, returns a valid email or None."""
        if email is not None:
            email = email.strip()
            try:
                if validators.email(email):
                    return email
                return None
            except Exception as e:
                print(e)
                raise ValueError("Invalid email format")
        else:
            return None

    @staticmethod
    def validate_student_id(student_id: str) -> Optional[str]:
        """Check if a student ID is valid, returns the student ID or None."""
        if student_id is not None:
            student_id = student_id.strip()
            if re.match(r"^[a-zA-Z0-9]{6,}$", student_id): 
                return student_id
            return None
        else:
            return None
